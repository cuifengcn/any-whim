# 并非可以直接用的东西，后续会继续补充

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

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
    npimg = cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2RGB)
    npimg = np.transpose(npimg, (2,0,1))
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

class ConvBN(nn.Module):
    def __init__(self, cin, cout, kernel_size=3, stride=1, padding=None):
        super().__init__()
        padding   = (kernel_size - 1) // 2
        self.conv = nn.Conv2d(cin, cout, kernel_size, stride, padding, bias=False)
        self.bn   = nn.BatchNorm2d(cout, momentum=0.01)
        self.relu = nn.LeakyReLU(0.1, inplace=True)
    def forward(self, x): 
        return self.relu(self.bn(self.conv(x)))

class Mini(nn.Module):
    def __init__(self, inchennel=3):
        super().__init__()
        self.model = nn.Sequential(
            OrderedDict([
                ('ConvBN_0',  ConvBN(inchennel, 32)),
                ('Pool_0',    nn.MaxPool2d(2, 2)),
                ('ConvBN_1',  ConvBN(32, 64)),
                ('Pool_1',    nn.MaxPool2d(2, 2)),
                ('ConvBN_2',  ConvBN(64, 128)),
                ('Pool_2',    nn.MaxPool2d(2, 2)),
                ('ConvBN_3',  ConvBN(128, 256)),
                ('Pool_3',    nn.MaxPool2d(2, 2)),
                ('ConvBN_4',  ConvBN(256, 512)),
                ('Pool_4',    nn.MaxPool2d(2, 2)),
                ('ConvBN_5',  ConvBN(512, 30)),
            ])
        )
    def forward(self, x):
        return self.model(x)

class loss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, pred_box, true_box):
        '''
        pred_box: (tensor) size(batchsize,S,S,Bx5+20=30) [x,y,w,h,c]
        true_box: (tensor) size(batchsize,S,S,30)
        '''
        pass




def make_img_train_tensor(imginfo, S, B):
    '''
    pred_box: (tensor) size(batchsize,S,S,Bx5+20=30) [x,y,w,h,c]
    '''
    cx = imginfo['centerx']
    cy = imginfo['centery']
    w, h = imginfo['width'], imginfo['height']
    bw = imginfo['xmax'] - imginfo['xmin']
    bh = imginfo['ymax'] - imginfo['ymin']
    gap = int(w/S)
    ww = list(range(416))[::int(gap)]
    for wi in range(len(ww)):
        if cx < ww[wi]:
            break
    hh = list(range(416))[::int(gap)]
    for hi in range(len(hh)):
        if cy < hh[hi]:
            break
    wi, hi = wi - 1, hi - 1
    sx, sy = cx-ww[wi], cy-hh[hi] # 与ceil的偏差大小
    z = torch.zeros((1, B*5+20, S, S))
    z[:,4,wi,hi] = 1 # 第一个计算窗的置信度
    z[:,:4,wi,hi] = torch.FloatTensor([sx, sy, bw, bh])
    z[:,9,wi,hi] = 1 # 第二个计算窗的置信度
    z[:,5:9,wi,hi] = torch.FloatTensor([sx, sy, bw, bh])
    z[:,10:,wi,hi] = torch.FloatTensor([0.]*19+[1.])
    print(z.shape)
    print(z.size())
    q = z[:,:10].contiguous().view(-1,5)
    print(q.shape)


xmlpath = './train_img/xmlpath/'
file = os.path.join(xmlpath, os.listdir(xmlpath)[0])
imginfo = readxml(file, islist=False)

img_ = imginfo['numpy']
img_ = torch.FloatTensor(img_).unsqueeze(0)
print(img_.shape)
s = make_img_train_tensor(imginfo, 13, 2)


net = Mini()
v = net(img_)
print(v.shape)









