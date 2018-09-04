import hashlib
import requests
import random,time

class youdao:
    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Referer': 'http://fanyi.youdao.com/',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=446843847@10.169.0.84'
            }

        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.S = "fanyideskweb"
        self.D = "ebSeFb%=XZ%T[KZ)c(sy!"

    def get_json(self,text):
        n = text
        r = str(int(time.time()*1000) + random.randint(0,9))
        sign = self.get_sign(self.S + n + r + self.D)

        data = f'i={n}&'                        + \
                'from=AUTO&'                    + \
                'to=AUTO&'                      + \
                'smartresult=dict&'             + \
                'client=fanyideskweb&'          + \
               f'salt={r}&'                     + \
               f'sign={sign}&'                  + \
                'doctype=json&'                 + \
                'version=2.1&'                  + \
                'keyfrom=fanyi.web&'            + \
                'action=FY_BY_CLICKBUTTION&'    + \
                'typoResult=false'
        data = self.parse2dict(data)
        s = requests.post(self.url,\
                          headers=self.headers,\
                          data=data)
        return s.json()

    def parse2dict(self,data):
         v = [i.split('=',1) for i in data.split('&')]
         v = {i:j for i,j in v}
         return v

    def get_sign(self,o):
        v = hashlib.md5()
        v.update(o.encode('utf-8'))
        sign = v.hexdigest()
        return sign

if __name__ == '__main__':
    text = 'you \s punch \s in \s \ witj \s'
    s = youdao()
    v = s.get_json(text)
    print(v)
