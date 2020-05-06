# 这部分的代码接近能用了，不过暂时还在调整当中
# 至少在无限训练一张图片的时候能够收敛了！使用的 backbone 网络非常粗暴。
# 目前仅考虑小图定位的处理。后续按需求扩展。
# 需要配合标注工具使用

# 开发于 python3，仅需要下面两个第三方依赖，训练的数据为 labelimg 标注型的数据。
# 依赖 pytorch：（官网找安装方式）开发使用版本为 torch-1.4.0-cp36-cp36m-win_amd64.whl
# 依赖 opencv： （pip install opencv-contrib-python==3.4.1.15）
#     其实这里的 opencv 版本不重要，py3能用就行，只是个人喜欢这个版本，因为能用sift图像检测，稳。






# 适配多锚点，不过不像是 darknet 那样检查三个尺度。目前只检查一个尺度。






import cv2
import numpy as np
import torch

import os
import math
import xml.dom.minidom
from collections import OrderedDict

def read_voc_xml(file, islist=False):
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

# 生成 y_true 用于误差计算
def make_y_true(imginfo, S, anchors, class_types):
    def get_max_match_anchor_idx(anchors, bw, bh):
        ious = []
        for aw, ah in anchors:
            mi = min(aw,bw)*min(ah,bh)
            ma = max(aw,bw)*max(ah,bh)
            ious.append(mi/(aw*ah + bw*bh - mi))
        return ious.index(max(ious))
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
    indx = get_max_match_anchor_idx(anchors, bw, bh)
    for i, (aw, ah) in enumerate(anchors):
        if i == indx:
            left = i*ceillen
            clz = [0.]*len(class_types)
            clz[class_types.get(imginfo['cate'])] = 1.
            v = torch.FloatTensor([sx, sy, log(bw/aw), log(bh/ah), 1.] + clz)
            z[wi, hi, left:left+ceillen] = v
    return z

