

# 关于 sojson 的处理方式，通常来说不难，
# 需要配置部分参数以及将通过原始代码自动生成部分 python 代码
# 合并那部分代码之后使用即可。
# 注意下面的每一块的代码的注释部分，每个部分都说明了 sojson 代码需要配置或处理的地方


















# sojson 需要配置的参数，不同的 sojson 版本可能不一样，这部分的参数很明显
# 加载到 sojson 的加密函数模块的时候，会有一个闭包来修改原始的偏移
# 并且这里做了简单的反爬虫处理，如果不是浏览器，这里的偏移很可能失败，造成后续解码寻址的错误
init_str = ["w6AqDcObOxDDnw==", "bgDClUzCgBB7", "w64RAsK7w6rDs8KF", "w7XDssKsw5/DrUMN", "wpbCu0rDhsKY", "UA0+J2I=", "bxDCh1PClQE=", "HcKGwp85wr4=", "I8KYwowEwok=", "wrJrwpsBFHs=", "wqNQSsKmw5Q=", "woHDoBoMw7g=", "A8KnwpkEwoQ0", "w75YeGXDtMOb", "HsOvwpd+wok=", "wpsLw75gw553Jg==", "TsK7w5MtI8Oa", "w58hMw/ChA==", "wro+w7Jbw7w=", "eFx6fcKR", "w4nCusKhGQLDnQ==", "wpHCisK2SsKp", "fMOsS8OMMQ==", "HcKIwpXChMOW", "PMOkwphkwq0=", "PArCtcKfHw==", "w6bCpm8dw45ZYw==", "djZkw5XDig==", "AsKrwo8cwrs=", "wrfCqsK2XcO3", "FMOvwqhNwrE=", "VznCscKHwoo=", "CA0rVsKp", "b0k/w68LMA==", "fsOUSsOcNw==", "w4/CuCHClWI=", "w54eFsKuw54=", "wrtqwpsxBg==", "SsO9w75fw4jCi3oxEQ==", "FcO5wrZVwpXCrk9IGA==", "wrPDhggNw7U=", "5Li26IK35YqS6ZujRiVFw7LCrzzCo3DDuw==", "HQYrIsKuChpDw68Qw6JBd0PDqw==", "J8OUwp9iwr/ChiZ2ZMK3cCvCtcKTwpJCwrzCvxA3wpHCiMKxw71Fw7Mgw7/CvSVhPMKHY1TDgsOmw47DhcKgDB7DnMKowpHDryp1aVMJw4/DtsK5w5nDiBbDkkZhwoZvfcOSXg==", "w5tAPMO4w5TDtcK7AsK8AA3DkcKUDCU0", "wqNDwp/DrMKqGjnCosOeRsOcYATDoA==", "dTzCjULCsQ==", "wpHCrsOtwoPDuQ==", "wq3CssKHKCE=", "fQnCisKpwpw=", "KCLCsMKIIQ==", "w4hHUHDDlg==", "wrDDmDkHw64=", "w6tfdXvDg8OBZsKLwp7DjzM3", "J8KgwrQQwoY=", "Uw59w4jDgh3DjFRhw7w=", "wqTCt8KEbcKJ", "G8KIw5bCmMOQ", "wo3CuMKgbMKrDA==", "fMK+w54zOQ==", "XEwrWHc=", "wr3CuF7DnsK3w5s9XhYA", "wog8w6zDncKJ", "w4vDlMKwG8KSwpk=", "w6liwrd/wrU=", "LS07fMKo", "w6HCuxDCsUIP", "cXnDiMOobw==", "ccKgw54WBg==", "wp/DkBXCmMOf", "w4NueUPDiw==", "NsKRwrI/wpo=", "MsKOwpvCvsOEKV3CgMKIwqY=", "CsOdwp90wqw=", "PTfCtMK6Ig==", "YyNcOcOp", "wr7DjwMYw7U4", "w7jClsKRBsKXw6fCucK5QsKR", "RC/CoHLCsA==", "wpPCisKtFzPCmB7DvXBYw7lO", "QkUnQkw=", "wpzCuMORw4zDkS5eW8Ozw4cgw5A=", "wrLCm3zDvsKi", "w50NW8KLXg==", "w6JtwpJ3wpU=", "Q8OnRsOEIQ==", "XTjDncOqdiJOw7PCgz3DqWM=", "w6zCnxXCm3o=", "Z3hiRsK5", "wrTDmAISw4I4w67Dq8Oww6rDp8Ox", "wohuYcKmw4o=", "w6kSDTbCug==", "w43CrXQBw7Y=", "w4PCrcKgEzXDnXXCuMODPMK7wrw=", "wo/CkcKqU8Km", "Yz4VPV0=", "w5nCiV4bw7Y=", "w7fDosKvw5s=", "GRrCk8KDNw=="]
init_num = 339
init_str = init_str[init_num%len(init_str):] + init_str[:init_num%len(init_str)]




















