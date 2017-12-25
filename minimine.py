import random
import numpy as np

iy,ix = 2,2 # click point
h,w = 16,16
minenum = 60

def mine_init(h,w,minenum,iy,ix):
    v = np.random.sample((h*w,))
    v[np.argsort(v)[:minenum]] = -1
    v[v!=-1] = 0
    v = v.reshape((h,w)).astype(np.int32)
    zero = zip(*np.where(v==0))
    mine = zip(*np.where(v!=0))
    if (iy,ix) in mine: # first click must no mine
        mine.remove((iy,ix))
        mine.append(random.choice(zero))
    for y,x in zero:
        mx = v[np.maximum(y-1,0):y+2,np.maximum(x-1,0):x+2]
        v[y,x] = len(mx[mx==-1])
    return v

def get_9(y,x):
    return np.maximum(y-1,0),y+2,np.maximum(x-1,0),x+2

def mine_zero(y,x,mask,mine,indx):
    sets = set()
    lists = [(y,x)]
    while lists:
        y,x = lists.pop()
        if (y,x) not in sets:
            ly,ry,lx,rx = get_9(y,x)
            ax,bx = mine[ly:ry,lx:rx],indx[ly:ry,lx:rx]
            nexs = set(map(lambda i:tuple(i),bx[np.where(ax==0)]))
            lists += list(nexs)
        sets.add((y,x))
    for y,x in sets:
        ly,ry,lx,rx = get_9(y,x)
        mask[ly:ry,lx:rx] = mine[ly:ry,lx:rx]

def mine_some(y,x,mask,mine,indx):
    mask[y,x] = mine[y,x]
    
mask = np.ones((h,w),dtype=np.int32) * -1
indx = np.concatenate(map(lambda i:i[...,None], np.mgrid[:h,:w]),axis=-1)
mine = mine_init(h,w,minenum,iy,ix)

print mine






