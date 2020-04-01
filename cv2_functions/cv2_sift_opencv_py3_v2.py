# 需要安装一些库
# pip install opencv-contrib-python==3.4.1.15 
# 直接安装这个就可以了

import cv2
import numpy as np

# 从大图（22）中找到匹配小图（11）的部分，并进行大图（22）中的定位
i1 = cv2.imread('11.jpg')
i2 = cv2.imread('22.jpg')

s = cv2.xfeatures2d.SIFT_create()
kp1,des1 = s.detectAndCompute(i1,None)
kp2,des2 = s.detectAndCompute(i2,None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)
good = []
for m,n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m.trainIdx, m.queryIdx])

# 获取前几位大图（22）特征点的重心并在大图（22）中标出坐标
xx = yy = 0
for d1,d2 in good:
    x, y = kp2[d1].pt
    xx += x
    yy += y
xx = xx/len(good)
yy = yy/len(good)
print('centre of gravity in match point:',xx,yy)

# 在被定位的位置上画个圈圈
cv2.circle(i2, (int(xx), int(yy)), 20, (0, 0, 255), 2)
cv2.imshow('g', i2)

cv2.waitKey(0)
cv2.destroyAllWindows()