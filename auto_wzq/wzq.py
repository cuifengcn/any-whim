import numpy as np
from itertools import groupby

#五子棋类
#包装了下棋函数，判断是否胜利函数以及估值函数
#下棋函数如果返回值不为 False 则返回胜者（player in [1,2]）
class WZQ:
    def __init__(self, h, w):
        self.s_map = np.zeros((h,w)).astype(np.int32)
        self._lu = np.zeros((h,w)).astype(np.bool8)
        self._ru = np.zeros((h,w)).astype(np.bool8)
        self._area_eval = np.zeros((h,w)).astype(np.int32)
        self._scal_eval = self._create_scal(5)
        self._scal_ecal_large = self._create_scal(9)
        self.win = False
        self._values = {
            (1,0,1,1,1,0,1):400,#活四
            (0,1,1,1,1,0):400,#活四
            (1,1,1,1,1):1000,#活五
            (1,1,1,1,0):80,#冲四
            (1,1,1,0,1):80,#冲四
            (1,1,0,1,1):80,#冲四
            (1,0,1,1,1):80,#冲四
            (0,1,1,1,1):80,#冲四
            (0,1,1,1,0):80,#活三
            (0,1,1,0,1):60,#眠三
            (1,0,1,0,1):60,#眠三
            (1,0,1,1,0):60,#眠三
            (1,1,1,0,0):18,#冲三
            (0,0,1,1,1):18,#冲三
            (1,1,0,1,0):18,#冲三
            (0,1,0,1,1):18,#冲三
            (0,1,1,0,0):6,#活二
            (0,0,1,1,0):6,#活二
            (0,1,0,1,0):6,#活二
            (1,0,1,0,0):6,#眠二
            (0,0,1,0,1):6,#眠二
            (1,0,1,0,0):1,#冲二
            (0,0,1,0,1):1,#冲二
            (1,1,0,0,0):1,#冲二
            (0,0,0,1,1):1,#冲二
            }

    #米字形的矩阵生成，用于优化结构
    def _create_scal(self, n):
        c = int(n/2)
        v = np.zeros((n,n),dtype=np.int32)
        v[c,:],v[:,c] = 1,1
        v = np.eye(n,dtype=np.int32)|np.eye(n,dtype=np.int32)[:,::-1]|v
        return v
    
    #找到一个点所在位置的横竖斜上的所有点以及该点在其array里的坐标
    def _find_crossNslash(self, point):
        oh,ow = self.s_map.shape
        h,w = point
        self._lu = np.eye(oh,ow,w-h).astype(np.bool8)
        self._ru = np.eye(oh,ow,ow-w-1-h).astype(np.bool8)[:,::-1]
        ph,harray = w,self.s_map[h,:]
        pw,warray = h,self.s_map[:,w]    
        plu,luarray = min((h,w))        ,self.s_map[self._lu]
        pru,ruarray = min((h,ow-w-1))   ,self.s_map[self._ru]
        return [(ph,harray),(pw,warray),(plu,luarray),(pru,ruarray)]
    
    #判断胜利
    def _jug_win(self, point):
        for idx,arr in self._find_crossNslash(point):
            for i,j in groupby(arr):
                if i!=0 and len(list(j)) >= 5:
                    return i
        return False
    
    #确保游戏没有结束
    #确保当前point没有其他落子
    def play_1_round(self, point, player):
        assert player in [1,2]
        if self.s_map[point] != 0:
            return False
        self.s_map[point] = player
        self._area_eval_add(point)
        self.win = self._jug_win(point)
        return True

    #根据自身修正 array 排除对手棋子的干扰
    def _revise_array(self, idx, arr, player):
        k = 3 - player
        v = np.where(arr[:idx]==k)[0]
        minx = v.max() + 1 if len(v) else 0
        ridx = idx - minx if len(v) else idx
        v = np.where(arr[idx:]==k)[0]
        maxx = v.min() + idx if len(v) else len(arr)
        return ridx,arr[minx:maxx]

    #估值算法
    def evaluate(self, point, player):
        assert self.s_map[point] == 0 #函数只估值未下过棋的点
        self.s_map[point] = player
        core = 0
        for idx,arr in self._find_crossNslash(point):
            idx,arr = self._revise_array(idx, arr, player)
            _core_list = []
            for val in self._values:
                iidx = idx - len(val)+1 if idx - len(val)+1 > 0 else 0
                jidx = idx + 1
                _val = np.array(val) * player
                for i in range(iidx,jidx):
                    _arr = arr[i:i+len(_val)]
                    if len(_arr) == len(_val) and np.any(_arr^_val)==False:
                        _core_list.append(self._values[val])
            core += max(_core_list) if len(_core_list) else 0
        #估值结束再把 s_map 原本样子还回去
        self.s_map[point] = 0
        return core

    #需要计算估值的范围
    def _area_eval_add(self, point):
        ph,pw = point
        (u,l) = np.maximum(np.array(point)-2, 0)
        (d,r) = np.minimum(np.array(point)+3, self.s_map.shape)
        gu,gl,gd,gr = 2-(ph-u), 2-(pw-l), 2+(d-ph), 2+(r-pw)
        self._area_eval[u:d,l:r] |= self._scal_eval[gu:gd,gl:gr]

    #test 一层的逻辑
    def robot_1(self, player):
        self._temp1_eval_map = np.zeros(self.s_map.shape).astype(np.int32)
        self._temp2_eval_map = np.zeros(self.s_map.shape).astype(np.int32)
        for i,j in np.vstack(np.where(self._area_eval==1)).transpose():
            if self.s_map[i,j] == 0:
                self._temp1_eval_map[i,j] = self.evaluate((i,j),player)
        for i,j in np.vstack(np.where(self._area_eval==1)).transpose():
            if self.s_map[i,j] == 0:
                self._temp2_eval_map[i,j] = self.evaluate((i,j),3-player)
        v = (self._temp1_eval_map+self._temp2_eval_map)
        v = np.vstack(np.where(v==v.max())).transpose()
        v = v[np.random.choice(range(len(v)))]
        return v
        

#test
if __name__== '__main__':
    wzq = WZQ(15,15)
    player = 2
    print(wzq.play_1_round((0,6),1))
    print(wzq.play_1_round((1,4),1))
    print(wzq.play_1_round((3,2),1))
    print(wzq.play_1_round((3,7),1))
    print(wzq.play_1_round((6,4),1))
    print(wzq.play_1_round((1,5),player))
    print(wzq.play_1_round((2,4),player))
    print(wzq.play_1_round((3,3),player))
    print(wzq.play_1_round((3,5),player))
    print(wzq.play_1_round((4,2),player))
    print(wzq.play_1_round((4,4),player))
    print(wzq.play_1_round((3,4),player))
    print(wzq.play_1_round((12,12),player))
    print(wzq.s_map)
    import time
    _t = time.time()
    print(wzq.evaluate((2,2),2))
    h,w = wzq.s_map.shape
    v = np.zeros(wzq.s_map.shape).astype(np.int32)
    for i,j in np.vstack(np.where(wzq._area_eval==1)).transpose():
        if wzq.s_map[i,j] == 0:
            v[i,j] = wzq.evaluate((i,j),2)
    print(v)
    print(time.time()-_t)