import base64
def rc4(data, key):
    data = bytes(ord(i) for i in base64.b64decode(data).decode())
    S, j, key = list(range(256)), 0, key.encode()
    for i in range(256):
        j = (j + S[i] + key[i%len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i, j = 0, 0
    R = []
    for c in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = c ^ (S[(S[i] + S[j]) % 256])
        R.append(t)
    return bytes(R).decode()
def sojsonrc4(idxstr, key):
    return rc4(init_str[int(idxstr, 16)], key)

# 上面则是 sojson 寻参解码函数，需要小心处理
# sojson 带有一个解码函数，在不同版本里面的函数名字可能不一样，
# 所以这里就需要针对不同版本的函数名字处理，使用这个函数名会对后续的处理有帮助
_0x53a5 = sojsonrc4




























code = '''
var D = {
    iYhbP: _0x53a5("0x0", "v4z2"),
    XJERQ: function I(ah, ai) {
        return ah > ai
    },
    DcjIe: function m(ai, ah) {
        return ai % ah
    },
    brTxo: function Z(ah, ai) {
        return ah + ai
    },
    EjJfV: function s(ai, ah) {
        return ai % ah
    },
    WrOgv: function A(ai, ah) {
        return ai ^ ah
    },
    SJwsy: function B(ai, ah) {
        return ai + ah
    },
    Apomn: function ad(ai, ah) {
        return ai >= ah
    },
    FCIHj: function E(ah, ai) {
        return ah % ai
    },
    ILJTB: _0x53a5("0x1", "$QKE"),
    gDfZv: function l(ai, ah) {
        return ai | ah
    },
    eyIJG: function x(ah, ai) {
        return ah & ai
    },
    LnoHQ: function N(ai, ah) {
        return ai >> ah
    },
    URSQx: function o(ai, ah) {
        return ai - ah
    },
    NCcUK: function V(ah, ai) {
        return ah * ai
    },
    lKCRV: function b(ah, ai) {
        return ah | ai
    },
    wgPJl: function g(ai, ah) {
        return ai << ah
    },
    HYDgv: function e(ah, ai) {
        return ah < ai
    },
    nLdXy: function M(ai, ah) {
        return ai | ah
    },
    Hkujl: function u(ai, ah) {
        return ai(ah)
    },
    VJbPx: _0x53a5("0x2", "mwuw"),
    mTdNN: function Y(ai, ah) {
        return ai(ah)
    },
    ErOXg: function W(ai, ah) {
        return ai(ah)
    },
    xyKXs: function T(ai, ah) {
        return ai(ah)
    },
    FPxoK: function L(ah, ai) {
        return ah(ai)
    },
    pWxAv: function af(ah, ai) {
        return ah + ai
    },
    ZrDBW: function X(ai, ah) {
        return ai + ah
    },
    vZQoQ: function P(ai, ah) {
        return ai / ah
    },
    rytkK: function h(ah, ai) {
        return ah + ai
    },
    nSQgs: function F(ah, ai) {
        return ah + ai
    },
    ccYbk: _0x53a5("0x3", "Afds"),
    MkPVa: function C(ai, ah) {
        return ai % ah
    },
    BjdyU: function a(ah, ai) {
        return ah + ai
    },
    ztbCf: function k(ai, ah) {
        return ai + ah
    }
};
'''
def create_code(code):
    import re
    code = re.sub(r'\{ *\n *', ':', code)
    code = re.sub(r'\n *},', '', code)
    code = re.sub(r', *\n', '\n', code)
    ls, fn = [], []
    for i in code.splitlines():
        if re.findall(r'\w{5}: ', i):
            ls.append(re.sub(r'.*(\w{5}): ', r'D["\1"]: ', i.lstrip(), count=1))
            if 'function' in i: 
                fn.append(i.lstrip()[7:].replace('function', 'def'))
    for idx, i in enumerate(ls): 
        ls[idx] = re.sub(r': function (\w+)\([^\(\)]+\).*', r' = \1', i)
        ls[idx] = re.sub(r': (.*)', r' = \1', ls[idx])
    for i in fn: print(i)
    print('D = {}')
    for i in ls: print(i)
create_code(code)

# 在代码内一定会遇到部分 create_code 函数以前的，类似 code 字符串的 js 代码，
# create_code 直接执行会自动打印出结果，打印出的结果就是新的代码，
# 然后将 该处的 code 以及 create_code 部分删除并将生成的代码粘贴到该处即可
# 代码结果类似下面的部分，遇到不同的部分函数结果注意修改即可

def I(ah, ai) :return ah > ai
def m(ai, ah) :return ai % ah
def Z(ah, ai) :return ah + ai
def s(ai, ah) :return ai % ah
def A(ai, ah) :return ai ^ ah
def B(ai, ah) :return ai + ah
def ad(ai, ah) :return ai >= ah
def E(ah, ai) :return ah % ai
def l(ai, ah) :return ai | ah
def x(ah, ai) :return ah & ai
def N(ai, ah) :return ai >> ah
def o(ai, ah) :return ai - ah
def V(ah, ai) :return ah * ai
def b(ah, ai) :return ah | ai
def g(ai, ah) :return ai << ah
def e(ah, ai) :return ah < ai
def M(ai, ah) :return ai | ah
def u(ai, ah) :return ai(ah)
def Y(ai, ah) :return ai(ah)
def W(ai, ah) :return ai(ah)
def T(ai, ah) :return ai(ah)
def L(ah, ai) :return ah(ai)
def af(ah, ai) :return ah + ai
def X(ai, ah) :return ai + ah
def P(ai, ah) :return ai / ah
def h(ah, ai) :return ah + ai
def F(ah, ai) :return ah + ai
def C(ai, ah) :return ai % ah
def a(ah, ai) :return ah + ai
def k(ai, ah) :return ai + ah
D = {}
D["XJERQ"] = I
D["DcjIe"] = m
D["brTxo"] = Z
D["EjJfV"] = s
D["WrOgv"] = A
D["SJwsy"] = B
D["Apomn"] = ad
D["FCIHj"] = E
D["ILJTB"]: _0x53a5("0x1", "$QKE")
D["gDfZv"] = l
D["eyIJG"] = x
D["LnoHQ"] = N
D["URSQx"] = o
D["NCcUK"] = V
D["lKCRV"] = b
D["wgPJl"] = g
D["HYDgv"] = e
D["nLdXy"] = M
D["Hkujl"] = u
D["VJbPx"]: _0x53a5("0x2", "mwuw")
D["mTdNN"] = Y
D["ErOXg"] = W
D["xyKXs"] = T
D["FPxoK"] = L
D["pWxAv"] = af
D["ZrDBW"] = X
D["vZQoQ"] = P
D["rytkK"] = h
D["nSQgs"] = F
D["ccYbk"]: _0x53a5("0x3", "Afds")
D["MkPVa"] = C
D["BjdyU"] = a
D["ztbCf"] = k












s = r'''
        while (!![]) {
            switch (H[i++]) {
            case "0":
                for (G = "",
                r = 0,
                K = 0,
                R = 0; D[_0x53a5("0x6", "Zipd")](O, R); R++) {
                    r = D[_0x53a5("0x7", "HdYa")](D[_0x53a5("0x8", "aJF)")](r, 1), 256),
                    K = D[_0x53a5("0x9", "ArEd")](D[_0x53a5("0xa", "$WyH")](K, Q[r]), 256),
                    n = Q[r],
                    Q[r] = Q[K],
                    Q[K] = n,
                    G += String[_0x53a5("0xb", "ArEd")](D[_0x53a5("0xc", "[I(U")](ae[R][_0x53a5("0xd", "#7C5")](), Q[D[_0x53a5("0xe", "I*O3")](D[_0x53a5("0xf", "d12c")](Q[r], Q[K]), 256)]))
                }
                continue;
            case "1":
                for (O = ae[_0x53a5("0x10", "I*O3")],
                aa = [],
                R = 0; D[_0x53a5("0x11", "8H#C")](255, R); R++) {
                    aa[R] = d[D[_0x53a5("0x12", "UU0z")](R, v)][_0x53a5("0x13", "@l$z")]()
                }
                continue;
            case "2":
                for (c = D[_0x53a5("0x14", "Afds")],
                y = 0,
                p = c,
                z = ""; G[_0x53a5("0x15", "tqAr")](D[_0x53a5("0x16", "FFp1")](0, y)) || (p = "=",
                D[_0x53a5("0x17", "1VKJ")](y, 1)); z += p[_0x53a5("0x18", "2)Vk")](D[_0x53a5("0x19", "tMcV")](63, D[_0x53a5("0x1a", "8H#C")](J, D[_0x53a5("0x1b", "QWU)")](8, D[_0x53a5("0x1c", "ArEd")](8, D[_0x53a5("0x1d", "[I(U")](y, 1))))))) {
                    q = G[_0x53a5("0x1e", "%GFP")](y += 0.75),
                    J = D[_0x53a5("0x1f", "$QKE")](D[_0x53a5("0x20", "aJF)")](J, 8), q)
                }
                continue;
            case "3":
                for (j = 0; D[_0x53a5("0x21", "v4z2")](j, t[_0x53a5("0x22", "$WyH")]); j++) {
                    ac = t[_0x53a5("0x23", "T%I]")](j),
                    D[_0x53a5("0x24", "H!NY")](128, ac) ? ae += String[_0x53a5("0x25", "Zipd")](ac) : D[_0x53a5("0x26", "UU0z")](ac, 127) && D[_0x53a5("0x26", "UU0z")](2048, ac) ? (ae += String[_0x53a5("0x27", "eQ8K")](D[_0x53a5("0x28", "@l$z")](192, D[_0x53a5("0x29", "NJBx")](ac, 6))),
                    ae += String[_0x53a5("0x25", "Zipd")](D[_0x53a5("0x2a", "FFp1")](128, D[_0x53a5("0x2b", "vkS%")](63, ac)))) : (ae += String[_0x53a5("0x2c", "s^8S")](D[_0x53a5("0x2d", "2)Vk")](224, D[_0x53a5("0x2e", "kjv)")](ac, 12))),
                    ae += String[_0x53a5("0x2f", "$WyH")](D[_0x53a5("0x30", "!tw2")](128, D[_0x53a5("0x31", "8XxX")](63, D[_0x53a5("0x32", "spiQ")](ac, 6)))),
                    ae += String[_0x53a5("0x33", "RF]N")](D[_0x53a5("0x34", "I*O3")](128, D[_0x53a5("0x35", "l(8Z")](63, ac))))
                }
                continue;
            case "4":
                for (Q = [],
                R = 0; D[_0x53a5("0x36", "spiQ")](256, R); R++) {
                    Q[_0x53a5("0x37", "vrDG")](R)
                }
                continue;
            case "5":
                return G = D[_0x53a5("0x38", "aJF)")](S, z[_0x53a5("0x39", "$J^e")](/=/g, ""))[_0x53a5("0x3a", "H!NY")](/\+/g, "-")[_0x53a5("0x3b", "mwuw")](/\//g, "_")[_0x53a5("0x3c", "vrDG")](/=/g, ".");
            case "6":
                var j, ac, O, aa, R, Q, K, n, G, r, c, J, q, y, p, z, ab = 4, f = D[_0x53a5("0x3d", "@l$z")](md5, D[_0x53a5("0x3e", "l(8Z")])[_0x53a5("0x3f", "H!NY")](0, 30), U = D[_0x53a5("0x40", "[I(U")](md5, D[_0x53a5("0x41", "[I(U")](f, "9b")[_0x53a5("0x42", "R%HY")](0, 16)), w = D[_0x53a5("0x43", "!tw2")](md5, D[_0x53a5("0x44", "$WyH")](f, "9b")[_0x53a5("0x45", "[I(U")](16, 32))[_0x53a5("0x46", "ArEd")](0, 16), S = D[_0x53a5("0x47", "$QKE")](md5, new Date()[_0x53a5("0x48", "Ec8P")]())[_0x53a5("0x49", "8H#C")](-ab), d = D[_0x53a5("0x4a", "8XxX")](U, D[_0x53a5("0x4b", "Ec8P")](md5, D[_0x53a5("0x4c", "kjv)")](U, S))), v = d[_0x53a5("0x4d", "RF]N")], t = D[_0x53a5("0x4e", "I*O3")](D[_0x53a5("0x4f", "vkS%")](D[_0x53a5("0x50", "%GFP")](D[_0x53a5("0x51", "$QKE")](D[_0x53a5("0x52", "aJF)")](new Date()[_0x53a5("0x53", "spiQ")](), 1000), 86400), 0), D[_0x53a5("0x54", "#7C5")](md5, D[_0x53a5("0x55", "[I(U")](ag, D[_0x53a5("0x56", ")dGK")](D[_0x53a5("0x57", "$QKE")](D[_0x53a5("0x58", "HdYa")](w, 5), D[_0x53a5("0x59", "1VKJ")]), 3)))[_0x53a5("0x5a", "DW9@")](0, 16)), ag), ae = "";
                continue;
            case "7":
                for (K = 0,
                R = 0; D[_0x53a5("0x5b", "vkS%")](256, R); R++) {
                    K = D[_0x53a5("0x5c", "2)Vk")](D[_0x53a5("0x5d", "mwuw")](D[_0x53a5("0x5e", "R%HY")](K, Q[R]), aa[R]), 256),
                    n = Q[R],
                    Q[R] = Q[K],
                    Q[K] = n
                }
                continue
            }
            break
        }
    }
'''



import re
def replace_rc4(e):
    try:
        return repr(eval(e.group(0)))
    except:
        print('error:', e.group(0))
        return e.group(0)
v = re.sub(r'_0x53a5\([^\(\)]+, *".{4}"\)', replace_rc4, s)
print(v)