# 下面的模型是从别的代码里面抄过来的，后续会更具这些进行个人代码上的修改
class yoloLoss(nn.Module):
    def __init__(self,S,B,l_coord,l_noobj):
        super(yoloLoss,self).__init__()
        self.S = S
        self.B = B
        self.l_coord = l_coord
        self.l_noobj = l_noobj

    def compute_iou(self, box1, box2):
        '''Compute the intersection over union of two set of boxes, each box is [x1,y1,x2,y2].
        Args:
          box1: (tensor) bounding boxes, sized [N,4].
          box2: (tensor) bounding boxes, sized [M,4].
        Return:
          (tensor) iou, sized [N,M].
        '''
        N = box1.size(0)
        M = box2.size(0)

        lt = torch.max(
            box1[:,:2].unsqueeze(1).expand(N,M,2),  # [N,2] -> [N,1,2] -> [N,M,2]
            box2[:,:2].unsqueeze(0).expand(N,M,2),  # [M,2] -> [1,M,2] -> [N,M,2]
        )

        rb = torch.min(
            box1[:,2:].unsqueeze(1).expand(N,M,2),  # [N,2] -> [N,1,2] -> [N,M,2]
            box2[:,2:].unsqueeze(0).expand(N,M,2),  # [M,2] -> [1,M,2] -> [N,M,2]
        )

        wh = rb - lt  # [N,M,2]
        wh[wh<0] = 0  # clip at 0
        inter = wh[:,:,0] * wh[:,:,1]  # [N,M]

        area1 = (box1[:,2]-box1[:,0]) * (box1[:,3]-box1[:,1])  # [N,]
        area2 = (box2[:,2]-box2[:,0]) * (box2[:,3]-box2[:,1])  # [M,]
        area1 = area1.unsqueeze(1).expand_as(inter)  # [N,] -> [N,1] -> [N,M]
        area2 = area2.unsqueeze(0).expand_as(inter)  # [M,] -> [1,M] -> [N,M]

        iou = inter / (area1 + area2 - inter)
        return iou
    def forward(self,pred_tensor,target_tensor):
        '''
        pred_tensor: (tensor) size(batchsize,S,S,Bx5+20=30) [x,y,w,h,c]
        target_tensor: (tensor) size(batchsize,S,S,30)
        '''
        N = pred_tensor.size()[0]
        coo_mask = target_tensor[:,:,:,4] > 0
        noo_mask = target_tensor[:,:,:,4] == 0
        coo_mask = coo_mask.unsqueeze(-1).expand_as(target_tensor)
        noo_mask = noo_mask.unsqueeze(-1).expand_as(target_tensor)

        coo_pred = pred_tensor[coo_mask].view(-1,30)
        box_pred = coo_pred[:,:10].contiguous().view(-1,5) #box[x1,y1,w1,h1,c1]
        class_pred = coo_pred[:,10:]                       #[x2,y2,w2,h2,c2]
        
        coo_target = target_tensor[coo_mask].view(-1,30)
        box_target = coo_target[:,:10].contiguous().view(-1,5)
        class_target = coo_target[:,10:]

        # compute not contain obj loss
        noo_pred = pred_tensor[noo_mask].view(-1,30)
        noo_target = target_tensor[noo_mask].view(-1,30)
        noo_pred_mask = torch.cuda.ByteTensor(noo_pred.size())
        noo_pred_mask.zero_()
        noo_pred_mask[:,4]=1;noo_pred_mask[:,9]=1
        noo_pred_c = noo_pred[noo_pred_mask] #noo pred只需要计算 c 的损失 size[-1,2]
        noo_target_c = noo_target[noo_pred_mask]
        nooobj_loss = F.mse_loss(noo_pred_c,noo_target_c,size_average=False)

        #compute contain obj loss
        coo_response_mask = torch.cuda.ByteTensor(box_target.size())
        coo_response_mask.zero_()
        coo_not_response_mask = torch.cuda.ByteTensor(box_target.size())
        coo_not_response_mask.zero_()
        box_target_iou = torch.zeros(box_target.size()).cuda()
        for i in range(0,box_target.size()[0],2): #choose the best iou box
            box1 = box_pred[i:i+2]
            box1_xyxy = Variable(torch.FloatTensor(box1.size()))
            box1_xyxy[:,:2] = box1[:,:2]/14. -0.5*box1[:,2:4]
            box1_xyxy[:,2:4] = box1[:,:2]/14. +0.5*box1[:,2:4]
            box2 = box_target[i].view(-1,5)
            box2_xyxy = Variable(torch.FloatTensor(box2.size()))
            box2_xyxy[:,:2] = box2[:,:2]/14. -0.5*box2[:,2:4]
            box2_xyxy[:,2:4] = box2[:,:2]/14. +0.5*box2[:,2:4]
            iou = self.compute_iou(box1_xyxy[:,:4],box2_xyxy[:,:4]) #[2,1]
            max_iou,max_index = iou.max(0)
            max_index = max_index.data.cuda()
            
            coo_response_mask[i+max_index]=1
            coo_not_response_mask[i+1-max_index]=1

            #####
            # we want the confidence score to equal the
            # intersection over union (IOU) between the predicted box
            # and the ground truth
            #####
            box_target_iou[i+max_index,torch.LongTensor([4]).cuda()] = (max_iou).data.cuda()
        box_target_iou = Variable(box_target_iou).cuda()
        #1.response loss
        box_pred_response = box_pred[coo_response_mask].view(-1,5)
        box_target_response_iou = box_target_iou[coo_response_mask].view(-1,5)
        box_target_response = box_target[coo_response_mask].view(-1,5)
        contain_loss = F.mse_loss(box_pred_response[:,4],box_target_response_iou[:,4],size_average=False)
        loc_loss = F.mse_loss(box_pred_response[:,:2],box_target_response[:,:2],size_average=False) + F.mse_loss(torch.sqrt(box_pred_response[:,2:4]),torch.sqrt(box_target_response[:,2:4]),size_average=False)
        #2.not response loss
        box_pred_not_response = box_pred[coo_not_response_mask].view(-1,5)
        box_target_not_response = box_target[coo_not_response_mask].view(-1,5)
        box_target_not_response[:,4]= 0
        #not_contain_loss = F.mse_loss(box_pred_response[:,4],box_target_response[:,4],size_average=False)
        
        #I believe this bug is simply a typo
        not_contain_loss = F.mse_loss(box_pred_not_response[:,4], box_target_not_response[:,4],size_average=False)

        #3.class loss
        class_loss = F.mse_loss(class_pred,class_target,size_average=False)

        return (self.l_coord*loc_loss + 2*contain_loss + not_contain_loss + self.l_noobj*nooobj_loss + class_loss)/N




