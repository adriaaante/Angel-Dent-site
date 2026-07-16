"""Карточки акций для Яндекс.Бизнеса (1200x1200) в бренд-стиле Angel-Dent.

Состав и цены = promotions.html (источник правды — сайт). Фото-исходники
генерятся в Higgsfield (soul_2, славянская внешность, "no text, no logos")
и лежат в scratchpad сессии; при перегенерации карточки достаточно любого
подходящего фото 1152x2048 — путь указывается в CARDS. Шрифт Manrope-var.ttf
(github google/fonts). Готовые JPG заливаются в Higgsfield storage
(media_upload -> curl PUT -> media_confirm), ссылки — в google-doc
"Акции ЯБ — карточки и инструкция" на Drive владельца.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
S = Path(__file__).parent
FONT = str(S/"fonts/Manrope-var.ttf")
def font(size, weight):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([weight]); return f
W,H=1200,1200
NAVY=(26,38,56); BLUE=(30,95,179); MUT=(64,83,110); GOLD=(245,166,35); BG=(234,242,252)
logo = Image.open("/home/user/Angel-Dent-site/assets/img/logo.png").convert("RGBA")

PANEL_X=660  # photo panel occupies x 660..1200
PANEL_W=W-PANEL_X

def feather_blur(photo, box, blur=14):
    x0,y0,x1,y1=box
    region=photo.crop(box).filter(ImageFilter.GaussianBlur(blur))
    m=Image.new("L",region.size,0)
    ImageDraw.Draw(m).rounded_rectangle([6,6,region.size[0]-6,region.size[1]-6],radius=20,fill=255)
    m=m.filter(ImageFilter.GaussianBlur(10))
    photo.paste(region,(x0,y0),m)

def make_card(out, photo_path, crop_x0, crop_y0, badge, title_lines, big, sub_lines,
              old_price=None, patches=None, zoom_w=None):
    photo=Image.open(photo_path).convert("RGB")
    if patches:
        for box in patches: feather_blur(photo,box)
    pw,ph=photo.size
    ratio=PANEL_W/H
    if zoom_w:
        cw=zoom_w; ch=int(cw/ratio)
        x0=max(0,min(pw-cw,crop_x0)); y0=max(0,min(ph-ch,crop_y0))
        crop=photo.crop((x0,y0,x0+cw,y0+ch)).resize((PANEL_W,H),Image.LANCZOS)
        return finish(out,crop,badge,title_lines,big,sub_lines,old_price)
    cw=int(ph*ratio) if pw/ph>ratio else pw
    ch=int(cw/ratio)
    if ch>ph: ch=ph; cw=int(ch*ratio)
    x0=max(0,min(pw-cw,crop_x0)); y0=max(0,min(ph-ch,crop_y0))
    crop=photo.crop((x0,y0,x0+cw,y0+ch)).resize((PANEL_W,H),Image.LANCZOS)
    return finish(out,crop,badge,title_lines,big,sub_lines,old_price)

def finish(out,crop,badge,title_lines,big,sub_lines,old_price):
    img=Image.new("RGBA",(W,H),BG+(255,))
    d=ImageDraw.Draw(img)
    d.ellipse([-260,900,340,1500],fill=(219,232,248,255))
    # photo panel with left fade
    fade=Image.new("L",(PANEL_W,H),255)
    fd=ImageDraw.Draw(fade)
    for x in range(140):
        fd.line([(x,0),(x,H)],fill=int(255*x/140))
    img.paste(crop,(PANEL_X,0),fade)
    d=ImageDraw.Draw(img)
    # brand row
    lh=84; ls=logo.resize((lh,lh),Image.LANCZOS); img.paste(ls,(56,52),ls)
    d=ImageDraw.Draw(img)
    d.text((160,58),"АНГЕЛ-ДЕНТ",font=font(38,800),fill=NAVY)
    d.text((160,102),"Стоматология · Реутов",font=font(28,600),fill=MUT)
    # gold badge
    f_b=font(40,800)
    bw=d.textlength(badge,font=f_b)
    bb=d.textbbox((0,0),badge,font=f_b)
    bx0,by0,bh=56,220,86
    d.rounded_rectangle([bx0,by0,bx0+bw+72,by0+bh],radius=43,fill=GOLD)
    d.text((bx0+36,by0+(bh-(bb[3]-bb[1]))//2-bb[1]),badge,font=f_b,fill=(46,32,4))
    # title
    ty=356
    for t in title_lines:
        d.text((56,ty),t,font=font(64,800),fill=NAVY); ty+=76
    # big benefit
    ty+=28
    f_big=font(104,800)
    d.text((56,ty),big,font=f_big,fill=BLUE)
    if old_price:
        f_old=font(46,600)
        ow=d.textlength(old_price,font=f_old)
        ox,oy=56+d.textlength(big,font=f_big)+30,ty+44
        d.text((ox,oy),old_price,font=f_old,fill=(140,152,170))
        d.line([ox-4,oy+30,ox+ow+4,oy+30],fill=(140,152,170),width=5)
    ty+=140
    for t in sub_lines:
        d.text((56,ty),t,font=font(37,600),fill=MUT); ty+=52
    # disclaimer
    d.text((56,1082),"Имеются противопоказания,",font=font(26,500),fill=(130,144,166))
    d.text((56,1118),"необходима консультация специалиста",font=font(26,500),fill=(130,144,166))
    img.convert("RGB").save(S/out,"JPEG",quality=90,optimize=True)
    print("built",out)

CARDS=[
 dict(out="yb-promo-1-kt-plan.jpg", photo_path=S/"story2-cta-photo.png", crop_x0=189, crop_y0=60,
      badge="−44%", title_lines=["КТ + план","лечения"], big="4 200 ₽", old_price="7 500 ₽",
      sub_lines=["Снимок, осмотр главврача,","план с фиксированными ценами.","При договоре — бесплатно"],
      patches=[(560,1430,820,1580)]),
 dict(out="yb-promo-2-amazing-white.jpg", photo_path=S/"story10-cta-photo.png", crop_x0=189, crop_y0=60,
      badge="−30%", title_lines=["Отбеливание","Amazing White"], big="17 500 ₽", old_price="25 000 ₽",
      sub_lines=["Обе челюсти «под ключ»","за один визит"],
      patches=[(600,355,780,450)]),
 dict(out="yb-promo-3-implant.jpg", photo_path=S/"implant-macro.png", crop_x0=678, crop_y0=0,
      badge="Подарок", title_lines=["Каждый 3-й","имплант"], big="в подарок", old_price=None,
      sub_lines=["При установке нескольких","имплантатов. Гарантия 10 лет"],
      patches=None),
 dict(out="yb-promo-4-chistka.jpg", photo_path=S/"promo-gift.png", crop_x0=189, crop_y0=100,
      badge="Подарок", title_lines=["Чистка","в подарок"], big="0 ₽", old_price="5 000 ₽",
      sub_lines=["Профгигиена при договоре на","имплантацию или брекеты"],
      patches=None),
 dict(out="yb-promo-5-ortodont.jpg", photo_path=S/"story7-cover-photo.png", crop_x0=189, crop_y0=328,
      badge="0 ₽", title_lines=["Консультация","ортодонта"], big="бесплатно", old_price=None,
      sub_lines=["С расчётом ТРГ. Поможем","выбрать брекеты или элайнеры"],
      patches=None),
 dict(out="yb-promo-6-lgoty.jpg", photo_path=S/"promo-seniors.png", crop_x0=290, crop_y0=60,
      badge="Скидка", title_lines=["Пенсионерам,","многодетным,","военным"], big="−10%", old_price=None,
      sub_lines=["На лечение, протезирование","и гигиену — постоянно"],
      patches=[(190,1060,360,1300),(460,1050,620,1240)]),
 dict(out="yb-promo-7-family.jpg", photo_path=S/"promo-family.png", crop_x0=180, crop_y0=493, zoom_w=700,
      badge="Семьям", title_lines=["Семейная","программа"], big="до −10%", old_price=None,
      sub_lines=["Скидка всем членам семьи","при лечении от 3 человек"],
      patches=None),
]
for c in CARDS: make_card(**c)
