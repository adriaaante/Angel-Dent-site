"""Картинки публикаций (постов) ЯБ: full-bleed 1800×960 в бренд-стиле,
но без цен — заголовок + подзаголовок + бренд-чип (посты = контент)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys
S = Path(__file__).parent
FONT = str(S/"fonts/Manrope-var.ttf")
def font(size, weight):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([weight]); return f
W,H=1800,960
GOLD=(245,166,35)
logo = Image.open("/home/user/Angel-Dent-site/assets/img/logo.png").convert("RGBA")

def make(out, photo_path, crop, title_lines, sub, grad_end=1060, title_size=92):
    photo=Image.open(S/photo_path).convert("RGB")
    ph=photo.crop(crop).resize((W,H),Image.LANCZOS)
    img=ph.convert("RGBA")
    grad=Image.new("L",(W,1),0)
    gd=ImageDraw.Draw(grad)
    for x in range(W):
        if x<600: a=int(230-40*(x/600))
        elif x<grad_end: a=int(190*(1-(x-600)/(grad_end-600)))
        else: a=0
        gd.point((x,0),fill=a)
    grad=grad.resize((W,H))
    tint=Image.new("RGBA",(W,H),(21,38,66,0))
    tint.putalpha(grad)
    img=Image.alpha_composite(img,tint)
    d=ImageDraw.Draw(img)
    ML=72
    chip=96
    d.rounded_rectangle([ML,64,ML+chip,64+chip],radius=26,fill=(255,255,255,255))
    ls=logo.resize((chip-20,chip-20),Image.LANCZOS)
    img.paste(ls,(ML+10,74),ls)
    d=ImageDraw.Draw(img)
    d.text((ML+chip+26,70),"АНГЕЛ-ДЕНТ",font=font(40,800),fill=(255,255,255))
    d.text((ML+chip+26,118),"Стоматология · Реутов",font=font(29,600),fill=(176,198,228))
    # заголовок по вертикальному центру
    n=len(title_lines)
    block=n*(title_size+16)+70
    ty=(H-block)//2+40
    for t in title_lines:
        d.text((ML,ty),t,font=font(title_size,800),fill=(255,255,255)); ty+=title_size+16
    ty+=18
    d.text((ML,ty),sub,font=font(44,600),fill=GOLD)
    img.convert("RGB").save(S/out,"JPEG",quality=90,optimize=True)
    print("built",out)

POSTS={
 "kids": dict(out="yb-post-1-detskaya.jpg", photo_path="post-kids.png", crop=(0,30,2048,1122),
      title_lines=["Детям — без слёз"], sub="Первый визит — как игра"),
 "visit": dict(out="yb-post-2-perviy-vizit.jpg", photo_path="post-visit-clean.png", crop=(0,30,2048,1122),
      title_lines=["Первый визит","без страха"], sub="Знакомство, осмотр и план"),
 "gigiena": dict(out="yb-post-3-gigiena.jpg", photo_path="post-gigiena-clean.png", crop=(0,30,2048,1122),
      title_lines=["Чистка раз","в полгода"], sub="Профилактика дешевле лечения"),
 "implant": dict(out="yb-post-4-implantaciya.jpg", photo_path="post-implant-clean.png", crop=(0,30,2048,1122),
      title_lines=["Имплантация","под ключ"], sub="Гарантия 10 лет"),
 "smile": dict(out="yb-post-5-esthetika.jpg", photo_path="post-smile.png", crop=(0,30,2048,1122),
      title_lines=["Улыбка мечты"], sub="Виниры и отбеливание"),
 "orto": dict(out="yb-post-6-ortodontiya.jpg", photo_path="post-orto-clean.png", crop=(0,18,2048,1110),
      title_lines=["Брекеты","или элайнеры?"], sub="Подберём бесплатно на консультации"),
}
keys=sys.argv[1:] or list(POSTS)
for k in keys: make(**POSTS[k])
