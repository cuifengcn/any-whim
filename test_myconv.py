from numpy import *
from numba import jit
import cv2,time

def logs(func):
    def t(*args,**kw):
        s = time.time()
        temp = func(*args,**kw)
        print time.time()-s
        return temp
    return t

shapeh,shapew = 13,13

mn = array([[1,0,1],
            [0,0,0],
            [1,0,1]])

mn = dstack((mn,mn,mn))
print mn

img = cv2.imread('nier.jpg')
def get_rdkn((shapeh,shapew)):
    rv = random.random((shapeh,shapew))
    gv = random.random((shapeh,shapew))
    bv = random.random((shapeh,shapew))
    return dstack((rv,gv,bv))
kn = get_rdkn((shapeh,shapew))
bn = get_rdkn((shapeh,shapew))
h,w,c = img.shape

@logs
def conv(h,w,c,kn):
    th,tw,tc = kn.shape
    assert c == tc, 'must'
    n_img = zeros((h-th+1,w-tw+1,c))
    for i in range(h-th+1):
        for j in range(w-tw+1):
            s = img[i:i+th,j:j+tw]*kn
            n_img[i,j] = [sum(s[:,:,m]) for m in range(c)]
    return n_img

def get_npic(n):
    t = conv(h,w,c,n)
    t = t-t.min()
    s = t/t.max()*255-127.5
    return s.astype('uint8')

#s0 = get_npic(kn)
#s1 = get_npic(bn)
s2 = get_npic(mn)
#cv2.imshow('niers0',s0)
#cv2.imshow('niers1',s1)
cv2.imshow('niers2',s2)

cv2.imshow('nier',img)
cv2.imshow('nier2',img-127)
cv2.waitKey()
cv2.destroyAllWindows()

