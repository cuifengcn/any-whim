import random
import numpy as np

def get_9(y,x):
    return np.maximum(y-1,0),y+2,np.maximum(x-1,0),x+2

def mine_zero(y,x,mask,mine,indx):
    sets,lists = set(),[(y,x)]
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

def mine_other(y,x,mask,mine):
    mask[y,x] = mine[y,x]

def mine_init(h,w,minenum,iy,ix):
    v = np.random.sample((h*w,))
    v[np.argsort(v)[:minenum]] = -1
    v[v!=-1] = 0
    v = v.reshape((h,w)).astype(np.int32)
    zero,mine = zip(*np.where(v==0)),zip(*np.where(v!=0))
    if (iy,ix) in mine: # first click must no mine
        mine.remove((iy,ix))
        mine.append(random.choice(zero))
    for y,x in zero:
        mx = v[np.maximum(y-1,0):y+2,np.maximum(x-1,0):x+2]
        v[y,x] = len(mx[mx==-1])
    mask = np.ones((h,w),dtype=np.int32) * -1
    indx = np.concatenate(map(lambda i:i[...,None], np.mgrid[:h,:w]),axis=-1)
    if v[iy,ix]==0: mine_zero(iy,ix,mask,v,indx)
    if v[iy,ix]!=0: mine_other(iy,ix,mask,v)
    return mask,indx,v

h,w = 16,16
minenum = 60

##import os
mask = np.ones((h,w),dtype=np.int32) * -1
##os.system('cls')
##print mask
##
### first click point
##iy,ix = map(int,raw_input('pls input first "x y":').split(' '))
##mask,indx,mine = mine_init(h,w,minenum,iy,ix)
##os.system('cls')
##print mask
##
##while True:
##    x,y = map(int,raw_input('pls input "x y":').split(' '))
##    os.system('cls')
##    if mine[y,x]==-1:
##        print mask
##        break
##    elif mine[y,x]==0:
##        mine_zero(y,x,mask,mine,indx)
##    else:
##        mine_other(y,x,mask,mine)
##    print mask
##print 'you fail. --- mine:'
##print mine
##

def foo(i,j):
    print i,j

from tkinter import *
master = Tk()
for i in range(h):
    for j in range(w):
        if mask[i,j]==-1:tx = ''
        else:tx = str(mask[i,j])
        e = Button(master,text=tx,height=1,width=2,fg='red',command=lambda:foo(i,j))
        e.grid(row=i,column=j,sticky=W+E+N+S)
mainloop()


