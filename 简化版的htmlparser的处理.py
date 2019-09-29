from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.curr = 0
        self.maps = {'info':{}, 'sub':[]} # 解析地图

    def get_curr_map_sub(self):
        tmap = self.maps['sub']
        for _ in range(self.curr): tmap = tmap[-1]['sub']
        return tmap

    def get_curr_map_info(self):
        if self.curr == 0: return 
        tmap = self.maps['sub']
        for _ in range(self.curr - 1): tmap = tmap[-1]['sub']
        return tmap[-1]['info']

    def _init_starttag(self):
        self.get_curr_map_sub().append({'info':{}, 'sub':[]})
        self.curr += 1

    def _finish_endtag(self):
        self.curr -= 1

    def _record_maps(self, tag, attrs=None):
        cinfo = self.get_curr_map_info()
        cinfo['tag'] = tag
        cinfo['attrs'] = dict(attrs)

    def _record_maps_data(self, data):
        cinfo = self.get_curr_map_info()
        if cinfo:
            cinfo['data'] = data

    def handle_starttag(self, tag, attrs):
        if tag in ['br', 'meta', 'link']: return
        self._init_starttag()
        self._record_maps(tag, attrs)
        print('<%s>' % tag, end='')

    def handle_endtag(self, tag):
        self._finish_endtag()
        print('</%s>' % tag, end='')

    def handle_startendtag(self, tag, attrs):
        self._init_starttag()
        self._record_maps(tag, attrs)
        self._finish_endtag()
        print('<%s/>' % tag, end='')

    def handle_data(self, data):
        self._record_maps_data(data)
        print(data, end='')

parser = MyHTMLParser()
parser.feed('''
<HTML>
    <head>
        <meta charset="utf-8">
        <title>在线JSON校验格式化工具（Be JSON）</title>
        <link rel='dns-prefetch' href='//www.bejson.com' />
    </head>
    <body>
        <!-- test html parser -->
        <img src='http://asdfasdf.jpg' />
        <div id="123" class="asdf">
            <p aaa='fff'>你好啊兄弟</p>
        </div>
        <p>
            Some 
            <a href="#">   html1   </a>
            HTML&nbsp;tutorial...<br/>END
        </p>
        <p>
            Some
            <a href="#">   html2  </a>
            asdfasdfasdf<br/>END
        </p>
    </body>
</html>
''')

# 目前暂时解析树，后续再考虑整理如何 “迭代树” 和 “列表树”
import json
v = json.dumps(parser.maps, indent=4)
print(v)