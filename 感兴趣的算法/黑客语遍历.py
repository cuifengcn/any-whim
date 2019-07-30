import zlib
import base64
import itertools

zpasslist = (
    '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'
)

def map_pass_leet(string, mode='hard'):
    def create_leet(string, mode='hard'):
        '''
        这里即便是 hard 模式也没有使用遍历处理方式，
        因为那样对数据的膨胀过大，所以这里暂时就选择了一个更加折中的办法进行处理
        '''
        easy = dict(
            A = ['4'],
            B = ['8'],
            C = [],
            D = [],
            E = ['3'],
            F = [],
            G = ['6'],
            H = [],
            I = [],
            J = [],
            K = [],
            L = ['1'],
            M = [],
            N = [],
            O = ['0'],
            P = [],
            Q = [],
            R = ['2'],
            S = ['5'],
            T = ['7'],
            U = ['v'],
            V = [],
            W = [],
            X = [],
            Y = [],
            Z = ['2'],
        )
        hard = dict(
            A = ['4', '@'],
            B = ['8'],
            C = ['('],
            D = [')'],
            E = ['3'],
            F = [],
            G = ['6'],
            H = ['#'],
            I = [],
            J = [],
            K = [],
            L = ['1', '|'],
            M = [],
            N = [],
            O = ['0'],
            P = ['9'],
            Q = ['&'],
            R = ['2'],
            S = ['5', '$'],
            T = [],
            U = ['v'],
            V = [],
            W = [],
            X = [],
            Y = [],
            Z = ['2', '%'],
        )
        if mode == 'easy': _mode = easy
        if mode == 'hard': _mode = hard
        rr = [[]]
        r = []
        q = []
        for i in string:
            if i.upper() in _mode and i.upper() not in q and _mode[i.upper()]:
                q.append(i.upper())
                r.append([i.upper(), _mode[i.upper()][0]])
        for l in range(1, len(r)+1):
            for i in itertools.combinations(r,l):
                rr.append(i)
        e = []
        q = []
        if ('A' in string.upper() or \
            'L' in string.upper() or \
            'S' in string.upper()) and \
            mode == 'hard':
            for i in string:
                if i.upper() in _mode and i.upper() not in q and _mode[i.upper()]:
                    q.append(i.upper())
                    e.append([i.upper(), _mode[i.upper()][-1]])
        for l in range(1, len(e)+1):
            for i in itertools.combinations(e, l):
                if any([i[0].upper() in 'ALS' for i in i]):
                    rr.append(i)
        return rr
    passlist = []
    for i in create_leet(string, mode):
        s = string
        i = dict(i)
        for j in string:
            if j.upper() in i:
                s = s.replace(j, i[j.upper()])
        passlist.append(s)
    return passlist

if __name__ == '__main__':
    # 这里解压出的 zpasslist 是从 sqlmap 中获取到的密码字典
    # 大约 4000+ 条密码数据。
    zpasslist = base64.b64decode(zpasslist.encode())
    zpasslist = zlib.decompress(zpasslist, -15).decode().splitlines()

    # 通过 map_pass_leet 函数将每个密码的常见的黑客语的各种可能组合的映射遍历出来，让字典更具备鲁棒性
    # 用 zpasslist 进行测试，easy 模式膨胀度约 15 倍，hard 模式膨胀度大约为 30 倍。
    passlist = ['sysadmin', '000000', 'password']
    passlist = zpasslist
    q = []
    for i in passlist:
        for j in map_pass_leet(i, 'hard'):
            q.append(j)

    # 简单的彩虹表测试
    import hashlib
    for i in q:
        v = hashlib.md5(i.encode()).hexdigest()
        print(v, i)