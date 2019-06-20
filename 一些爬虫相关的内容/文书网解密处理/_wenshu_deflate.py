# 文书网 deflate 混合加解密的函数处理

import base64
import zlib

data = r"""setTimeout('$("#resultList").css("height", "500px").css("font-size", "18px");$("#resultList").html("\u7cfb\u7edf\u7e41\u5fd9\uff0c\u8bf7\u60a8\u7a0d\u540e\u518d\u8bd5\u3002");',100)"""

def deflate_and_base64_encode(string_val,level=-1):
    zlibbed_str = zlib.compress(string_val,level=level)[2:-4]
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
    decoded_data = base64.b64decode(b64string)
    print('===',len(b64(decoded_data)),b64(decoded_data))
    return zlib.decompress(decoded_data,-15)

# 这里是通过自己的函数处理生成的密文。加密逻辑现在已经理清，后续的解密逻辑相信也不会太难。
v = deflate_and_base64_encode(data.encode(),6)
print(v,len(v))

# 这里是需要破解的js文件里面通过 s 算出来的密文。
s = 'ZcONTQrDgjAQwobDocKrSBTCmkLClcKJw7Ynw6IVXMK6w4zCpm1mbMKgwrViZkA8wr3DicOCwpXCm3cxD3wTwpFvYcOBVVgXO8KtwrYvwowyw7M1RFbDpWHCjFHCqwnDg31iVW1UA8OwfMO/w47CtD54H8ODB8KzGMKbw6HDsjcww7Eya8OlwqQbaUhFT8K5wrVxw5LCkD87IcKCw5HCiR3CqHPDkkJvwpPDtsOgwpPDlsKAwqnDhsO6wqzCvnFyAjjCpg9FZQDDii8='
print(s,len(s))
