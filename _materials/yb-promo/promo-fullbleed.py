"""Акции ЯБ, формат v3 «full-bleed»: фото на весь холст 1800×960 (мин. поля
ЯБ 900×480), слева брендовый градиент, текст поверх. Ни одного пустого поля."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import sys
S = Path(__file__).parent
FONT = str(S/"fonts/Manrope-var.ttf")
def font(size, weight):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([weight]); return f
W,H=1800,960
NAVY=(26,38,56); BLUE=(30,95,179); GOLD=(245,166,35)
logo = Image.open("/home/user/Angel-Dent-site/assets/img/logo.png").convert("RGBA")

def make(out, photo_path, crop, badge, title_lines, big, sub_lines,
         old_price=None, grad_end=1060, title_size=88):
    photo=Image.open(S/photo_path).convert("RGB")
    ph=photo.crop(crop).resize((W,H),Image.LANCZOS)
    img=ph.convert("RGBA")

    # градиент: глубокий сине-графитовый слева -> прозрачный
    grad=Image.new("L",(W,1),0)
    gd=ImageDraw.Draw(grad)
    for x in range(W):
        if x<600: a=int(242-42*(x/600))          # 242 -> 200
        elif x<grad_end: a=int(200*(1-(x-600)/(grad_end-600)))
        else: a=0
        gd.point((x,0),fill=a)
    grad=grad.resize((W,H))
    tint=Image.new("RGBA",(W,H),(21,38,66,0))    # тёмно-синий бренд
    tint.putalpha(grad)
    img=Image.alpha_composite(img,tint)
    d=ImageDraw.Draw(img)
    ML=72
    # бренд-строка: лого на белом чипе
    chip=96
    d.rounded_rectangle([ML,52,ML+chip,52+chip],radius=26,fill=(255,255,255,255))
    ls=logo.resize((chip-20,chip-20),Image.LANCZOS)
    img.paste(ls,(ML+10,62),ls)
    d=ImageDraw.Draw(img)
    d.text((ML+chip+26,58),"АНГЕЛ-ДЕНТ",font=font(40,800),fill=(255,255,255))
    d.text((ML+chip+26,106),"Стоматология · Реутов",font=font(29,600),fill=(176,198,228))
    # бейдж
    f_b=font(48,800)
    btxt=badge
    bw=d.textlength(btxt,font=f_b); bb=d.textbbox((0,0),btxt,font=f_b)
    by0=224; bh=94
    d.rounded_rectangle([ML,by0,ML+bw+84,by0+bh],radius=47,fill=GOLD)
    d.text((ML+42,by0+(bh-(bb[3]-bb[1]))//2-bb[1]),btxt,font=f_b,fill=(46,32,4))
    # заголовок
    ty=372
    for t in title_lines:
        d.text((ML,ty),t,font=font(title_size,800),fill=(255,255,255)); ty+=title_size+14
    # цена — золотом
    ty+=24
    f_big=font(148,800)
    d.text((ML,ty),big,font=f_big,fill=GOLD)
    if old_price:
        f_old=font(58,600)
        ow=d.textlength(old_price,font=f_old)
        ox,oy=ML+d.textlength(big,font=f_big)+42,ty+70
        d.text((ox,oy),old_price,font=f_old,fill=(198,210,226))
        d.line([ox-5,oy+40,ox+ow+5,oy+40],fill=(198,210,226),width=6)
    ty+=192
    for t in sub_lines:
        d.text((ML,ty),t,font=font(42,600),fill=(214,226,240)); ty+=58
    # дисклеймер
    d.text((ML,898),"Имеются противопоказания, необходима консультация специалиста",
           font=font(26,500),fill=(160,176,196))
    img.convert("RGB").save(S/out,"JPEG",quality=90,optimize=True)
    print("built",out)

CARDS={
 "kt": dict(out="yb-akcia-f1-kt-plan.jpg", photo_path="akcia-wide3-clean.png",
      crop=(0,90,1688,990),
      badge="−44%", title_lines=["КТ + план лечения"], big="4 200 ₽", old_price="7 500 ₽",
      sub_lines=["Снимок, осмотр главврача и план","с фиксированными ценами"]),

 "aw": dict(out="yb-akcia-f2-amazing-white.jpg", photo_path="akcia-aw-clean.png",
      crop=(0,90,1688,990),
      badge="−30%", title_lines=["Отбеливание","Amazing White"], big="17 500 ₽", old_price="25 000 ₽",
      sub_lines=["Обе челюсти «под ключ» за один визит"]),

 "implant": dict(out="yb-akcia-f3-implant.jpg", photo_path="akcia-implant-clean.png",
      crop=(0,55,1740,983),
      badge="Акция", title_lines=["Каждый 3-й имплант"], big="в подарок",
      sub_lines=["При установке нескольких имплантатов","Гарантия 10 лет"]),

 "gift": dict(out="yb-akcia-f4-chistka.jpg", photo_path="akcia-gift2.png",
      crop=(0,30,2048,1122),
      badge="Акция", title_lines=["Чистка в подарок"], big="0 ₽", old_price="5 000 ₽",
      sub_lines=["Профгигиена при договоре на","имплантацию или брекеты"]),

 "orto": dict(out="yb-akcia-f5-ortodont.jpg", photo_path="akcia-orto-clean.png",
      crop=(0,30,2048,1122),
      badge="0 ₽", title_lines=["Консультация","ортодонта"], big="бесплатно",
      sub_lines=["С расчётом ТРГ. Выбор брекетов или элайнеров"]),

 "lgoty": dict(out="yb-akcia-f6-lgoty.jpg", photo_path="akcia-lgoty2.png",
      crop=(0,30,2048,1122), title_size=72,
      badge="Льготы", title_lines=["Пенсионерам,","многодетным, военным"], big="−10%",
      sub_lines=["На лечение, протезирование","и гигиену — постоянно"]),

 "family": dict(out="yb-akcia-f7-family.jpg", photo_path="akcia-family-clean.png",
      crop=(234,54,1905,945), title_size=80,
      badge="Семьям", title_lines=["Семейная программа"], big="до −10%",
      sub_lines=["Скидка всем членам семьи","при лечении от 3 человек"]),
}
keys=sys.argv[1:] or list(CARDS)
for k in keys: make(**CARDS[k])
