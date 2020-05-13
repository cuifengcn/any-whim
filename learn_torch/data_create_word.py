import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def cv2ImgAddText(img, text, padding=10, rotate=0, bgColor=(0,0,0), textColor=(0, 255, 0), font='simsun.ttc', textSize=20):
    font = ImageFont.truetype(font, textSize, encoding="utf-8")
    size = tuple(map(lambda i:i+padding, font.getsize('哈')))
    if img is None:
        img = Image.new("RGB", size)
    else:
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, *size), fill=bgColor)
    draw.text((padding//2, padding//2), text, textColor, font=font)
    help(draw.text)
    img = cv2.cvtColor(np.asarray(img.rotate(rotate)), cv2.COLOR_RGB2BGR)
    return img

words = ['你', '好']
fonts = ['simsun.ttc']
colors = [(255,0,0), (0,255,0), (0,0,255)]
bgcolors = [(255,255,255)]
rotates = range(0,360,30)
paddings = [30, 15, 0]

for word in words:
    for font in fonts:
        for color in colors:
            for bgcolor in bgcolors:
                for rotate in rotates:
                    for padding in paddings:
                        img = cv2ImgAddText(None, word, padding=padding, rotate=rotate, bgColor=bgcolor, textColor=color, font=font)
                        name = '{}_{:>02}_{}_{}_{}_{}.jpg'.format(word,padding,rotate,bgcolor,color,font,)
                        cv2.imshow('test', img)
                        cv2.imencode('.jpg', img)[1].tofile(name) # cv2.imwrite 保存中文路径存在问题，需要这样保存文件
                        cv2.waitKey(0)