# 文书网混合压缩加密

import base64
import zlib

def deflate_and_base64_encode(string_val):
    zlibbed_str = zlib.compress(string_val.encode())[2:-4]
    cb_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    def cb_encode(t):
        p = [0,2,1][len(t)%3]
        q = (t[0]<<16) + ((t[1] if len(t)>1 else 0)<<8) + (t[2] if len(t)>2 else 0)
        l = ''.join([ cb_string[q>>18],
                      cb_string[(q>>12)&63],
                      '=' if p>=2 else cb_string[(q>>6)&63],
                      '=' if p>=1 else cb_string[q&63], ])
        return l
    def cb_utob(t):
        r = []
        for i in t:
            q = [i] if i < 127 else [(0xc0 | (i>>6)), (0x80 | (i&0x3f))]
            r.extend(q)
        return bytes(r)
    zlibbed_str = cb_utob(zlibbed_str)
    finstring = ''
    for i in range(0,len(zlibbed_str),3):
        finstring += cb_encode(zlibbed_str[i:i+3])
    return finstring

def decode_base64_and_inflate(b64string):
    cb_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    cb_tab, idx = {}, 0
    for i in cb_string:
        cb_tab[i] = idx
        idx += 1
    def cb_decode(t):
        l = len(t)
        q = ((cb_tab[t[0]] << 18) if l>0 and t[0] in cb_tab else 0) + \
            ((cb_tab[t[1]] << 12) if l>1 and t[1] in cb_tab else 0) + \
            ((cb_tab[t[2]] << 6 ) if l>2 and t[2] in cb_tab else 0) + \
            (cb_tab[t[3]]         if l>3 and t[3] in cb_tab else 0)
        c = [(q>>16), ((q>>8)&0xff), (q&0xff)]
        return c
    lrange1 = list(range(0xC0, 0xDF+1))
    lrange2 = list(range(0x80, 0xBF+1))
    def cb_btou(t):
        ret, idx = [], 0
        for i in range(0,len(t)):
            if t[i] in lrange1 and t[i+1] in lrange2:
                ret.append(((t[i]&0x1f)<<6) + (0x3f&t[i+1]))
                idx = i+2
            elif i>=idx:
                ret.append(t[i])
        return ret
    cb_data = []
    for i in range(0, len(b64string), 4):
        cb_data.extend(cb_decode(b64string[i:i+4]))
    return zlib.decompress(bytes(cb_btou(cb_data)),-15).decode()

# 这里是通过自己的函数处理生成的密文。加密逻辑现在已经理清，后续的解密逻辑相信也不会太难。
data = 'this is a original data.'
print('original:',data)
v = deflate_and_base64_encode(data); print('_wenshu_mix_deflate_b64:',v)
v = decode_base64_and_inflate(v);    print('_wenshu_mix_inflate_b64:',v)

# 这里是文书网的部分加密的数据，解密后是一个jsfuck的加密
runeval = 'w61aw4tuw4IwEMO8wpYgDsK2UsO1ByJOfALDh8KVFcKhQCEHSGXDkhPDosOfwpvCpMOUw43DgxDDk8OYw4HDgEjDkcKiw4TCuzvCs8OjwrfDhHTCm8Kuw5bCh0TCpsKfw7lswpHDi3TCv3nDv8KQw5luwr5dw4p5wrZawrMwCEnDgHhtw54gAsOMa8KMwpBnKMOkRcKmK1Ylw7QtDHTCh8KyMMOoPSjChsOOwoUcw5AESkAdCMKDwoJRP0rChwjCqBo6wqE4wpTChB7CgMOBQMOww5DDsCjCimfCkyTDmx9yw7nClcOkwpnCnEQxw4XCongYC8KPwqfDkk09w4cTwqfCn0gqwowQIQvCqgZOw43CnGVDf0vDtTrDvcO7dwLCscOyc8OhQUHDmULCgsKKwp8WYMOTPTgHXAZrw7HDlsO6XsOlVMOPwqbDv8KuwqAqw5Zdwok6FMK0NVzDicKtSMKaKVp7w63CpW3DqHHCi8Obw43CvsO/CxgQNTTDlErCvMK9JMKWM8K1R8Kbw73DpD0Tw4Y+wpYCVDPDkcKVbm57w6VOEE/CiWMZw4zDvcKEGV82NWN+d8OiRsK1BlvCrsKRwr8Lw55eLcONGlVHXcO4w4Yqwqx/HMOZX3ldL8OfwqPDr1EeHEosw4PDnsKJwpNbw6xHPjY8w7zCkcOHcwJnFsKsdQszwrpjesKpwpfDpkrDmSnCjhoHBcO9w5d6QhpwKcO2SDzDsMKpw4Fyw4bCo28='
v = decode_base64_and_inflate(runeval)
print('jsfuck:',v)
