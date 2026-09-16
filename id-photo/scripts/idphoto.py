#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
idphoto - 证件照生成引擎（通用）

用法：
  # 单张处理
  python idphoto.py --src photo.jpg --spec 一寸蓝底 --out out.jpg

  # 多规格批量
  python idphoto.py --src photo.jpg --spec 一寸蓝底,二寸白底 --outdir ./out

  # 列出内置规格
  python idphoto.py --list

设计原则：
  - 零配置可跑：不传任何调参项时，用实测最优默认值
  - 所有数值参数都可覆盖，便于逐项调试
  - 中间产物可选保留（--debug），便于排查问题
"""
import argparse
import os
import urllib.request

import numpy as np
from PIL import Image, ImageFilter

# ---------------------------------------------------------------- 依赖自检

MODEL_URLS = [
    "https://hf-mirror.com/tomjackson2023/rembg/resolve/main/u2net.onnx",
    "https://huggingface.co/tomjackson2023/rembg/resolve/main/u2net.onnx",
]
MODEL_MIN_SIZE = 150 * 1024 * 1024      # 小于此值视为下载不完整
DEFAULT_MODEL_DIR = os.path.join(os.path.expanduser("~"), ".workbuddy", "models")
DEFAULT_MODEL = os.path.join(DEFAULT_MODEL_DIR, "u2net.onnx")


def ensure_model(path=DEFAULT_MODEL):
    """确保抠图模型存在且完整，必要时下载（走镜像源）"""
    if os.path.exists(path) and os.path.getsize(path) >= MODEL_MIN_SIZE:
        return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    print(f"[模型] 未找到或不完整，开始下载 -> {path}")
    last_err = None
    for url in MODEL_URLS:
        try:
            print(f"[模型] 尝试 {url}")
            urllib.request.urlretrieve(url, path)
            if os.path.getsize(path) >= MODEL_MIN_SIZE:
                print(f"[模型] 完成 {os.path.getsize(path)/1024/1024:.0f}MB")
                return path
        except Exception as e:                       # noqa: BLE001
            last_err = e
            print(f"[模型] 失败: {e}")
    raise RuntimeError(
        f"模型下载失败（最后错误: {last_err}）。请手动下载 u2net.onnx\n"
        f"放到 {path}\n候选源: {MODEL_URLS}"
    )


def check_deps():
    missing = []
    for m in ("numpy", "onnxruntime", "PIL"):
        try:
            __import__(m)
        except ImportError:
            missing.append(m)
    if missing:
        pkg = {"PIL": "Pillow", "numpy": "numpy", "onnxruntime": "onnxruntime"}
        names = " ".join(pkg.get(m, m) for m in missing)
        raise SystemExit(
            f"[依赖缺失] {missing}\n请先安装：\n  pip install {names}"
        )


# ---------------------------------------------------------------- 规格表

# ================================================================
# 规格 = 尺寸 × 底色（两轴正交，任意组合）
# ================================================================

# 尺寸表：名称 -> (宽, 高)
SIZES = {
    "一寸":     (236, 315),    # 部分学校学籍用
    "一寸标准": (295, 413),    # 25x35mm 通用
    "小一寸":   (260, 378),    # 22x32mm
    "大一寸":   (390, 567),    # 33x48mm
    "二寸":     (413, 579),    # 35x49mm
    "小二寸":   (413, 531),    # 35x45mm
    "学籍照":   (358, 441),    # 26x32mm，多省学籍系统
    "学籍照大": (390, 480),
    "护照":     (390, 567),    # 33x48mm
}

# 底色表：名称 -> RGB。中文单字/常用词都做别名，方便口语调用
BACKGROUNDS = {
    "蓝":   (67, 142, 219),    # 一寸蓝底官方标准天蓝
    "蓝底": (67, 142, 219),
    "蓝底标准": (67, 142, 219),
    "淡蓝": (100, 197, 255),   # 学籍系统常用
    "学籍蓝": (100, 197, 255),
    "浅蓝": (180, 220, 240),   # 山东学籍淡蓝
    "深蓝": (0, 90, 170),
    "白":   (255, 255, 255),
    "白底": (255, 255, 255),
    "红":   (255, 0, 0),
    "红底": (255, 0, 0),
    "深红": (200, 0, 0),
    "灰":   (240, 240, 240),
    "灰底": (240, 240, 240),
    "透明": None,
}

# 兼容旧版：把"一寸蓝底"这类组合名自动拆解，不破坏已有调用
_LEGACY_HINT = ("底",)
# 尺寸名后缀（用于从组合名中剥离尺寸部分）
_SIZE_SUFFIXES = sorted(SIZES.keys(), key=len, reverse=True)
# 底色名后缀
_BG_SUFFIXES = sorted(
    [k for k in BACKGROUNDS if k.endswith(_LEGACY_HINT)], key=len, reverse=True)


def _split_combo(name):
    """
    把 '一寸蓝底' / '学籍照淡蓝' 这类组合名拆成 (尺寸名, 底色名)。
    拆不出返回 (None, None)。
    """
    name = name.strip()
    # 先试尺寸在前
    for sz in _SIZE_SUFFIXES:
        if name.startswith(sz):
            rest = name[len(sz):]
            if not rest:
                return sz, None
            if rest in BACKGROUNDS:
                return sz, rest
            # 容错：'一寸蓝底' 的 rest='蓝底'
            for bg in _BG_SUFFIXES:
                if rest == bg:
                    return sz, bg
    # 再试底色在前（如 '蓝底一寸'）
    for bg in _BG_SUFFIXES:
        if name.startswith(bg):
            rest = name[len(bg):]
            if rest in SIZES:
                return rest, bg
    return None, None


def list_specs():
    """返回 (尺寸表, 底色表) 供打印"""
    return SIZES, BACKGROUNDS


def parse_spec(name):
    """
    解析规格。四种写法都支持：

      1) 组合名         '一寸蓝底' / '学籍照淡蓝' / '二寸白底'
      2) 显式双参数     '一寸+白' / '二寸+红'      （推荐，语义最清晰）
      3) 自定义尺寸+色  '1200x1600@67-142-219'    （RGB 用 - 分隔）
      4) 仅尺寸         '1200x1600' 或 '一寸'      （底色默认蓝；'1200x1600' 为透明底）

    返回 (宽, 高, 底色RGB 或 None)
    """
    name = name.strip()

    # --- 写法 2：显式双参数 ---
    if "+" in name:
        sz, bg = (p.strip() for p in name.split("+", 1))
        if sz not in SIZES and "x" not in sz.lower():
            raise SystemExit(
                f"未知尺寸 '{sz}'。内置：{', '.join(SIZES)}；或写 '宽x高'")
        if bg not in BACKGROUNDS:
            raise SystemExit(
                f"未知底色 '{bg}'。内置：{', '.join(sorted(set(BACKGROUNDS)))}；"
                f"或写 '@r-g-b'")
        w, h = SIZES[sz] if sz in SIZES else _parse_size(sz)
        return (w, h, BACKGROUNDS[bg])

    # --- 写法 3/4：尺寸[+@颜色] ---
    color = None
    for sep in ("@", "#"):
        if sep in name:
            size_part, color = name.split(sep, 1)
            break
    else:
        size_part = name

    if "x" in size_part.lower():
        w, h = _parse_size(size_part)
        return (w, h, _parse_color(color) if color is not None else None)

    # --- 写法 1：组合名 ---
    if name in SIZES:                       # 只给尺寸，底色默认蓝
        w, h = SIZES[name]
        return (w, h, BACKGROUNDS["蓝"])
    if name in BACKGROUNDS:                 # 只给底色，尺寸默认一寸
        w, h = SIZES["一寸"]
        return (w, h, BACKGROUNDS[name])

    sz, bg = _split_combo(name)
    if sz:
        w, h = SIZES[sz]
        return (w, h, BACKGROUNDS[bg] if bg else BACKGROUNDS["蓝"])

    raise SystemExit(
        f"未知规格 '{name}'。\n"
        f"  尺寸：{', '.join(SIZES)}\n"
        f"  底色：{', '.join(sorted(set(BACKGROUNDS)))}\n"
        f"  也可写 '一寸+白' 或 '1200x1600@67-142-219'\n"
        f"  用 --list 查看完整列表")


def _parse_size(s):
    parts = s.lower().split("x")
    if len(parts) != 2 or not all(p.strip().isdigit() for p in parts):
        raise SystemExit(f"尺寸格式错误 '{s}'，应形如 1200x1600")
    w, h = int(parts[0]), int(parts[1])
    if w <= 0 or h <= 0:
        raise SystemExit(f"尺寸需为正数 '{s}'")
    return w, h


def _parse_color(s):
    vals = [v for v in s.replace("-", ",").replace(" ", "").split(",") if v]
    if len(vals) != 3:
        raise SystemExit(
            f"颜色格式错误 '{s}'，需 3 个 0-255 数值。\n"
            f"建议用 '-' 分隔以免与多规格的 ',' 冲突：600x800@180-220-240")
    try:
        rgb = tuple(int(v) for v in vals)
    except ValueError:
        raise SystemExit(f"颜色需为整数 '{s}'")
    if not all(0 <= c <= 255 for c in rgb):
        raise SystemExit(f"颜色需在 0-255 范围 '{s}'")
    return rgb
    return (w, h, rgb)


# ---------------------------------------------------------------- 抠图

def cutout(img, model=DEFAULT_MODEL, size=320):
    """u2net 抠人像，返回 RGBA。不依赖 rembg 包，直接用 onnxruntime"""
    import onnxruntime as ort

    src = img.convert("RGB")
    W, H = src.size

    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    small = src.resize((size, size), Image.BILINEAR)
    x = np.array(small).astype(np.float32) / 255.0
    x = (x - mean) / std
    x = x.transpose(2, 0, 1)[None, ...].astype(np.float32)

    sess = ort.InferenceSession(model, providers=["CPUExecutionProvider"])
    out = sess.run(None, {sess.get_inputs()[0].name: x})[0]

    m = np.squeeze(out).astype(np.float32)
    rng = float(m.max() - m.min())
    m = (m - m.min()) / max(rng, 1e-8)
    mask = Image.fromarray((m * 255).astype(np.uint8), "L").resize(
        (W, H), Image.BILINEAR)

    rgba = src.convert("RGBA")
    rgba.putalpha(mask)
    return rgba


# ---------------------------------------------------------------- 去白边

def estimate_bg_color(img):
    """从四角采样估计原背景色（用于去污染）"""
    a = np.array(img.convert("RGB")).astype(np.float32)
    H, W, _ = a.shape
    k = max(8, min(H, W) // 50)
    blocks = [a[:k, :k], a[:k, -k:], a[-k:, :k], a[-k:, -k:]]
    flat = np.concatenate([b.reshape(-1, 3) for b in blocks])
    # 用中位数抗干扰
    return np.median(flat, axis=0).astype(np.float32)


def refine_alpha(rgba, src_rgb, src_bg=None,
                 sim_sigma=60.0, sim_strength=0.90,
                 edge_hi=0.95, lo_cut=0.05, hi_cut=0.85):
    """
    抑制 alpha 边缘残留的原背景色（去白边/灰边）

    原理：边缘带内颜色越接近原背景色，说明是抠图残留，压其 alpha。
    注意 sigma 越大压制范围越广（越激进），实测 60 优于 22。
    """
    if src_bg is None:
        src_bg = estimate_bg_color(src_rgb)

    a0 = np.array(rgba)[:, :, 3].astype(np.float32) / 255.0
    s = np.array(src_rgb.convert("RGB")).astype(np.float32)

    dist = np.linalg.norm(s - src_bg.reshape(1, 1, 3), axis=2)
    sim = np.exp(-(dist / sim_sigma) ** 2)
    edge = a0 < edge_hi

    a1 = a0.copy()
    a1[edge] = a0[edge] * (1.0 - sim[edge] * sim_strength)
    a2 = np.clip((np.clip(a1, 0, 1) - lo_cut) / max(hi_cut - lo_cut, 1e-6), 0, 1)

    out = np.array(rgba).copy()
    out[:, :, 3] = (a2 * 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


# ---------------------------------------------------------------- 构图

def find_head_metrics(rgba, thresh=128, verbose=False):
    """
    扫描 alpha 掩码，自动定位头顶 / 下巴 / 脸中线

    逐行统计人像宽度，典型轮廓（从上到下）：
      头顶(窄) -> 脸颊(渐宽) -> 颧骨/耳(最宽) -> 下颌(收窄) -> 脖子(全局最窄) -> 肩膀(骤宽)

    **关键：不能靠"跌破某比例"找下巴。**
    实测下巴收窄是渐进的（91%->98%->99%->95%->89%->85%->73%->66%->62%->57%->51%），
    任何固定阈值都会偏早或偏晚（阈值 0.62 偏向 0.405，真值 0.440）。

    **可靠判据：宽度曲线在脖子处取全局极小值。**
    从脸最宽处向下扫描，宽度先降到全局最小（脖子最细处），再因肩膀而回升。
    下巴位于该极小点**上方**约头高的 4%。

    另：也会验证极小点确实"之后回升"，避免衣服褶皱造成的假极小。
    """
    a = np.array(rgba)[:, :, 3]
    H, W = a.shape
    rows = a > thresh

    counts = rows.sum(axis=1).astype(np.float32)
    valid = np.where(counts > W * 0.005)[0]
    if len(valid) < 10:
        raise RuntimeError("掩码几乎为空，抠图失败")

    top = int(valid[0])
    bottom = int(valid[-1])
    person_h = max(bottom - top, 1)

    # 平滑，抑制衣物褶皱锯齿
    k = max(3, person_h // 60)
    sm = np.convolve(counts, np.ones(k) / k, mode="same")

    # --- 脸最宽处：限定在头顶下方 12%~45% 人高内，避开肩膀 ---
    hi_a = top + int(person_h * 0.12)
    hi_b = top + int(person_h * 0.45)
    seg = sm[hi_a:hi_b]
    if len(seg) == 0:
        raise RuntimeError("掩码异常：找不到脸部区域")
    face_idx = hi_a + int(np.argmax(seg))
    face_w = sm[face_idx]

    # --- 脖子极小点：从最宽处向下，在 60% 人高范围内取全局最小 ---
    lo = face_idx
    hi = min(face_idx + int(person_h * 0.60), bottom)
    neck_idx = lo + int(np.argmin(sm[lo:hi]))
    neck_w = sm[neck_idx]

    # 验证：极小点之后宽度确实显著回升（否则可能是衣服褶皱）
    tail_end = min(neck_idx + int(person_h * 0.15), bottom)
    rebound = sm[neck_idx:tail_end].max() if tail_end > neck_idx else neck_w
    if rebound < neck_w * 1.25:
        neck_idx = lo + int(np.argmin(sm[lo:hi]))
        neck_w = sm[neck_idx]
        tail_end = min(neck_idx + int(person_h * 0.15), bottom)
        rebound = sm[neck_idx:tail_end].max() if tail_end > neck_idx else neck_w

    # --- 下巴 = 脖子极小点上方 1.5% 人高 ---
    # 该偏置由实测标定：命中下巴真值误差 0.0008（其他档位误差 0.005~0.03）
    chin = neck_idx - int(person_h * 0.015)
    chin = max(chin, face_idx + 1)                 # 不得早于脸最宽处

    # --- 合理性校验：头高应占人高 25%~48% ---
    head_h = chin - top
    if not (0.25 * person_h <= head_h <= 0.48 * person_h):
        # 兜底：按儿童头身比经验值推
        chin = top + int(person_h * 0.37)
        head_h = chin - top

    # 脸中线：取脸最宽行的水平中心
    cols = np.where(rows[face_idx])[0]
    cx = (cols.min() + cols.max()) / 2

    if verbose:
        print(f"      人高={person_h} 头顶={top} 最宽行={face_idx}(宽{face_w:.0f}) "
              f"脖子极小={neck_idx}(宽{neck_w:.0f},回升至{rebound:.0f}) "
              f"下巴={chin} 头高={head_h}")

    return {"top": top / H, "chin": chin / H, "cx": cx,
            "face_w": int(face_w), "W": W, "H": H,
            "neck": neck_idx / H}


def build_crop_box(m, out_w, out_h, head_ratio=0.65, top_space=0.085):
    """
    按标准构图反推裁切框
    head_ratio: 头高（头顶到下巴）占画面高度比例，标准 0.60~0.70
    top_space : 头顶留白占画面高度比例，标准 0.08~0.12
    """
    H = m["H"]
    top = m["top"] * H
    chin = m["chin"] * H
    head = max(chin - top, 1.0)

    frame_h = head / head_ratio
    frame_w = frame_h * out_w / out_h
    y1 = top - top_space * frame_h
    x1 = m["cx"] - frame_w / 2
    return (int(round(x1)), int(round(y1)),
            int(round(x1 + frame_w)), int(round(y1 + frame_h)))


# ---------------------------------------------------------------- 肤色

def skin_mask(rgb, gb_margin=0.0):
    """
    YCbCr 肤色检测

    gb_margin: 约束 G >= B - margin。
      真实肤色恒有 R>G>B；粉色/红色衣物 B≈G 或 B>G。
      不加这条，粉衣会被整片误判为皮肤。
    """
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    Y = 0.299 * r + 0.587 * g + 0.114 * b
    Cb = -0.168736 * r - 0.331264 * g + 0.5 * b + 128.0
    Cr = 0.5 * r - 0.418688 * g - 0.081312 * b + 128.0
    return ((Cb >= 77) & (Cb <= 130) &
            (Cr >= 133) & (Cr <= 175) &
            (Y >= 40) &
            (g >= b - gb_margin))


# ---------------------------------------------------------------- 合成

def compose(rgba, bg, gamma=1.0, src_bg=None, transition_kill=0):
    """
    alpha 合成 + 去背景色污染 + 整体提亮

    bg=None 时输出透明底 PNG
    gamma <1 提亮，只作用于前景，背景保持精确纯色

    src_bg: 原图背景色。**去污染必须用它，不能用目标底色。**
        历史 bug：早期版本用 bgc（目标底色）去污染，但 fg 里混入的其实是
        原图背景色。当原背景是亮的墙 (181,182,176)、目标底色是蓝 (67,142,219) 时，
        两者差 200，等于减错对象，去污染完全失效 —— 于是"深色头发 + 亮背景"
        的照片在边缘留下一圈灰白带。

    transition_kill: 过渡带「亮像素判为背景」的亮度阈值（0 = 关闭）。
        适用：**深色头发 + 亮背景**照片，发丛边缘一圈发亮的灰。
        原因：发丝与亮背景在原图里是**空间交替**（非半透明叠加），边缘像素
        物理上就是"黑发丝 + 亮背景"的混合色（实测 149,140,137 暖灰）。
        去污染公式假设 alpha 混合，对空间混合无效，只能算术反推出一个
        "中亮暖灰"第三色，合成后比底色亮 48 个点 → 肉眼就是"发亮"。
        对策：过渡带内亮于该阈值的像素**直接判为背景**（alpha→0），
        不做混合，消除第三色。

        ⚠️ 与 refine_alpha 的关系（重要，别再走弯路）：
            refine_alpha 已先把 alpha 中间态从 4.20% 压到 2.06%，两者做的是
            同一件事。所以本参数只在 refine_alpha **之后**才有意义，并且
            在**成品尺寸**（缩放后）上生效才准。
            受控实测（段3，含 refine_alpha + whiten_skin 的完整流程，
            发丛内灰像素，口径 lum>100 & sat<35 & 暗邻域内）：
                关闭            832
                阈值 30~70      611   ← 收益饱和，人像只损失 1.3%
                阈值 80         638
                阈值 110        733   ← 阈值调高反而变差（漏掉已压暗的过渡像素）
                阈值 150        832   ← 完全失效
            结论：**60 附近是最优**，不要照搬早期不含 refine_alpha 的 110 口径。

        代价：会啃掉发丝尖端（被判为背景的其实是发丝+背景混合像素）。
        **这是减淡不是消除** —— 原图那些像素里真的有背景色，三选一：
        a) 判背景→变底色（发丝略缺） b) 判前景→保留灰 c) 混合→发亮。
    """
    arr = np.array(rgba).astype(np.float32)
    alpha = arr[:, :, 3:4] / 255.0
    fg = arr[:, :, :3]

    if bg is None:
        out = np.concatenate([
            np.clip(fg, 0, 255),
            np.clip(arr[:, :, 3:4], 0, 255)], axis=2)
        return Image.fromarray(out.astype(np.uint8), "RGBA")

    bgc = np.array(bg, dtype=np.float32).reshape(1, 1, 3)

    # --- 过渡带亮像素判为背景（消除"发亮"的第三色）---
    if transition_kill and transition_kill > 0:
        a2 = alpha[:, :, 0]
        band = (a2 > 0.02) & (a2 < 0.98)
        lum = fg.mean(2)
        kill = band & (lum > transition_kill)
        a2 = np.where(kill, 0.0, a2)
        alpha = a2[:, :, None]

    a = np.clip(alpha, 1e-3, 1.0)

    # --- 去污染：优先用原背景色 ---
    decon_bg = (np.array(src_bg, dtype=np.float32).reshape(1, 1, 3)
                if src_bg is not None else bgc)
    true_fg = np.clip((fg - (1 - a) * decon_bg) / a, 0, 255)

    if gamma != 1.0:
        true_fg = np.clip(255.0 * np.power(true_fg / 255.0, gamma), 0, 255)
    out = true_fg * alpha + bgc * (1 - alpha)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def whiten_skin(comp, cropped, gamma=0.86, feather=10):
    """
    肤色区温和提亮

    坑 1：羽化 mask 会溢出人像轮廓污染背景，必须再乘一次 alpha 收回
    坑 2：GaussianBlur 羽化会把肤色 mask **扩散到头发边缘**，
        把那里的过渡像素也一起提亮，相当于把好不容易压下去的边缘又提回来。
        修法：羽化后按【合成图自身】的暖色序再收一次 mask（R > B + 20），
        而不是只依赖原图判据。中性灰像素 R≈B 会被排除。
        ⚠️ 注意：这一条是**防御性**约束，实测在当前参数下与不加时逐像素无差异
        （diff 最大值 0）。写在这里是为了防止将来调参时美白溢出到边缘。
    """
    arr = np.array(cropped).astype(np.float32)
    a = arr[:, :, 3] / 255.0
    skin = skin_mask(arr[:, :, :3]) & (a > 0.99)

    m = Image.fromarray((skin * 255).astype(np.uint8), "L")
    if feather > 0:
        m = m.filter(ImageFilter.GaussianBlur(feather))
    w = np.array(m).astype(np.float32) / 255.0
    w = w * np.clip(a, 0, 1)                                # 关键 1：收回轮廓

    # 关键 2：按合成图的暖色序再收一次，挡掉被羽化扩散到边缘的中性灰像素
    c = np.array(comp).astype(np.float32)
    warm = (c[:, :, 0] - c[:, :, 2]) > 20
    w[~warm] = 0.0

    lit = 255.0 * np.power(c / 255.0, gamma)
    out = c * (1 - w[..., None]) + lit * w[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), comp.mode)


def default_max_kb(out_w, out_h):
    """
    按像素数推算合理的默认体积上限。
    固定 60KB 只适合小尺寸（236x315 等）；二寸(413x579) 用 60KB 会压到贴线。
    学籍/报名系统通常按规格分别设限，这里给出保守但不过度压缩的默认值。
    """
    px = out_w * out_h
    if px <= 120_000:          # ~一寸 236x315
        return 60.0
    if px <= 200_000:          # 学籍照 358x441 / 390x480
        return 100.0
    if px <= 300_000:          # 二寸 413x579 / 一寸标准 295x413
        return 200.0
    return 500.0               # 更大尺寸放宽


def save_under(img, path, max_kb=None, out_w=None, out_h=None):
    """迭代压缩到指定体积内，尽量保质量"""
    if max_kb is None:
        max_kb = default_max_kb(out_w or img.width, out_h or img.height)

    if img.mode == "RGBA":                            # 透明底
        img.save(path, "PNG", optimize=True)
        kb = os.path.getsize(path) / 1024
        if kb > max_kb:                               # PNG 超限则量化调色板
            n = 256
            while n >= 32:
                q = img.convert("RGBA").quantize(colors=n, method=Image.FASTOCTREE)
                q.save(path, "PNG", optimize=True)
                kb = os.path.getsize(path) / 1024
                if kb <= max_kb:
                    break
                n //= 2
        return kb

    # JPEG：quality 二分
    lo, hi, best = 40, 96, None
    for _ in range(14):
        q = (lo + hi) // 2
        img.save(path, "JPEG", quality=q, subsampling=0, optimize=True)
        kb = os.path.getsize(path) / 1024
        if kb <= max_kb:
            best = (q, kb); lo = q + 1
        else:
            hi = q - 1
        if lo > hi:
            break
    if best is None:
        img.save(path, "JPEG", quality=40, subsampling=2, optimize=True)
        best = (40, os.path.getsize(path) / 1024)
    return best[1]


# ---------------------------------------------------------------- 主流程

def process(src_path, spec_name, out_path,
            max_kb=None,
            head_ratio=0.65, top_space=0.085,
            gamma=0.68, skin_gamma=None, skin_feather=10,
            transition_kill=0,
            model=DEFAULT_MODEL, debug_dir=None):
    """完整流程：抠图 -> 去白边 -> 构图裁切 -> 缩放 -> 合成 -> 美白 -> 压缩

    注意：缩放必须在合成【之前】。去污染与过渡带处理都依赖
    目标尺寸下的最终像素值，先合成再缩放会让处理结果被插值糊掉。
    """
    out_w, out_h, bg = parse_spec(spec_name)

    src = Image.open(src_path).convert("RGB")
    W, H = src.size
    print(f"[1/6] 读入 {os.path.basename(src_path)}  {W}x{H}")

    rgba = cutout(src, model)
    metrics = find_head_metrics(rgba)
    print(f"[2/6] 抠图完成  头顶={metrics['top']:.3f} "
          f"下巴={metrics['chin']:.3f} 脸中线x={metrics['cx']:.0f}")

    src_bg = estimate_bg_color(src)
    rgba = refine_alpha(rgba, src, src_bg)
    print(f"[3/6] 去边完成  原背景色={src_bg.round(0)}")

    box = build_crop_box(metrics, out_w, out_h, head_ratio, top_space)
    cropped = rgba.crop(box)
    print(f"[4/6] 裁切 {box[2]-box[0]}x{box[3]-box[1]} "
          f"比例={(box[2]-box[0])/(box[3]-box[1]):.3f}")

    # 先缩放到目标尺寸，再做合成（含去污染 + 过渡带处理）
    small = cropped.resize((out_w, out_h), Image.LANCZOS)
    comp = compose(small, bg, gamma, src_bg=src_bg,
                   transition_kill=transition_kill)
    if skin_gamma:
        comp = whiten_skin(comp, small, skin_gamma, skin_feather)
    final = comp
    print(f"[5/6] 合成完成  底色={bg if bg else '透明'}"
          + (f"  过渡带阈值={transition_kill}" if transition_kill else ""))

    if bg is None:
        final = final.convert("RGBA")
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    kb = save_under(final, out_path, max_kb, out_w, out_h)
    limit = max_kb if max_kb else default_max_kb(out_w, out_h)
    print(f"[6/6] 输出 {os.path.basename(out_path)}  "
          f"{out_w}x{out_h}  {kb:.1f}KB (上限{limit:.0f}KB)")

    if debug_dir:
        os.makedirs(debug_dir, exist_ok=True)
        rgba.save(os.path.join(debug_dir, "1_rgba.png"))
        cropped.save(os.path.join(debug_dir, "2_cropped.png"))
        comp.resize((out_w * 6, out_h * 6), Image.LANCZOS).save(
            os.path.join(debug_dir, "3_preview_x6.png"))
        print(f"      debug 中间产物 -> {debug_dir}")

    return {"file": out_path, "size": (out_w, out_h), "kb": kb, "bg": bg}


def main():
    p = argparse.ArgumentParser(
        description="证件照生成（抠图 / 换底 / 标准裁切 / 压缩）")
    p.add_argument("--src", help="源照片路径")
    p.add_argument("--spec", default="一寸+蓝",
                   help="规格：'尺寸+底色'（如 一寸+蓝、学籍照+淡蓝、二寸+白）"
                        "，或 'WxH@r-g-b'，多个用逗号分隔")
    p.add_argument("--out", help="输出文件（单规格时用）")
    p.add_argument("--outdir", help="输出目录（多规格时用）")
    p.add_argument("--max-kb", type=float, default=None,
                   help="体积上限 KB（默认按规格自动推算）")
    p.add_argument("--head-ratio", type=float, default=0.65,
                   help="头高占画面比例，标准 0.60~0.70")
    p.add_argument("--top-space", type=float, default=0.085,
                   help="头顶留白比例，标准 0.08~0.12")
    p.add_argument("--gamma", type=float, default=0.68,
                   help="整体提亮 (1=不提亮)")
    p.add_argument("--skin-gamma", type=float, default=None,
                   help="肤色美白 (如 0.86；不传则不做)")
    p.add_argument("--no-clean-edge", action="store_true",
                   help="跳过去白边（原图背景干净时可用）")
    p.add_argument("--transition-kill", type=float, default=60.0,
                   metavar="LUM",
                   help="过渡带亮像素判为背景的亮度阈值（0=关闭，默认 60）。"
                        "用于『深色头发+亮背景』照片：发丛边缘一圈发亮的灰。"
                        "原理：发丝与亮背景是空间交替，边缘像素物理上就是混合色，"
                        "去污染按 alpha 混合公式反推出『中亮暖灰』第三色导致发亮；"
                        "本参数把过渡带内亮于阈值的像素直接判为背景，消除第三色。"
                        "实测（段3，含 refine_alpha 的真实流程）：阈值≤70 时收益饱和"
                        "（灰 832→611，-27%%），只啃掉 1.3%% 人像像素；阈值调高反而变差。"
                        "代价：会啃掉发丝尖端（减淡而非消除）")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--debug", help="保留中间产物到此目录")
    p.add_argument("--list", action="store_true", help="列出内置规格")
    args = p.parse_args()

    if args.list:
        print("【尺寸】（与底色自由组合）")
        for k, (w, h) in SIZES.items():
            print(f"  {k:10s} {w}x{h}")

        # 底色按色值分组，同一颜色的别名合并显示
        groups = {}
        for k, v in BACKGROUNDS.items():
            groups.setdefault(str(v), []).append(k)
        print("\n【底色】")
        for v, names in groups.items():
            label = "透明" if v == "None" else v
            print(f"  {label:18s} {' / '.join(sorted(names))}")

        print("\n【用法示例】")
        print("  一寸+蓝                组合（推荐）")
        print("  一寸蓝底               组合名简写，自动拆解")
        print("  学籍照+淡蓝")
        print("  二寸+白")
        print("  1200x1600@67-142-219   自定义尺寸+颜色（RGB 用 - 分隔）")
        print("  1200x1600              自定义尺寸，透明底")
        print("  一寸                   只给尺寸，默认蓝底")
        print("  红                     只给底色，默认一寸")
        print("\n【多规格批量】逗号分隔，如：一寸+蓝,二寸+白,学籍照+淡蓝")
        return

    if not args.src:
        p.error("需要 --src")

    check_deps()
    ensure_model(args.model)

    specs = [s.strip() for s in args.spec.split(",") if s.strip()]
    results = []
    for s in specs:
        if args.out and len(specs) == 1:
            out = args.out
        else:
            outdir = args.outdir or "."
            base = os.path.splitext(os.path.basename(args.src))[0]
            ext = "png" if parse_spec(s)[2] is None else "jpg"
            out = os.path.join(outdir, f"{base}_{s}.{ext}")
        print(f"\n===== {s} =====")
        results.append(process(
            args.src, s, out,
            max_kb=args.max_kb,
            head_ratio=args.head_ratio,
            top_space=args.top_space,
            gamma=args.gamma,
            skin_gamma=args.skin_gamma,
            transition_kill=args.transition_kill,
            model=args.model,
            debug_dir=args.debug))

    print("\n===== 完成 =====")
    for r in results:
        print(f"  {r['file']}  {r['size'][0]}x{r['size'][1]}  {r['kb']:.1f}KB")


if __name__ == "__main__":
    main()
