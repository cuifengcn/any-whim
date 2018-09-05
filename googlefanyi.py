import execjs
import requests
import json,re,time

from urllib.parse import quote

class googlefanyi:
    def __init__(self):
        self.ctx = execjs.compile("""
                function TL(a) {
                var k = "";
                var b = 406644;
                var b1 = 3293161072;
                
                var jd = ".";
                var $b = "+-a^+6";
                var Zb = "+-3^+b+-f";
            
                for (var e = [], f = 0, g = 0; g < a.length; g++) {
                    var m = a.charCodeAt(g);
                    128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                    e[f++] = m >> 18 | 240,
                    e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
                    e[f++] = m >> 6 & 63 | 128),
                    e[f++] = m & 63 | 128)
                }
                a = b;
                for (f = 0; f < e.length; f++) a += e[f],
                a = RL(a, $b);
                a = RL(a, Zb);
                a ^= b1 || 0;
                0 > a && (a = (a & 2147483647) + 2147483648);
                a %= 1E6;
                return a.toString() + jd + (a ^ b)
            };
            
            function RL(a, b) {
                var t = "a";
                var Yb = "+";
                for (var c = 0; c < b.length - 2; c += 3) {
                    var d = b.charAt(c + 2),
                    d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
                    d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
                    a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
                }
                return a
            }
            """)
        self.url = 'https://translate.google.cn/translate_a/single?'+\
                   'client=t&sl=ko&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&'+\
                   'dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&'+\
                   'ie=UTF-8&oe=UTF-8&ssel=3&tsel=3&kc=0&tk=%s&q=%s'

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'x-client-data': 'xxx',
            'referer': 'https://translate.google.cn/',
            'cookie': 'xxx'}

    def translate(self,text):
        tk = self.ctx.call("TL",text)
        url = self.url % (tk,quote(text))
        v = requests.get(url,headers=self.headers)
        v = json.loads(v.content)
        return v

gf = googlefanyi()
##v = gf.translate('뒤를밟으며곱씹기시작한다')
##print(v)

def deal_has_slash(text):
    v = re.split(r'\\\d+',text)
    b = re.findall(r'\\\d+',text)
    q = []
    for i in range(len(v)):
        if i == len(v)-1:
            q.append(v[i])
        else:
            q.append(v[i])
            q.append(b[i])
    return q

def translate_line(text_line):
    q = []
    for idx,i in enumerate(text_line):
        if idx % 2 == 0:
            if i.strip() != '':
                v = gf.translate(i)
                q.append(v[0][0][0])
            else:
                q.append(i)
        else:
            q.append(i)
    return ''.join(q)

##
##with open('fin.txt','w',encoding='utf-8') as f:
##    for idx,i in list(enumerate(s.splitlines()))[7568:]:
##        v = deal_has_slash(i)
##        q = translate_line(v)
##        time.sleep(.1)
##        print(idx,':',q)
##        f.write(q + '\n')
##











