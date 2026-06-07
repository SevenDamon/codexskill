const fs = require('fs');
const path = require('path');

const skillRoot = path.resolve(__dirname, '..');
const templateDir = path.join(skillRoot, 'assets', 'local-card-app');
const targetArg = process.argv[2];

if (!targetArg) {
  console.error('Usage: node scripts/scaffold.js <target-directory>');
  process.exit(1);
}

const targetDir = path.resolve(process.cwd(), targetArg);

function copyDir(source, target) {
  if (!fs.existsSync(source)) {
    throw new Error(`Template directory not found: ${source}`);
  }
  fs.mkdirSync(target, { recursive: true });
  for (const entry of fs.readdirSync(source, { withFileTypes: true })) {
    const sourcePath = path.join(source, entry.name);
    const targetPath = path.join(target, entry.name);
    if (entry.isDirectory()) {
      copyDir(sourcePath, targetPath);
    } else {
      if (fs.existsSync(targetPath)) {
        throw new Error(`Refusing to overwrite existing file: ${targetPath}`);
      }
      fs.copyFileSync(sourcePath, targetPath);
    }
  }
}

try {
  copyDir(templateDir, targetDir);
  console.log(`Created local XHS card app at: ${targetDir}`);
  console.log('Next steps:');
  console.log(`  cd "${targetDir}"`);
  console.log('  npm.cmd install');
  console.log('  node server.js');
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