# 将经过网络得内容转换成坐标和分类名字
def parse_y_pred(ypred, anchors, class_types):
    ceillen = 5+len(class_types)
    nn = None
    mm = float('inf')
    for idx in range(len(anchors)):
        if USE_CUDA:
            a = ypred[:,:,:,4+idx*ceillen].cpu().detach().numpy()
        else:
            a = ypred[:,:,:,4+idx*ceillen].detach().numpy()
        for ii,i in enumerate(a[0]):
            for jj,j in enumerate(i):
                if j > mm or nn == None:
                    nn = (ii,jj,idx)
                    mm = j
    gap = 416/ypred.shape[1]
    x,y,idx = nn
    gp = idx*ceillen
    contain = torch.sigmoid(ypred[0,x,y,gp+4])
    pred_xy = torch.sigmoid(ypred[0,x,y,gp+0:gp+2])
    pred_wh = ypred[0,x,y,gp+2:gp+4]
    pred_clz = ypred[0,x,y,gp+5:gp+5+len(class_types)]
    if USE_CUDA:
        pred_xy = pred_xy.cpu().detach().numpy()
        pred_wh = pred_wh.cpu().detach().numpy()
        pred_clz = pred_clz.cpu().detach().numpy()
    else:
        pred_xy = pred_xy.detach().numpy()
        pred_wh = pred_wh.detach().numpy()
        pred_clz = pred_clz.detach().numpy()
    import math
    exp = math.exp
    cx, cy = map(float, pred_xy)
    rx, ry = (cx + x)*gap, (cy + y)*gap
    rw, rh = map(float, pred_wh)
    rw, rh = exp(rw)*anchors[idx][0], exp(rh)*anchors[idx][1]
    clz_   = list(map(float, pred_clz))
    xx = rx - rw/2
    _x = rx + rw/2
    yy = ry - rh/2
    _y = ry + rh/2
    np.set_printoptions(precision=2, linewidth=200, suppress=True)
    if USE_CUDA:
        log_cons = torch.sigmoid(ypred[:,:,:,gp+4]).cpu().detach().numpy()
    else:
        log_cons = torch.sigmoid(ypred[:,:,:,gp+4]).detach().numpy()
    log_cons = np.transpose(log_cons, (0, 2, 1))
    for key in class_types:
        if clz_.index(max(clz_)) == class_types[key]:
            clz = key
            break
    return [xx, yy, _x, _y], clz, mm, log_cons
















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
            self.relu = nn.LeakyReLU(0.1, inplace=True)
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
    def __init__(self, S, anchors, class_types):
        super(yoloLoss,self).__init__()
        self.S = S
        self.B = len(anchors)
        self.clazlen = len(class_types)
        self.ceillen = (5+self.clazlen)
        self.anchors = torch.FloatTensor(anchors).to(DEVICE)

    def get_iou(self,box_pred,box_targ,anchor_idx):
        rate = 416/self.S
        pre_xy = box_pred[...,:2] * rate
        pre_wh_half = torch.exp(box_pred[...,2:4])*self.anchors[anchor_idx]/2
        pre_mins = pre_xy - pre_wh_half
        pre_maxs = pre_xy + pre_wh_half
        true_xy = box_targ[...,:2] * rate
        true_wh_half = torch.exp(box_targ[...,2:4])*self.anchors[anchor_idx]/2
        true_mins = true_xy - true_wh_half
        true_maxs = true_xy + true_wh_half

        inter_mins = torch.max(true_mins, pre_mins)
        inter_maxs = torch.min(true_maxs, pre_maxs)
        inter_wh   = torch.max(inter_maxs - inter_mins, torch.FloatTensor([0.]).to(DEVICE))
        inter_area = inter_wh[...,0] * inter_wh[...,1]
        ture_area = torch.exp(box_pred[...,2])*self.anchors[anchor_idx][0] * torch.exp(box_pred[...,3])*self.anchors[anchor_idx][1]
        pred_area = torch.exp(box_targ[...,2])*self.anchors[anchor_idx][0] * torch.exp(box_targ[...,3])*self.anchors[anchor_idx][1]
        ious = inter_area/(ture_area+pred_area-inter_area)
        return ious

    def forward(self,predict_tensor,target_tensor):
        N = predict_tensor.size()[0]
        box_contain_loss = 0
        noo_contain_loss = 0
        locxy_loss       = 0
        locwh_loss       = 0
        loc_loss         = 0
        class_loss       = 0
        for idx in range(self.B):
            targ_tensor = target_tensor [:,:,:,idx*self.ceillen:(idx+1)*self.ceillen]
            pred_tensor = predict_tensor[:,:,:,idx*self.ceillen:(idx+1)*self.ceillen]
            coo_mask = (targ_tensor[:,:,:,4] >  0).unsqueeze(-1).expand_as(targ_tensor)
            noo_mask = (targ_tensor[:,:,:,4] == 0).unsqueeze(-1).expand_as(targ_tensor)
            if not torch.any(coo_mask): 
                noo_pred = pred_tensor[noo_mask].view(N,-1,self.ceillen)
                noo_targ = targ_tensor[noo_mask].view(N,-1,self.ceillen)
                noo_contain_loss += F.mse_loss(torch.sigmoid(noo_pred[...,4])*1, noo_targ[...,4],reduction='sum')*.1
            else:
                coo_pred = pred_tensor[coo_mask].view(N,-1,self.ceillen).to(DEVICE)
                coo_targ = targ_tensor[coo_mask].view(N,-1,self.ceillen).to(DEVICE)
                noo_pred = pred_tensor[noo_mask].view(N,-1,self.ceillen)
                noo_targ = targ_tensor[noo_mask].view(N,-1,self.ceillen)

                box_pred = coo_pred[...,0:5].contiguous().view(N,-1,5)
                box_targ = coo_targ[...,0:5].contiguous().view(N,-1,5)
                class_pred = coo_pred[...,5:5+self.clazlen]
                class_targ = coo_targ[...,5:5+self.clazlen]

                box_pred[...,:2] = torch.sigmoid(box_pred[...,:2])
                ious = self.get_iou(box_pred,box_targ,idx)
                box_contain_loss += F.mse_loss(torch.sigmoid(box_pred[...,4])*ious, box_targ[...,4],reduction='sum')
                noo_contain_loss += F.mse_loss(torch.sigmoid(noo_pred[...,4])*ious, noo_targ[...,4],reduction='sum')*.1
                locxy_loss       += F.mse_loss(box_pred[...,0:2], box_targ[...,0:2],reduction='sum')
                locwh_loss       += F.mse_loss(box_pred[...,2:4], box_targ[...,2:4],reduction='sum')
                loc_loss         += locxy_loss + locwh_loss
                class_loss       += F.mse_loss(class_pred,class_targ,reduction='sum')
                # print('[ ious ]              :', ious)
        all_loss = (box_contain_loss + noo_contain_loss + loc_loss + class_loss)/N/self.B
        print(
            '[ loss ] (con){:>.3f}, (noo){:>.3f}, (xy){:>.3f}, (wh){:>.3f}, (class){:>.3f}, (all){:>.3f}.'.format(
                box_contain_loss.item(),    noo_contain_loss.item(),    locxy_loss.item(),
                locwh_loss.item(),          class_loss.item(),          all_loss.item(),
            )
        )
        return all_loss
























