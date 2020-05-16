# 写一个中文的单字识别的cnn
# 尽可能的搞定旋转缩放之类的分类问题












import os
import cv2
import numpy as np

# 读取单字图片文件
def read_imginfos(file):
    # 目前读取的数据是单字识别，这里读取的格式为，图片文件的第一个汉字代表了其类别
    class_types = set()
    imginfos = []
    for i in os.listdir(file):
        if i.endswith('.jpg') or i.endswith('.png'):
            class_types.add(i[0])
    for i in os.listdir(file):
        if i.endswith('.jpg') or i.endswith('.png'):
            fil = os.path.join(file, i)
            img = cv2.imdecode(np.fromfile(fil, dtype=np.uint8), 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # [y,x,c]
            img = cv2.resize(img, (40, 40))
            img = np.transpose(img, (2,1,0)) # [c,x,y]
            imginfo = {}
            imginfo['class'] = i[0]
            imginfo['img'] = img
            imginfos.append(imginfo)
            # cv2.imshow('test', img)
            # cv2.waitKey(0)
    class_types = {tp: idx for idx, tp in enumerate(sorted(class_types))}
    return imginfos, class_types

# 生成 y_true 用于误差计算
def make_y_true(imginfo, class_types):
    img = imginfo['img']
    class_types.get(imginfo['class'])
    clz = [0.]*len(class_types)
    clz[class_types.get(imginfo['class'])] = 1.
    return torch.FloatTensor(clz)

def load_data(filepath):
    imginfos, class_types = read_imginfos(filepath)
    train_data = []
    for imginfo in imginfos:
        train_data.append([torch.FloatTensor(imginfo['img']), make_y_true(imginfo, class_types)])
    return train_data, class_types












import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
from torch.autograd import Variable
from collections import OrderedDict

USE_CUDA = True if torch.cuda.is_available() else False
DEVICE = 'cuda' if USE_CUDA else 'cpu'
torch.set_printoptions(precision=2, sci_mode=False, linewidth=120, profile='full')

class MiniCNN(nn.Module):
    class ConvBN(nn.Module):
        def __init__(self, cin, cout, kernel_size=3, stride=1, padding=None):
            super().__init__()
            padding   = (kernel_size - 1) // 2 if not padding else padding
            self.conv = nn.Conv2d(cin, cout, kernel_size, stride, padding, bias=False)
            self.bn   = nn.BatchNorm2d(cout, momentum=0.01)
            self.relu = nn.LeakyReLU(0.1, inplace=True)
        def forward(self, x): 
            return self.relu(self.bn(self.conv(x)))
    def __init__(self, class_types, inchennel=3):
        super().__init__()
        self.oceil = len(class_types)
        self.model = nn.Sequential(
            OrderedDict([
                ('ConvBN_0',  self.ConvBN(inchennel, 32)),
                ('Pool_0',    nn.MaxPool2d(2, 2)),
                ('ConvBN_1',  self.ConvBN(32, 64)),
                ('Pool_1',    nn.MaxPool2d(2, 2)),
                ('ConvBN_2',  self.ConvBN(64, 128)),
                ('Pool_2',    nn.MaxPool2d(2, 2)),
                ('ConvBN_3',  self.ConvBN(128, 256)),
                ('Flatten',   nn.Flatten()),
                ('Linear',    nn.Linear(6400, self.oceil)),
            ])
        )
    def forward(self, x):
        x = torch.sigmoid(self.model(x))
        return x

class miniloss(nn.Module):
    def __init__(self, class_types):
        super().__init__()
        self.clazlen = len(class_types)

    def forward(self, pred, targ, callback=None):
        loss = F.mse_loss(pred,targ,reduction='sum')
        global print
        print = callback if callback else print
        print(loss)
        return loss

def train(train_data, class_types):
    EPOCH = 10
    BATCH_SIZE = 100
    LR = 0.001
    net = MiniCNN(class_types).to(DEVICE)
    mloss = miniloss(class_types).to(DEVICE)
    optimizer = torch.optim.Adam(net.parameters(), lr=LR)
    train_loader = Data.DataLoader(
        dataset=train_data,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )
    for epoch in range(EPOCH):
        print('epoch', epoch)
        for step, (b_x, b_y) in enumerate(train_loader):
            b_x = Variable(b_x).to(DEVICE)
            b_y = Variable(b_y).to(DEVICE)
            loss = mloss(net(b_x), b_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        state = {'net':net.state_dict(), 'optimizer':optimizer, 'epoch':epoch+1, 'class_types':class_types}
        torch.save(state, 'net.pkl')
        print('save.')
    print('end.')










def load_state(filename):
    state = torch.load(filename)
    class_types = state['class_types']
    net = MiniCNN(class_types)
    net.load_state_dict(state['net'])
    net.to(DEVICE)
    net.eval()
    state['net'] = net
    return state

def test(filename, state):
    net = state['net'].to(DEVICE)
    class_types = state['class_types']
    img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # [y,x,c]
    img = cv2.resize(img, (40, 40))
    img = np.transpose(img, (2,1,0)) # [c,x,y]
    x = torch.FloatTensor(img).unsqueeze(0).to(DEVICE)
    v = net(x)
    if USE_CUDA:
        v = v.cpu().detach().numpy()
    else:
        v = v.detach().numpy()
    v = v[0].tolist()
    r = sorted(class_types)[v.index(max(v))]
    print(v)
    print(r)
    return r










# train_data, class_types = load_data('./train_img')
# train(train_data, class_types)




print('loading model.')
state = load_state('net.pkl')
print('loading model. ok.')
test('./train_img/你_00_30_(255, 255, 255)_(0, 0, 255)_simsun.ttc.jpg', state)
