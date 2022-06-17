# python3 
# pip install ddddocr

from io import BytesIO
import ddddocr
from PIL import Image, ImageDraw, ImageFont

clz_ocr = ddddocr.DdddOcr(show_ad=False)
loc_ocr = ddddocr.DdddOcr(det=True, show_ad=False)

def cut_img_from_bytes(img_bytes, cut_size=None):
    img = Image.open(BytesIO(img_bytes))
    if cut_size:
        img = img.crop(cut_size)
        byt = BytesIO()
        img.save(byt, 'png')
        img_bytes = byt.getvalue()
    return img_bytes

def get_loc_words(img_bytes, cut_size=None):
    img_bytes = cut_img_from_bytes(img_bytes, cut_size)
    loc_list = loc_ocr.detection(img_bytes)
    ret = {}
    dimg = Image.open(BytesIO(img_bytes))
    for loc in loc_list:
        cut = dimg.crop(loc)
        byt = BytesIO()
        cut.save(byt, 'png')
        word = clz_ocr.classification(byt.getvalue())
        ret[word] = int((loc[0] + loc[2]) / 2), int((loc[1] + loc[3]) / 2)
    return ret

with open(r'./67aa614e93c6432fae4af80d5119d251.jpg', 'rb') as f:
    img_bytes = f.read()

v = get_loc_words(img_bytes, (0, 0, 344, 344))
print(v)








# 展示用测试

def test(img_bytes, cut_size=None):
    img_bytes = cut_img_from_bytes(img_bytes, cut_size)
    loc_list = loc_ocr.detection(img_bytes)
    font_type = "./simsun.ttc"
    font_size = 20
    font = ImageFont.truetype(font_type, font_size)
    dimg = Image.open(BytesIO(img_bytes))
    draw = ImageDraw.Draw(dimg)
    for loc in loc_list:
        x1, y1, x2, y2 = loc
        cut = dimg.crop(loc)
        byt = BytesIO()
        cut.save(byt, 'png')
        word = clz_ocr.classification(byt.getvalue())
        draw.line(([(x1, y1), (x1, y2), (x2, y2), (x2, y1), (x1, y1)]), width=1, fill="white")
        hloc = y1 - 30 if y2 > 300 else y2
        draw.text((int((x1 + x2)/2), hloc), word, font=font, fill="white")
    dimg.show()

test(img_bytes, (0, 0, 344, 344))