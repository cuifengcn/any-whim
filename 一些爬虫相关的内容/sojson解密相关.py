

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
        if re.findall(r'^ *\w{5}: ', i):
            ls.append(re.sub(r'^(\w{5})', r'D["\1"]', i.lstrip()))
            if 'function' in i: 
                fn.append(i.lstrip()[7:].replace('function', 'def'))
    for idx, i in enumerate(ls): 
        ls[idx] = re.sub(r': function (\w+)\([^\(\)]+\).*', r' = \1', i)
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










# 后续的处理就是将 switch 部分的寻参函数全部都解码成可用的字符串，后续再进一步处理
# 增强语义，后续的处理就会干净很多很多。看情况多次解码也可以高强度增强语义，大幅节约解码时间。
print(_0x53a5("0x3d", "@l$z"))
print(_0x53a5("0x3e", "l(8Z"))
print(_0x53a5("0x3f", "H!NY"))
print(_0x53a5("0x40", "[I(U"))
print(_0x53a5("0x41", "[I(U"))
print(_0x53a5("0x42", "R%HY"))
print(_0x53a5("0x43", "!tw2"))
print(_0x53a5("0x44", "$WyH"))