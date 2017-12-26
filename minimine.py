import random, sys
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
def mine_1to8(y,x,mask,mine):
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
    indx = np.concatenate(tuple(map(lambda i:i[...,None], np.mgrid[:h,:w])),axis=-1)
    # python3 function map return a 'map' object, so it need tuple
    if v[iy,ix]==0: mine_zero(iy,ix,mask,v,indx)
    if v[iy,ix]!=0: mine_1to8(iy,ix,mask,v)
    return mask,indx,v

def flash(mask,k=True):
    global minenum,outcome
    for i,j in indx.reshape((-1,2)):
        if mask[i,j] != -1:
            if mask[i,j] != 0:
                exec("e%d_%d['text']=mask[%d,%d]"%(i,j,i,j))
            if k:exec("e%d_%d['relief']='groove'"%(i,j))
        elif not k:exec("e%d_%d['text']='*'"%(i,j))
    if len(mask[mask==-1])==minenum and outcome ==0:
        outcome = 1
        master.title('you win.')

def foo(i,j):
    if 'mask' not in globals():
        global mask,indx,mine
        mask,indx,mine = mine_init(h,w,minenum,i,j)
        flash(mask)
    elif outcome==0:
        if mine[i,j] != -1:
            if mine[i,j]==0:mine_zero(i,j,mask,mine,indx)
            if mine[i,j]!=0:mine_1to8(i,j,mask,mine)
            flash(mask)
        else:
            flash(mine,False)
            master.title('you fail.')

if sys.version[0] == '2':from Tkinter import *
if sys.version[0] == '3':from tkinter import *
master = Tk()
master.title()
h,w,minenum,outcome = 16,16,25,0
for i in range(h):
    for j in range(w):
        exec('def func%d_%d():foo(%d,%d)'%(i,j,i,j))
        exec("e%d_%d = Button(master,text='',width=2,relief='flat',command=func%d_%d)"%(i,j,i,j))
        exec("e%d_%d.grid(row=i,column=j,sticky=W+E+N+S)"%(i,j))
mainloop()
