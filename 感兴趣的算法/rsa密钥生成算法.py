# 根据二进制数字长度需求生成rsa密钥，length需要为2的倍数
def create_rsa_key(length=1024):
    # miller-rabin 算法素性检测
    def isprime_mr(a,b=None):
        # 暂时选一百以内的全部素数作为检测标准
        # 目前不太清楚“标准算法”里面如何选取 miller-rabin 检测数，不过以以下检测数作检测目前没出现过错误
        if b is None: b = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
        if a == 2:return True
        if a%2==0 or a==1:return False
        for x in b:
            t = a - 1
            while t%2 == 0:
                v = pow(x,t,a)# python自带函数pow就带有快速幂取模功能
                if v not in [0,1,a-1]:
                    return False
                else:
                    if v in [0,a-1]: break
                    t //= 2
        return True
    # 根据长度随机迭代，获取质数
    import random
    def get_prime(halflen):
        rd = random.randint(1<<(halflen-1),1<<(halflen))
        rd = rd+1 if rd%2==0 else rd
        while True:
            rd += 2
            if isprime_mr(rd):
                return rd
    # 确保公共参数n的位数，以便保证密钥长度。
    while True:
        p = get_prime(length//2)
        q = get_prime(length//2)
        n = p * q
        if n.bit_length() == length:
            break
    fn  = (p-1) * (q-1)
    # 扩展欧几里得算法获取乘法模逆元
    def ex_gcd(a,b):
        if b == 0:
            return (1,0,a)
        (x, y, r) = ex_gcd(b,a%b)
        t = x
        x = y
        y = t - a//b*y
        return (x,y,r)
    # 由于主动设定了e为素数，所以一次获取肯定能获取到符合要求的模逆元
    # 该数也是一般通用标准，是为了方便计算机计算而选的数字：0x10001==65537
    e = 65537 
    a, b, r = ex_gcd(fn, e)
    d = b + fn
    # 公钥n,e 私钥n,d
    return e,d,n

print('============= test =============')
# 测试rsa密钥生成效率
e,d,n = create_rsa_key(1024)#默认生成1024位的密钥
print('(rsa publicKey n,e) {} --- {}'.format(n,e))
print('(rsa PrivateKey n,d) {} --- {}'.format(n,d))

print('============= test =============')
# 测试rsa密钥加密解密
# rsa可以加解密一个 1024bit 位的数据，所以通常加密数据过长就需要切分处理
def test(o):
    print('(rsa original data) {}'.format(o))
    c = pow(o,e,n)
    v = pow(c,d,n)
    print('(rsa decoding data) {}'.format(v))
    print('(rsa encoding data) {}'.format(c))
    print(len(bin(c)))
    print(len(bin(n)))
test(12345678987654321)
test(11111111111111111222222222222222222222000)
test(33333333333333333333333333333333333333333333333)

