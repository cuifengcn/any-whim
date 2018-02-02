import numpy as np
from collections import OrderedDict
from itertools import groupby

# 五子棋类
# 包装了下棋函数，判断是否胜利函数以及估值函数，深度搜索估值函数。
# 下棋函数如果返回值为真则在该点下棋，否则下棋失败（被其他棋子占用）
# 每下一步棋就会更新 self.win 。如果该值不为 False 则为胜利者
# player in[1, 2]
class WZQ:
    def __init__(self, h, w):
        self.s_map = np.zeros((h,w)).astype(np.int32)


        self.h = h
        self.w = w
        self._lu = np.zeros((h,w)).astype(np.bool8)
        self._ru = np.zeros((h,w)).astype(np.bool8)
        self._area_eval = np.zeros((h,w),dtype=np.int32)
        self._scal_eval = self._create_scal(5)
        self._scal_ecal_large = self._create_scal(9)
        self.win = False

        #分值列表，如果有新加入的估值，按照分值顺序插入即可。
        self._values = OrderedDict([
            [(1,1,1,1,1),1000],#活五1000分
            [(1,0,1,1,1,0,1),400],#活四
            [(0,1,1,1,1,0),400],#活四
            [(1,1,1,1,0),100],#冲四
            [(1,1,1,0,1),100],#冲四
            [(1,1,0,1,1),100],#冲四
            [(1,0,1,1,1),100],#冲四
            [(0,1,1,1,1),100],#冲四
            [(0,1,1,1,0,0),100],#活三
            [(0,0,1,1,1,0),100],#活三
            #优冲三：因为这里如果被对手中间截断也能很快再生成冲三，所以分值较高
            [(0,0,0,1,1,0,1),50],#优冲三
            [(1,0,1,1,0,0,0),50],#优冲三
            [(0,0,1,0,1,0,1),30],#优眠三
            [(1,0,1,0,1,0,0),30],#优眠三
            #劣冲三：因为这里如果被对手截断那么在这一维就直接失去价值所以分值低
            [(1,1,1,0,0),20],#劣冲三
            [(0,0,1,1,1),20],#劣冲三
            [(1,1,0,1,0),20],#劣冲三
            [(0,1,0,1,1),20],#劣冲三
            [(0,1,1,0,0),6],#活二
            [(0,0,1,1,0),6],#活二
            [(0,1,0,1,0),6],#活二
            [(1,0,1,0,0),2],#冲二
            [(0,0,1,0,1),2],#冲二
            [(1,1,0,0,0),2],#冲二
            [(0,0,0,1,1),2],#冲二
            [(0,0,0,0,1),1],#一
            [(0,0,0,1,0),1],#一
            [(0,0,1,0,0),1],#一
            [(0,1,0,0,0),1],#一
            [(1,0,0,0,0),1],#一
            ])






    ##ls = []
    ##def some(深度, 范围图, 权重图, ls, chain=[]):
    ##    新的范围图 = 添范围函数(范围图, chain)
    ##    新的权重图 = 添权重函数(权重图, chain)
    ##    ## 这里的400主要是因为这是最接近活五的分值
    ##    if 新的权重图.max() >= 400 or 深度>目标深度:
    ##        对 ls 添加 chain 的信息
    ##        return
    ##    for point in 新的范围图.所有点:
    ##        some(深度, 范围图, 权重图, ls, chain+[point])


    #临时范围图
    def eval_area_add(self, eval_area, chain):
        eval_area = eval_area.copy()
        if chain:
            ph,pw = point = chain[-1]
            (u,l) = np.maximum(np.array(point)-2, 0)
            (d,r) = np.minimum(np.array(point)+3, self.s_map.shape)
            gu,gl,gd,gr = 2-(ph-u), 2-(pw-l), 2+(d-ph), 2+(r-pw)
            eval_area[u:d,l:r] |= self._scal_eval[gu:gd,gl:gr]
        return eval_area

    #临时权重图
    def eval_map_add(self, eval_map, player_chain, chain):
        eval_map = eval_map.copy()
        player = player_chain[len(chain)]
        if chain:
            ph,pw = point = chain[-1]
            (u,l) = np.maximum(np.array(point)-4, 0)
            (d,r) = np.minimum(np.array(point)+5, self.s_map.shape)
            gu,gl,gd,gr = 4-(ph-u), 4-(pw-l), 4+(d-ph), 4+(r-pw)
            z = np.zeros((self.h,self.w),dtype=np.int32)
            z[u:d,l:r] |= self._scal_ecal_large[gu:gd,gl:gr]
            for point in  np.vstack(np.where((z==1)&(self.s_map==0))).transpose():
                eval_map[tuple(point)] = self.evaluate(tuple(point), player)+self.evaluate(tuple(point), 3-player)*.8
        return eval_map

    #棋谱的栈形式的调用push pop, 仅仅使用原有落子图，对计算空间的优化
    def s_map_push(self, player_chain, chain):
        if chain:
            player = player_chain[len(chain)]
            self.s_map[tuple(chain[-1])] = player

    def s_map_pop(self, player_chain, chain):
        if chain:
            player = player_chain[len(chain)]
            self.s_map[tuple(chain[-1])] = 0

    def pred(self, target_deep, player):
        ls = []
        # 考虑到可能会有三手交换之类的规则，下棋顺序 player_chain 以下述方式存放，index==0位不用管
        if player==1: player_chain = [-1]+[1,2]*10
        if player==2: player_chain = [-1]+[2,1]*10

        alpha=float('-inf')
        beta =float('-inf')

        def funcition(deep, eval_area, eval_map, ls, alpha, beta, chain=[], value_chain=[]):
            self.s_map_push(player_chain, chain)
            eval_area = self.eval_area_add(eval_area, chain)#范围图
            eval_map  = self.eval_map_add(eval_map, player_chain, chain)#权重图
            
            if np.any(eval_map >= 400) or deep == target_deep:
                v = np.vstack(np.where(eval_map==eval_map.max())).transpose()
                v = v[np.random.choice(range(len(v)))]
                z = [eval_map[v[0],v[1]]]
                ls+=[(chain+[v],sum(value_chain+z))]
                self.s_map_pop(player_chain, chain)
                return eval_map.max()
            
            print(*chain,*value_chain,alpha,'next lv node num:',len(np.where(eval_area==1)[0]))
            # 最终的算法瓶颈就在 np.vstack(np.where((eval_area==1)&(self.s_map==0))).transpose() 这一句上面
            # 考虑一下，如果将每次下棋时候考虑的点缩小到仅仅只有前一次下棋点的八方向长度为二的点效果会不会更好一些呢？
            # 不过这样的话就会被单方面约束在下棋点周围摇摆，失去另一种策略上的自由
            # 即在对方最高分也很少时候，自己距离最新落子点较为偏僻地方开始反扑的机会
            # 或者就直接选择当前 eval_map 下数值最高的十个的位置，这样就不用考虑太多问题，也能很大程度上约束数量
            
            x = (eval_map!=0)&(self.s_map==0)
            sort_idx = np.argsort(eval_map[x])
            for point in np.vstack(np.where(x)).transpose()[sort_idx][::-1][:10]:
                v = funcition(deep+1, eval_area, eval_map, ls, alpha, beta, chain+[(point)], value_chain+[eval_map[tuple(point)]])
                if v > (alpha if len(chain)%2 else beta):
                    if len(chain)%2:
                        alpha = v
                    else:
                        beta = v
                elif v < (beta if len(chain)%2 else alpha):
                    break

            self.s_map_pop(player_chain, chain)
            return eval_map.max()
        
        funcition(1, self._area_eval, self._calc_eval_map(1), ls, alpha, beta)
        return ls
    #以上深度搜索的大体框架已经完成，目前就是考虑如何将剪枝方式放入以处理速度过慢的情况
    #目前来说，考虑三层就已经需要大约五分钟的时间。
    #返回值ls是以 一个list包含了各种目标深度下各种落子可能
    #【【chain1，value_chain1】，【chain2，value_chain2】，……】
    #加入剪枝处理之后效率提高很多，已经能在 test 的三层中只要13秒的时间。
    #四层以及之后的数量还是非常夸张。
    #最后还是加入了 eval_map 的动态规划处理，对下一步的约束使得考虑的步数大大减少。
    #加入动态规划之后，在test下几乎可以遍历到所有的树梢节点，并且只需要不到五秒。
    #在目前情况下已经很不错了，但是在4层时候还是稍微有点问题，调整完毕会进行总结性的处理。



    

    #米字形的矩阵生成，用于优化计算范围
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
    
    #确保当前point没有其他落子
    #确保每下一步都会更新 self.win 。
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
                        break
                if len(_core_list)!= 0:
                    break
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

    #将估值函数包装一下，使得使用起来会更加方便
    def _calc_eval_map(self, player):
        self._temp1_eval_map = np.zeros(self.s_map.shape).astype(np.int32)
        self._temp2_eval_map = np.zeros(self.s_map.shape).astype(np.int32)
        for i,j in np.vstack(np.where((self._area_eval==1)&(self.s_map==0))).transpose():
            self._temp1_eval_map[i,j] = self.evaluate((i,j),player)
        for i,j in np.vstack(np.where((self._area_eval==1)&(self.s_map==0))).transpose():
            self._temp2_eval_map[i,j] = self.evaluate((i,j),3-player)
        #这里的0.8是为了防止在预测中对手权重过高过度防御导致连自己的连五都被无视
        return (self._temp1_eval_map+self._temp2_eval_map*.8)

    #test 一层的逻辑
    #经过测试，该简单算法不能应对较为复杂的多层考虑，仅仅应用于简单难度
    def robot_level1(self, player):
        v = self._calc_eval_map(player)
        v = np.vstack(np.where(v==v.max())).transpose()
        v = v[np.random.choice(range(len(v)))]
        return v

    def robot_level2(self, player):
        pass
    
        

#以下只用于简单语法错误的检查测试test
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
##    print(wzq.play_1_round((4,2),player))
    print(wzq.play_1_round((4,4),player))
    print(wzq.play_1_round((3,4),player))
    print(wzq.play_1_round((12,12),player))
    print(wzq.play_1_round((14,14),player))
    print(wzq.s_map)
    import time

    _t = time.time()
    print(wzq.evaluate((2,2),2))
    h,w = wzq.s_map.shape
    v = np.zeros(wzq.s_map.shape).astype(np.int32)
    for i,j in np.vstack(np.where(wzq._area_eval==1)).transpose():
        if wzq.s_map[i,j] == 0:
            v[i,j] = wzq.evaluate((i,j),1)
    print(v)
    print(time.time()-_t)

    
    _t = time.time()
    print(wzq._calc_eval_map(2).astype(np.int32))
    print(time.time()-_t)
    _t = time.time()
    v = wzq.pred(4, 1)
    print(len(v))
    print(time.time()-_t)
