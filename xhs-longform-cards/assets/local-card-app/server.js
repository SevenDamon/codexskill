const fs = require('fs');
const path = require('path');
const express = require('express');
const cors = require('cors');
const puppeteer = require('puppeteer-core');

const app = express();
const port = Number(process.env.PORT || 3000);
const publicDir = path.join(__dirname, 'public');

app.use(cors());
app.use(express.json({ limit: '25mb' }));
app.use(express.static(publicDir, {
  setHeaders(res, filePath) {
    if (filePath.endsWith('.html')) {
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
    }
  }
}));

function existingFile(filePath) {
  return filePath && fs.existsSync(filePath) ? filePath : null;
}

function findBrowserExecutable() {
  const envPath = existingFile(process.env.CHROME_EXECUTABLE_PATH);
  if (envPath) return envPath;

  const candidates = [
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  ];

  const programFiles = process.env.ProgramFiles;
  const programFilesX86 = process.env['ProgramFiles(x86)'];
  if (programFiles) {
    candidates.push(path.join(programFiles, 'Google\\Chrome\\Application\\chrome.exe'));
    candidates.push(path.join(programFiles, 'Microsoft\\Edge\\Application\\msedge.exe'));
  }
  if (programFilesX86) {
    candidates.push(path.join(programFilesX86, 'Google\\Chrome\\Application\\chrome.exe'));
    candidates.push(path.join(programFilesX86, 'Microsoft\\Edge\\Application\\msedge.exe'));
  }

  return candidates.find(existingFile) || null;
}

function validateCardId(cardId) {
  return typeof cardId === 'string' && /^[A-Za-z0-9_-]{1,80}$/.test(cardId);
}

app.get('/api/health', (_req, res) => {
  const browserPath = findBrowserExecutable();
  res.json({
    ok: Boolean(browserPath),
    browserPath,
    port
  });
});

app.post('/api/screenshot', async (req, res) => {
  const { fullHtml, cardId } = req.body || {};
  if (typeof fullHtml !== 'string' || !fullHtml.trim()) {
    return res.status(400).json({ error: '没有提供完整 HTML。' });
  }
  if (!validateCardId(cardId)) {
    return res.status(400).json({ error: '卡片 ID 无效。' });
  }

  const executablePath = findBrowserExecutable();
  if (!executablePath) {
    return res.status(500).json({
      error: '没有找到 Chrome 或 Edge。请安装 Chrome/Edge，或设置 CHROME_EXECUTABLE_PATH。'
    });
  }

  let browser;
  try {
    browser = await puppeteer.launch({
      executablePath,
      headless: 'new',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--font-render-hinting=none'
      ]
    });

    const page = await browser.newPage();
    await page.setViewport({
      width: 1280,
      height: 900,
      deviceScaleFactor: 2
    });
    await page.setContent(fullHtml, {
      waitUntil: 'networkidle0',
      timeout: 30000
    });
    await page.evaluate(() => {
      document.body.classList.add('exporting');
    });

    const element = await page.$(`#${cardId}`);
    if (!element) {
      throw new Error(`找不到 ID 为 "${cardId}" 的卡片。`);
    }

    const imageBuffer = await element.screenshot({
      type: 'png',
      omitBackground: false
    });

    res.setHeader('Content-Type', 'image/png');
    res.setHeader('Cache-Control', 'no-store');
    res.send(imageBuffer);
  } catch (error) {
    console.error('Puppeteer screenshot failed:', error);
    res.status(500).json({
      error: `生成图片失败：${error.message}`
    });
  } finally {
    if (browser) {
      await browser.close().catch(() => {});
    }
  }
});

app.get('*', (_req, res) => {
  res.sendFile(path.join(publicDir, 'index.html'));
});

app.listen(port, () => {
  const browserPath = findBrowserExecutable();
  console.log(`长文转多图工具已启动：http://localhost:${port}`);
  console.log(browserPath ? `截图浏览器：${browserPath}` : '未找到 Chrome/Edge，截图接口暂不可用。');
});
