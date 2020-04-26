# 这部分的代码接近能用了，不过暂时还在调整当中
# 至少在无限训练一张图片的时候能够收敛了！使用的 backbone 网络非常粗暴。
# 目前仅考虑小图定位的处理。后续按需求扩展。
# 需要配合标注工具使用

# 开发于 python3，仅需要下面两个第三方依赖，训练的数据为 labelimg 标注型的数据。
# 依赖 pytorch：（官网找安装方式）开发使用版本为 torch-1.4.0-cp36-cp36m-win_amd64.whl
# 依赖 opencv： （pip install opencv-contrib-python==3.4.1.15）
#     其实这里的 opencv 版本不重要，py3能用就行，只是个人喜欢这个版本，因为能用sift图像检测，稳。






# 下面的 readxml 函数是用的 python 自带的库实现加载 labelimg 的数据，降低了第三方依赖度
# 生成的数据将会自动进行相关的标签处理，所以算是一种对类似格式数据加载的一种定制化处理。
# 后续如果需要使用新的数据，就尽量使用 labelimg 标注的数据
# 目前只是一次训练即可保存模型，加载模型即刻测试当前数据集的部分数据。
# 后续将增强处理的功能。可能增加部分多分类处理的部分。
# 或许增加试试查看误差的折线图之类的处理？
# 另外在加载网络结构的时候注意需要 net.eval() 否则结果可能不准。（已经包含于以下代码中）






import cv2
import numpy as np
import torch

import os
import math
import xml.dom.minidom
from collections import OrderedDict

def readxml(file, islist=False):
    # 读取 xml 文件，根据其中的内容读取图片数据，并且获取标注信息
    # 该类 xml 文件为 python第三方库 labelImg 所标注的数据的结构信息
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
    npimg = cv2.cvtColor(npimg, cv2.COLOR_BGR2RGB) # [y,x,c]
    npimg = cv2.resize(npimg, (416, 416))
    npimg_ = np.transpose(npimg, (2,1,0)) # [c,x,y]
    def readobj(obj):
        d = {}
        obj  = v.getElementsByTagName('object')[0]
        bbox = obj.getElementsByTagName('bndbox')[0]
        d['width']  = int(size.getElementsByTagName('width')[0].firstChild.data)
        d['height'] = int(size.getElementsByTagName('height')[0].firstChild.data)
        d['ratew']  = rw = d['width']/416
        d['rateh']  = rh = d['height']/416
        d['depth']  = int(size.getElementsByTagName('depth')[0].firstChild.data)
        d['cate']   = obj.getElementsByTagName('name')[0].firstChild.data
        d['xmin']   = int(bbox.getElementsByTagName('xmin')[0].firstChild.data)/rw
        d['ymin']   = int(bbox.getElementsByTagName('ymin')[0].firstChild.data)/rh
        d['xmax']   = int(bbox.getElementsByTagName('xmax')[0].firstChild.data)/rw
        d['ymax']   = int(bbox.getElementsByTagName('ymax')[0].firstChild.data)/rh
        d['w']      = d['xmax'] - d['xmin']
        d['h']      = d['ymax'] - d['ymin']
        d['rect']   = d['xmin'],d['ymin'],d['xmax'],d['ymax']
        d['centerx'] = (d['xmin'] + d['xmax'])/2.
        d['centery'] = (d['ymin'] + d['ymax'])/2.
        d['numpy']  = npimg_
        d['file'] = f
        return d
    if islist:  r = [readobj(obj) for obj in v.getElementsByTagName('object')]
    else:       r = readobj(v.getElementsByTagName('object')[0])
    return r

