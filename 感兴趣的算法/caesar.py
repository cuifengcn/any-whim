def caesar(t, n, keys='abcdefghijklmnopqrstuvwxyz'):
    s = list(keys)
    r = ''
    for i in t:
        if i in s:
            r += s[(s.index(i) + n)% len(keys)]
        else:
            r += i
    return r

def map_caesar(t, func=None, keys='abcdefghijklmnopqrstuvwxyz'):
    l = len(keys) // 2
    r = len(keys) - l
    o = []
    for n in range(-l, r, 1):
        v = caesar(t, n, keys)
        v = func(v) if func else v
        o.append(v)
    return o


import base64
import hashlib
def func(i):
    e = base64.b64encode
    return e(i.encode()).decode()

def func2(i):
    v = hashlib.new('md5',i.encode())
    v = v.hexdigest()
    return v

if __name__ == '__main__':
    v = map_caesar('asdf', func)
    for i in v:
        print(i)