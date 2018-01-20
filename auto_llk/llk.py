import numpy as np


#for test
s_map = np.random.randint(0,9,(5,5))
s_map[1:4,1:4]=0
point = (2,2)

# 根据输入的方向返回该方向上的同链为零的端点坐标
# 以及其端点延伸一格的坐标（坐标受限于 s_map 范围中）
def get_cross(s_map,point,target):
    h0,w0 = point
    h,w = s_map.shape
    ret,packer = [],[]
    for i in target:
        if i.lower() in ('left','l'):
            k = np.where(s_map[h0,:w0+1]==0)[0].min()
            if k != 0: packer.append((h0, k-1))
        if i.lower() in ('right','r'):
            k = np.where(s_map[h0,w0:]==0)[0].max()+w0
            if k != w-1: packer.append((h0, k+1))
        if i.lower() in ('up','u'):
            k = np.where(s_map[:h0+1,w0]==0)[0].min()
            if k != 0: packer.append((k-1, w0))
        if i.lower() in ('down','d'):
            k = np.where(s_map[h0:,w0]==0)[0].max()+h0
            if k != h-1: packer.append((k+1, w0))
        ret.append(k)
    return ret,packer

# 鱼骨抽关键点的这种算法，目前这里只考虑鱼脊梁为横向的情况
def get_fish(s_map,point):
    pack = []
    (l,r),packer = get_cross(s_map,point,('l','r'))
    pack += packer
    for i in range(l,r+1):
        pt = (point[0],i)
        _,packer = get_cross(s_map,pt,('u','d'))
        pack += packer
    return pack

# 根据坐标点获取其坐标的类别以字典形式返回
def get_class_point(s_map,fishpoint):
    dc = dict()
    for i in fishpoint:
        key = s_map[i]
        if not dc.get(key):
            dc[s_map[i]] = [i]
        else:
            dc[s_map[i]] += [i]
    return dc

# 通过类别坐标字典，获取该字典可以被返回的所有双点
# 双点即为连连看每次需要选择的两个坐标点
def pick_dc_all(dc):
    pts = []
    for i in dc:
        for _ in range(int(len(dc[i])/2)):
            pts.append((dc[i].pop(),dc[i].pop()))
    return pts

# 单个点获取该点下鱼骨端点后能获取到的所有可消除的双点
def get_1point_results(s_map,point):
    fish = get_fish(s_map,point)
    dc   = get_class_point(s_map,fish)
    pts  = pick_dc_all(dc)
    return pts