def make_y_true(imginfo, S, anchors, class_types):
    cx = imginfo['centerx']
    cy = imginfo['centery']
    bw = imginfo['w']
    bh = imginfo['h']
    gap = int(416/S)
    ww = list(range(416))[::int(gap)]
    for wi in range(len(ww)):
        if ww[wi] > cx: 
            break
    hh = list(range(416))[::int(gap)]
    for hi in range(len(hh)):
        if hh[hi] > cy: 
            break
    wi, hi = wi - 1, hi - 1
    sx, sy = (cx-ww[wi])/gap, (cy-hh[hi])/gap # 用ceil左上角做坐标并进行归一化
    ceillen = (5+len(class_types))
    log = math.log
    z = torch.zeros((S, S, len(anchors)*ceillen))
    for i, (aw, ah) in enumerate(anchors): # 这里的 anchor 没有参与处理，因为我暂时不会用，照着公式写仍旧有问题
        left = i*ceillen
        clz = [0.]*len(class_types)
        clz[class_types.get(imginfo['cate'])] = 1.
        # v = torch.FloatTensor([sx, sy, log(bw/aw), log(bh/ah), 1.] + clz)
        v = torch.FloatTensor([sx, sy, bw, bh, 1.] + clz)
        z[wi, hi, left:left+ceillen] = v
    return z

















import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
from torch.autograd import Variable

USE_CUDA = True if torch.cuda.is_available() else False
DEVICE = 'cuda' if USE_CUDA else 'cpu'
torch.set_printoptions(precision=2, sci_mode=False, linewidth=120, profile='full')

class Mini(nn.Module):
    class ConvBN(nn.Module):
        def __init__(self, cin, cout, kernel_size=3, stride=1, padding=None):
            super().__init__()
            padding   = (kernel_size - 1) // 2 if not padding else padding
            self.conv = nn.Conv2d(cin, cout, kernel_size, stride, padding, bias=False)
            self.bn   = nn.BatchNorm2d(cout, momentum=0.01)
            self.relu = nn.LeakyReLU(0.01, inplace=True)
        def forward(self, x): 
            return self.relu(self.bn(self.conv(x)))
    def __init__(self, anchors, class_types, inchennel=3):
        super().__init__()
        self.oceil = len(anchors)*(5+len(class_types))
        self.model = nn.Sequential(
            OrderedDict([
                ('ConvBN_0',  self.ConvBN(inchennel, 32)),
                ('Pool_0',    nn.MaxPool2d(2, 2)),
                ('ConvBN_1',  self.ConvBN(32, 64)),
                ('Pool_1',    nn.MaxPool2d(2, 2)),
                ('ConvBN_2',  self.ConvBN(64, 128)),
                ('Pool_2',    nn.MaxPool2d(2, 2)),
                ('ConvBN_3',  self.ConvBN(128, 256)),
                ('Pool_3',    nn.MaxPool2d(2, 2)),
                ('ConvBN_4',  self.ConvBN(256, 512)),
                ('Pool_4',    nn.MaxPool2d(2, 2)),
                ('ConvBN_5',  self.ConvBN(512, 1024)),
                ('ConvEND',   nn.Conv2d(1024, self.oceil, 1)),
            ])
        )
    def forward(self, x):
        return self.model(x).permute(0,2,3,1)

