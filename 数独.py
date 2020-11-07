class Mat:
    def __init__(self, mx):
        self.mx = mx
        self.ret = None
        self.dct = self.init9x9pos()
        self.pos = self.get9x9pos()
        self.cnt = 0
    def __str__(self,):
        ret = []
        for i in self.mx:
            ret.append(' '.join('{:2s}'.format(str(j) if j else '_') for j in i))
        return '\n'.join(ret)
    def init9x9pos(self):
        pos_val = {}
        for y in range(len(self.mx)):
            for x in range(len(self.mx[0])):
                if self.mx[y][x] == 0:
                    rest = self.get_rest_list(x, y)
                    # import random
                    # random.shuffle(rest)
                    pos_val[(x, y)] = rest
        return pos_val
    def get9x9pos(self):
        pos_val = self.dct.items()
        pos_val = sorted(pos_val, key=lambda i:len(i[1]))
        pos = [pos[0] for pos in pos_val]
        return pos
    def get9x9(self, num=None, pidx=0):
        self.cnt += 1
        if pidx >= (num if num else len(self.pos)):
            print('cost:', self.cnt)
            return self.mx
        for x, y in self.pos[pidx:]:
            for key in self.get_rest_list(x, y, self.dct):
                self.mx[y][x] = key
                ret = self.get9x9(num=num, pidx=pidx+1)
                if ret:
                    return ret
                else:
                    self.mx[y][x] = 0
            return
    def get_rest_list(self, x, y, dct=None):
        anum = []
        for i in self.mx[y]:
            if i:
                anum.append(i)
        for i in self.mx:
            if i[x]:
                anum.append(i[x])
        if x >= 0 and x < 3: rngx = [0,1,2]
        if x >= 3 and x < 6: rngx = [3,4,5]
        if x >= 6 and x < 9: rngx = [6,7,8]
        if y >= 0 and y < 3: rngy = [0,1,2]
        if y >= 3 and y < 6: rngy = [3,4,5]
        if y >= 6 and y < 9: rngy = [6,7,8]
        for _x in rngx:
            for _y in rngy:
                if self.mx[_y][_x]:
                    anum.append(self.mx[_y][_x])
        rest = []
        for i in dct[(x, y)] if dct else range(1, 10):
            if i not in anum:
                rest.append(i)
        return rest

s = [
    [0,0,0,  8,0,0,  0,0,0],
    [0,0,0,  5,6,0,  0,9,0],
    [0,0,7,  0,0,0,  2,0,0],
    [8,0,0,  0,0,0,  0,0,0],
    [5,0,0,  1,0,0,  0,0,0],
    [0,0,0,  0,2,0,  4,0,7],
    [0,0,0,  0,0,0,  0,1,0],
    [0,0,4,  0,0,0,  0,0,0],
    [3,0,0,  0,0,0,  0,5,8],
]
# s = [
#     [8,0,0,  0,0,0,  0,0,0],
#     [0,0,3,  6,0,0,  0,0,0],
#     [0,7,0,  0,9,0,  2,0,0],
#     [0,5,0,  0,0,7,  0,0,0],
#     [0,0,0,  8,4,5,  7,0,0],
#     [0,0,0,  1,0,0,  0,3,0],
#     [0,0,1,  0,0,0,  0,6,8],
#     [0,0,8,  5,0,0,  0,1,0],
#     [0,9,0,  0,0,0,  4,0,0]
# ]

s = Mat(s)
v = s.get9x9()
print(s)