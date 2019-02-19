# 快速幂
def qk_pow(a,b):
    ans = 1
    while b>0:
        if b & 1:
            ans *= a
        a *= a
        b >>= 1
    return ans

# 快速幂取模
def qk_pow_mod(a,b,m):
    ans = 1
    while b>0:
        if b & 1:
            ans = a * ans % m
        a = a * a % m
        b >>= 1
    return ans

v = qk_pow(2,8)
q = qk_pow_mod(2,1000000000,100)

print(v)
print(q)