class yoloLoss(nn.Module):
    def __init__(self,S, anchors, class_types):
        super(yoloLoss,self).__init__()
        self.S = S
        self.B = len(anchors)
        self.clazlen = len(class_types)
        self.ceillen = (5+self.clazlen)
        # self.anchor0 = torch.FloatTensor(anchors[0]).to(DEVICE)

    def get_iou(self,box_pred,box_target):
        rate = 416/self.S

        pre_xy = box_pred[...,:2] * rate
        pre_wh_half = box_pred[...,2:4]/2
        pre_mins = pre_xy - pre_wh_half
        pre_maxs = pre_xy + pre_wh_half
        true_xy = box_target[...,:2] * rate
        true_wh_half = box_target[...,2:4]/2
        true_mins = true_xy - true_wh_half
        true_maxs = true_xy + true_wh_half

        inter_mins = torch.max(true_mins, pre_mins)
        inter_maxs = torch.min(true_maxs, pre_maxs)
        inter_wh   = torch.max(inter_maxs - inter_mins, torch.FloatTensor([0.]).to(DEVICE))
        inter_area = inter_wh[...,0] * inter_wh[...,1]
        ture_area = box_pred[...,2] * box_pred[...,3]
        pred_area = box_target[...,2] * box_target[...,3]
        IOUS = inter_area/(ture_area+pred_area-inter_area)
        return IOUS

    def forward(self,pred_tensor,target_tensor):
        N = pred_tensor.size()[0]
        coo_mask     = target_tensor[:,:,:,4] > 0
        noo_mask     = target_tensor[:,:,:,4] == 0
        coo_mask     = coo_mask.unsqueeze(-1).expand_as(target_tensor)
        noo_mask     = noo_mask.unsqueeze(-1).expand_as(target_tensor)
        coo_pred     = pred_tensor[coo_mask].view(N,-1,self.ceillen).to(DEVICE)
        coo_target   = target_tensor[coo_mask].view(N,-1,self.ceillen).to(DEVICE)
        box_pred     = coo_pred[...,0:5].contiguous().view(N,-1,5).to(DEVICE)
        box_target   = coo_target[...,0:5].contiguous().view(N,-1,5).to(DEVICE)
        class_pred   = coo_pred[...,5:5+self.clazlen]
        class_target = coo_target[...,5:5+self.clazlen]

        # 使用torch的函数时候，要注意会在执行点进行训练处理，所以不能将该处的处理滞后
        # 这里可以很重要，因为容易变踩坑，滞后的话训练会出现异常
        box_pred[...,4]  = torch.sigmoid(box_pred[...,4])
        box_pred[...,:2] = torch.sigmoid(box_pred[...,:2])
        # box_pred[...,2:4] = torch.exp(box_pred[...,2:4])*self.anchor0
        # 非目标区将降低误差处理
        noo_pred   = pred_tensor[noo_mask].view(N,-1,self.ceillen).to(DEVICE)
        noo_target = target_tensor[noo_mask].view(N,-1,self.ceillen).to(DEVICE)
        # 置信度
        IOUS = self.get_iou(box_pred,box_target)
        box_contain_loss = F.mse_loss(box_pred[...,4]*IOUS,box_target[...,4],reduction='sum')
        noo_contain_loss = F.mse_loss(noo_pred[...,4]*IOUS,noo_target[...,4],reduction='sum')*.5
        # 坐标点的误差，注意这里的wh，因为我没有使用anchor，所以这里直接除以 416 来均衡敏感度。
        locxy_loss = F.mse_loss(box_pred[...,:2],box_target[...,:2],reduction='sum')
        locwh_loss = F.mse_loss(box_pred[...,2:4]/416,box_target[...,2:4]/416,reduction='sum')
        loc_loss   = locxy_loss + locwh_loss
        # 分类误差
        class_loss = F.mse_loss(class_pred,class_target,reduction='sum')
        # 全部误差
        all_loss = (box_contain_loss + noo_contain_loss + loc_loss + class_loss)/N
        print('[ IOUS ]              :', IOUS)
        print('[ box_contain_loss ]  :', box_contain_loss)
        print('[ noo_contain_loss ]  :', noo_contain_loss)
        print('[ loc_loss ]          :', loc_loss)
        print('[  |locxy_loss ]      :', locxy_loss)
        print('[  |locwh_loss ]      :', locwh_loss)
        print('[ class_loss ]        :', class_loss)
        print('[ all_loss ]          :', all_loss)
        return all_loss
















# 将经过网络得内容转换成坐标和分类名字
def parse_y_pred(ypred):
    if USE_CUDA:
        a = ypred[:,:,:,4].cpu().detach().numpy()
    else:
        a = ypred[:,:,:,4].detach().numpy()
    nn = None
    mm = float('inf')
    for ii,i in enumerate(a[0]):
        for jj,j in enumerate(i):
            if j > mm or nn == None:
                nn = (ii,jj)
                mm = j
    gap = 416/ypred.shape[1]
    x,y = nn
    contain = torch.sigmoid(ypred[0,x,y,4])
    pred_xy = torch.sigmoid(ypred[0,x,y,0:2])
    pred_wh = ypred[0,x,y,2:4]
    pred_clz = ypred[0,x,y,5:5+len(class_types)]
    if USE_CUDA:
        pred_xy = pred_xy.cpu().detach().numpy()
        pred_wh = pred_wh.cpu().detach().numpy()
        pred_clz = pred_clz.cpu().detach().numpy()
    else:
        pred_xy = pred_xy.detach().numpy()
        pred_wh = pred_wh.detach().numpy()
        pred_clz = pred_clz.detach().numpy()
    cx, cy = map(float, pred_xy)
    rx, ry = (cx + x)*gap, (cy + y)*gap
    rw, rh = map(float, pred_wh)
    clz_   = list(map(float, pred_clz))
    xx = rx - rw/2
    _x = rx + rw/2
    yy = ry - rh/2
    _y = ry + rh/2
    for key in class_types:
        if clz_.index(max(clz_)) == class_types[key]:
            clz = key
            break
    return [xx, yy, _x, _y], clz, mm

















