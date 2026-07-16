from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
S = Path(__file__).parent
OUT = 1200

WM = Image.open("/home/user/Angel-Dent-site/assets/img/watermark.png").convert("RGBA")
WM_RATIO, WM_MARGIN, WM_OP, SH_OP, SH_BLUR = 0.32, 0.03, 0.78, 0.55, 0.014

def watermark(img):
    tw = int(img.width * WM_RATIO)
    scale = tw / WM.width
    th = int(WM.height * scale)
    wm = WM.resize((tw, th), Image.LANCZOS)
    a = wm.split()[3].point(lambda p: int(p * WM_OP))
    wm.putalpha(a)
    m = int(img.width * WM_MARGIN)
    pos = (img.width - tw - m, img.height - th - m)
    br = max(2, int(tw * SH_BLUR)); pad = br * 4
    sa = wm.split()[3].point(lambda p: int(p * SH_OP))
    sh = Image.new("RGBA", (tw + pad*2, th + pad*2), (0,0,0,0))
    sh.paste(Image.new("RGBA", wm.size, (0,0,0,255)), (pad,pad), sa)
    sh = sh.filter(ImageFilter.GaussianBlur(br))
    layer = Image.new("RGBA", img.size, (0,0,0,0))
    layer.paste(sh, (pos[0]-pad, pos[1]-pad), sh)
    layer.paste(wm, pos, wm)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

def feather_blur(photo, box, blur=34):
    region = photo.crop(box).filter(ImageFilter.GaussianBlur(blur))
    m = Image.new("L", region.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([6,6,region.size[0]-6,region.size[1]-6], radius=24, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(12))
    photo.paste(region, (box[0], box[1]), m)

def build(src, out, crop=None, patches=None):
    img = Image.open(S/src).convert("RGB")
    if patches:
        for b in patches: feather_blur(img, b)
    if crop:
        img = img.crop(crop)
    else:
        side = min(img.size)
        x0 = (img.width - side)//2; y0 = (img.height - side)//2
        img = img.crop((x0, y0, x0+side, y0+side))
    img = img.resize((OUT, OUT), Image.LANCZOS)
    watermark(img).save(S/out, "JPEG", quality=90, optimize=True)
    print("built", out)

ITEMS = [
    ("vit-airflow.png",      "yb-vitrina-01-chistka.jpg",      None, None),
    ("vit-mirror.png",       "yb-vitrina-02-karies.jpg",       None, None),  # v2: реалистичный осмотр (vit-mirror.png перезаписан новым фото)
    ("vit-ct.png",           "yb-vitrina-03-kt.jpg",           None, None),
    ("vit-smile.png",        "yb-vitrina-04-otbelivanie.jpg",  None, None),
    ("vit-veneers.png",      "yb-vitrina-05-viniry.jpg",       None, None),
    ("story7-cover-photo.png","yb-vitrina-06-ortodont.jpg",    (0, 896, 1152, 2048), None),
    ("vit-braces.png",       "yb-vitrina-07-brekety.jpg",      None, None),
    ("story9-cover-photo.png","yb-vitrina-08-detskiy.jpg",     (0, 500, 1152, 1652), None),
    ("vit-surgical.png",     "yb-vitrina-09-udalenie.jpg",     None, [(490, 700, 1350, 1030)]),
    ("vit-gums-fixed.png",   "yb-vitrina-10-desny.jpg",        None, None),
    ("implant-macro.png",    "yb-vitrina-11-implant.jpg",      (255, 0, 1791, 1536), None),
    ("vit-implantmodel.png", "yb-vitrina-12-implant-kluch.jpg",None, [(560, 230, 900, 450)]),
    ("vit-crowns.png",       "yb-vitrina-13-protez.jpg",       None, None),
]
for src, out, crop, patches in ITEMS:
    build(src, out, crop, patches)
