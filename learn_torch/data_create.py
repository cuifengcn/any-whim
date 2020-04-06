# 创建定位训练的数据集脚本，该脚本会生成三种颜色的色块用于分类定位

import os, time, random

import cv2
import numpy as np

class Data:
    def __init__(   self, 
                    path = 'train_img',
                    minw = 416,
                    minh = 416,
                    maxw = 416,
                    maxh = 416,
                    channel = 3,
                    randomrect = (50,200,50,200), # minw,maxw,minh,maxh
                    randomcolor = {
                        'blue':  [255,0,0],
                        'red':   [0,0,255],
                        'green': [0,255,0],
                    },
                    bgcolor = [230,230,230],
                ):
        self.imgpath = os.path.join(path, 'imgfile')
        self.xmlpath = os.path.join(path, 'xmlpath')
        if not os.path.isdir(self.imgpath): os.makedirs(self.imgpath)
        if not os.path.isdir(self.xmlpath): os.makedirs(self.xmlpath)
        self.minw = minw
        self.minh = minh
        self.maxw = maxw
        self.maxh = maxh
        self.channel = channel
        self.rangew = list(range(self.minw, self.maxw+1))
        self.rangeh = list(range(self.minh, self.maxh+1))
        self.randomw = list(range(randomrect[0], randomrect[1]+1))
        self.randomh = list(range(randomrect[2], randomrect[3]+1))
        self.color = randomcolor
        self.bgcolor = np.array(bgcolor)

        self.img_id = 0
        self.stamp = time.strftime("%Y%m%d", time.localtime())

    def make_img(self,):
        w = random.choice(self.rangew)
        h = random.choice(self.rangeh)
        img = np.ones((w, h, self.channel))
        img = img[:,:] * self.bgcolor
        return img, w, h

    def create_img(self,):
        w = random.choice(self.randomw)
        h = random.choice(self.randomh)
        img, iw, ih = self.make_img()
        x = random.choice(list(range(iw-w)))
        y = random.choice(list(range(ih-h)))
        c = random.choice(list(self.color))
        minx = x
        miny = y
        maxx = x+w
        maxy = y+h
        img[minx:maxx, miny:maxy] = self.color[c]
        folder = 'imgfile'
        filename, xmlname = self.create_name()
        realimgpath = os.path.join(self.imgpath, filename)
        realxmlpath = os.path.join(self.xmlpath, xmlname)
        xml = self.mkxml(folder,filename,realimgpath,iw,ih,self.channel,c,minx,miny,maxx,maxy)
        cv2.imwrite(realimgpath, img)
        with open(realxmlpath, 'w', encoding='utf-8') as f:
            f.write(xml)
        return realimgpath

    def create_imgs(self, number):
        for _ in range(number):
            self.create_img()

    def create_name(self,):
        imgname = '{}_{:>05}.png'.format(self.stamp, self.img_id)
        xmlname = '{}_{:>05}.xml'.format(self.stamp, self.img_id)
        self.img_id += 1
        return imgname, xmlname

    def mkxml(self,folder,filename,realpath,w,h,channel,clazz,minx,miny,maxx,maxy):
        # 保存为 python第三方库 labelImg 所标注的数据的结构信息
        # 这样会方便于快速将虚拟数据的使用切换到实际数据的使用
        return r'''
<annotation>
    <folder>{}</folder>
    <filename>{}</filename>
    <path>{}</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
        <width>{}</width>
        <height>{}</height>
        <depth>{}</depth>
    </size>
    <segmented>0</segmented>
    <object>
        <name>{}</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{}</xmin>
            <ymin>{}</ymin>
            <xmax>{}</xmax>
            <ymax>{}</ymax>
        </bndbox>
    </object>
</annotation>
'''.format(folder,filename,realpath,w,h,channel,clazz,minx,miny,maxx,maxy).strip()



def drawrect_and_show(imgfile, rect, text):# 只能写英文
    img = cv2.imread(imgfile)
    cv2.rectangle(img, rect[:2], rect[2:], (10,10,10), 1, 1)
    x, y = rect[:2]
    cv2.putText(img, text, (x,y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10,10,10), 1)
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def readxml(file, islist=False):
    # 读取 xml 文件，根据其中的内容读取图片数据，并且获取标注信息
    # 该类 xml 文件为 python第三方库 labelImg 所标注的数据的结构信息
    # file：
    #   xml文件的路径地址
    # islist：
    #   xml 文件是否包含多个标注，如果有，统一返回列表，
    #   如果只有一个标注，直接返回一个信息字典方便使用
    d = xml.dom.minidom.parse(file)
    v = d.getElementsByTagName('annotation')[0]
    f = v.getElementsByTagName('path')[0].firstChild.data
    if not os.path.isfile(f):
        raise 'fail load img: {}'.format(f)
    size = v.getElementsByTagName('size')[0]
    npimg = cv2.imread(f)
    def readobj(obj):
        d = {}
        obj  = v.getElementsByTagName('object')[0]
        bbox = obj.getElementsByTagName('bndbox')[0]
        d['width']  = int(size.getElementsByTagName('width')[0].firstChild.data)
        d['height'] = int(size.getElementsByTagName('height')[0].firstChild.data)
        d['depth']  = int(size.getElementsByTagName('depth')[0].firstChild.data)
        d['cate']   = obj.getElementsByTagName('name')[0].firstChild.data
        d['xmin']   = int(bbox.getElementsByTagName('xmin')[0].firstChild.data)
        d['ymin']   = int(bbox.getElementsByTagName('ymin')[0].firstChild.data)
        d['xmax']   = int(bbox.getElementsByTagName('xmax')[0].firstChild.data)
        d['ymax']   = int(bbox.getElementsByTagName('ymax')[0].firstChild.data)
        d['centerx'] = (d['xmin'] + d['xmax'])/2.
        d['centery'] = (d['ymin'] + d['ymax'])/2.
        d['numpy']  = npimg
        return d
    if islist:  r = [readobj(obj) for obj in v.getElementsByTagName('object')]
    else:       r = readobj(v.getElementsByTagName('object')[0])
    return r



if __name__ == '__main__':
    d = Data()
    for i in range(2):
        img = d.create_img()
    drawrect_and_show(img, (20,20,100,100), 'hello world.')

    s = time.time()
    d.create_imgs(100)
    print(time.time() - s)