def train(train_data, anchors, class_types):
    EPOCH = 1
    BATCH_SIZE = 2
    LR = 0.001
    train_loader = Data.DataLoader(
        dataset    = train_data,
        batch_size = BATCH_SIZE,
        # shuffle    = True,
    )
    try:
        state = torch.load('net.pkl')
        net = state['net'].to(DEVICE)
        optimizer = state['optimizer']
        epoch = state['epoch']
        print('load train.')
    except:
        net = Mini(anchors, class_types)
        net.to(DEVICE)
        optimizer = torch.optim.Adam(net.parameters(), lr=LR)
        epoch = 0
        print('new train.')
    yloss = yoloLoss(13, anchors=anchors, class_types=class_types, )
    net.train()
    for epoch in range(epoch, epoch+EPOCH):
        print('epoch', epoch)
        for step, (x_true_, y_true_) in enumerate(train_loader):
            break
        for step in range(250):
            print('[{:<3}]'.format(step), end='')
            x_true = Variable(x_true_).to(DEVICE)
            y_true = Variable(y_true_).to(DEVICE)
            output = net(x_true)
            loss = yloss(output, y_true)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    print('end.')
    state = {'net':net, 'optimizer':optimizer, 'epoch':epoch+1, 'anchors':anchors, 'class_types':class_types}
    torch.save(state, 'net.pkl')
    print('save.')









def drawrect_and_show(imgfile, rect, text):# 只能写英文
    img = cv2.imread(imgfile)
    cv2.rectangle(img, tuple(rect[:2]), tuple(rect[2:]), (10,10,10), 1, 1)
    x, y = rect[:2]
    cv2.putText(img, text, (x,y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10,10,10), 1)
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def test(imginfos):
    state = torch.load('net.pkl')
    net = state['net'].to(DEVICE)
    optimizer = state['optimizer']
    anchors = state['anchors']
    class_types = state['class_types']
    net.eval() # 重点中的重点，被坑了一整天。
    with torch.no_grad():
        for i in range(10):
            y_pred = net(torch.FloatTensor(imginfos[i]['numpy']).unsqueeze(0).to(DEVICE))
            rect, clz, con, log_cons = parse_y_pred(y_pred, anchors, class_types)
            rh = imginfos[i]['rateh']
            rw = imginfos[i]['ratew']
            rect[0],rect[2] = int(rect[0]*rw),int(rect[2]*rw)
            rect[1],rect[3] = int(rect[1]*rh),int(rect[3]*rh)
            con = torch.sigmoid(torch.FloatTensor([con])).item()
            print(con)
            print(log_cons)
            drawrect_and_show(imginfos[i]['file'], rect, '{}|{:<.2f}'.format(clz,con))
def test2(filename):
    state = torch.load('net.pkl')
    net = state['net'].to(DEVICE)
    optimizer = state['optimizer']
    anchors = state['anchors']
    class_types = state['class_types']
    net.eval() # 重点中的重点，被坑了一整天。
    npimg = cv2.imread(filename)
    height, width = npimg.shape[:2]
    npimg = cv2.cvtColor(npimg, cv2.COLOR_BGR2RGB) # [y,x,c]
    npimg = cv2.resize(npimg, (416, 416))
    npimg_ = np.transpose(npimg, (2,1,0)) # [c,x,y]
    y_pred = net(torch.FloatTensor(npimg_).unsqueeze(0).to(DEVICE))
    rect, clz, con, log_cons = parse_y_pred(y_pred, anchors, class_types)
    rw, rh = width/416, height/416
    rect[0],rect[2] = int(rect[0]*rw),int(rect[2]*rw)
    rect[1],rect[3] = int(rect[1]*rh),int(rect[3]*rh)
    con = torch.sigmoid(torch.FloatTensor([con])).item()
    print(con)
    print(log_cons)
    drawrect_and_show(filename, rect, '{}|{:<.2f}'.format(clz,con))










def load_voc_data(xmlpath, anchors):
    files = [os.path.join(xmlpath, path) for path in os.listdir(xmlpath) if path.endswith('.xml')]
    imginfos = []
    for idx, file in enumerate(files):
        imginfos.extend(read_voc_xml(file, islist=True))
    # 注意这里加载数据的方式是小批量加载处理，所以自动生成 class_types
    # 如果有大量数据想要进行多批次训练，那么就需要注意 class_types 的生成。
    class_types = [imginfo.get('cate') for imginfo in imginfos]
    class_types = {typ:idx for idx,typ in enumerate(sorted(list(set(class_types))))}
    train_data = []
    for idx, imginfo in enumerate(imginfos):
        x_true = torch.FloatTensor(imginfo['numpy'])
        y_true = make_y_true(imginfo, 13, anchors, class_types)
        train_data.append([x_true, y_true])
    print('load_xml_num:', len(files))
    print('class_types:', class_types)
    print('anchors:', anchors)
    return train_data, imginfos, class_types











# 加载数据，生成训练数据的结构，主要需要的三个数据 anchors，class_types，train_data
# 训练结束后会将 anchors, class_types 信息一并存放，所以预测时无需重新加载数据获取这两项信息
# 如果存在之前的训练文件，会自动加载进行继续训练，并且保存时会覆盖之前的模型
xmlpath = './train_img'
anchors = [[40, 80],[80, 40],[60, 60]]
train_data, imginfos, class_types = load_voc_data(xmlpath, anchors)
train(train_data, anchors, class_types)
test(imginfos)


test2('./train_img/20200426_00000.png')

















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