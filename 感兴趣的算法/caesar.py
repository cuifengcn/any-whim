def caesar(t, n, l='abcdefghijklmnopqrstuvwxyz'):
    s = list(l)
    r = ''
    for i in t:
        if i in s:
            r += s[(s.index(i) + n)% len(l)]
        else:
            r += i
    return r

def map_caesar(t, func=None, l='abcdefghijklmnopqrstuvwxyz'):
    left = len(l) // 2
    right = len(l) - left
    ls = []
    for n in range(-left, right, 1):
        v = caesar(t, n, l)
        v = func(v) if func else v
        ls.append(v)
    return ls

if __name__ == '__main__':
    import base64
    func = lambda i:base64.b64encode(i.encode()).decode()
    v = map_caesar('asdf', func)
    for i in v:
        print(i)