def train():
    EPOCH = 1
    BATCH_SIZE = 2
    LR = 0.001
    train_loader = Data.DataLoader(
        dataset=train_data,
        batch_size=BATCH_SIZE,
        # shuffle=SHUFFLE,
    )
    net = Mini(anchors, class_types)
    net.to(DEVICE)
    optimizer = torch.optim.Adam(net.parameters(), lr=LR)
    yloss = yoloLoss(13, anchors=anchors, class_types=class_types, )
    with torch.no_grad():
        x_test = train_data[0][0]
        y_test = train_data[0][1]
    # 测试代码，目前只抽取一张图片无限训练，这样可以很快测试这张图片是否存在收敛
    # 正式使用请改成训练全部图片的代码
    for epoch in range(EPOCH):
        print('epoch', epoch)
        for step, (x_true_, y_true_) in enumerate(train_loader):
            break
        for step in range(500):
            print('[{:<3}]'.format(step), end='')
            x_true = Variable(x_true_).to(DEVICE)
            y_true = Variable(y_true_).to(DEVICE)
            output = net(x_true)
            loss = yloss(output, y_true)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if step%10 == 0:
                y_pred = net(x_test.unsqueeze(0).to(DEVICE))
                rect, clz, con = parse_y_pred(y_pred)
    print('end.')
    torch.save(net, 'net.pkl')
    print('save.')









def drawrect_and_show(imgfile, rect, text):# 只能写英文
    img = cv2.imread(imgfile)
    cv2.rectangle(img, tuple(rect[:2]), tuple(rect[2:]), (10,10,10), 1, 1)
    x, y = rect[:2]
    cv2.putText(img, text, (x,y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10,10,10), 1)
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def test():
    net = torch.load('net.pkl').to(DEVICE)
    net.eval() # 重点中的重点，被坑了一整天。
    with torch.no_grad():
        for i in range(2):
            y_pred = net(train_data[i][0].unsqueeze(0).to(DEVICE))
            rect, clz, con = parse_y_pred(y_pred)
            rh = imginfos[i]['rateh']
            rw = imginfos[i]['ratew']
            rect[0],rect[2] = int(rect[0]*rw),int(rect[2]*rw)
            rect[1],rect[3] = int(rect[1]*rh),int(rect[3]*rh)
            con = torch.sigmoid(torch.FloatTensor([con])).tolist()[0]
            drawrect_and_show(imginfos[i]['file'], rect, '{}|{:<.2f}'.format(clz,con))











# 加载数据，生成训练数据的结构，主要需要的三个数据 anchors，class_types，train_data
xmlpath = './train_img'
SHUFFLE = False
files = [os.path.join(xmlpath, path) for path in os.listdir(xmlpath) if path.endswith('.xml')]
print('load_xml_num:',len(files))
anchors = [[121, 174]] # 这里的内容没有被实际用到，仅留后续扩展考虑。
imginfos = [readxml(file) for file in files]
class_types = [imginfo.get('cate') for imginfo in imginfos]
class_types = {typ:idx for idx,typ in enumerate(sorted(list(set(class_types))))}
train_data = [(torch.FloatTensor(imginfo['numpy']), \
              make_y_true(imginfo, 13, anchors, class_types)) for imginfo in imginfos]
print('class_types:',class_types)
train()
test()








# f = imginfos[0]['file']
# rw,rh = imginfos[0]['ratew'],imginfos[0]['rateh']
# rect = tuple(map(int, imginfos[0]['rect']))
# print(rect)
# v = cv2.imread(f)
# v = cv2.cvtColor(v, cv2.COLOR_BGR2RGB)
# v = cv2.resize(v, (416, 416))
# cv2.rectangle(v, tuple(rect[:2]), tuple(rect[2:]), (10,10,10), 1, 1)
# cv2.imshow('123', v.astype(np.uint8))
# cv2.waitKey(0)