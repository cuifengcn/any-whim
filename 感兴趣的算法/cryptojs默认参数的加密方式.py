from hashlib import new
import base64
def parse_cryptojs_from_default_params(key, data):
    def EvpKDF(hash_name, password, salt, iterations, dklen=None):
        dkey = b''
        block = None
        hasher = new(hash_name)
        while len(dkey) < dklen:
            if block:
                hasher.update(block)
            hasher.update(password)
            hasher.update(salt)
            block = hasher.digest()
            hasher = new(hash_name)
            for i in range(1, iterations):
                hasher.update(block)
                block = hasher.digest()
                hasher = new(hash_name)
            dkey += block
        return dkey[:dklen]
    s = base64.b64decode(data)
    v = EvpKDF('md5', key, s[8:16], 1, 48)
    return v[:32], v[32:], s[16:]



key     = '123456'.encode()                                 # 密钥
data    = 'U2FsdGVkX19Z5E1HW9aINhHNTZWP9j5n92CpTMuJqJc='    # 原始数据 '111111'
key, iv, data = parse_cryptojs_from_default_params(key, data)

# cryptojs 的默认加密方式每次加密都不一样，并且都有 U2FsdGVkX1 这个头标志
# 虽然加密不一样，但是解密都是一样的，这是因为他使用了一个随机数，并且这个随机数是放在加密数据里面
# 用这个随机数进行散列算法，算出 key 以及 iv 使用固定的模式进行加密就可以每次加密不同了。
# 所以，只要拿到这个随机数的部分，然后将这个随机进行一个固定的散列算法就可以算出真实的 aes 的key和iv
# 剩下的部分就是真实的加密流，通过固定的模式直接解密即可获取数据，cbc/pkcs7
print(key)
print(iv)
print(data)