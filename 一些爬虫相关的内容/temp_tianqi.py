# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

import re
import json
from urllib.parse import unquote, quote, urlencode

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # Do not use automatic cookie caching(set 'dont_merge_cookies' as True in Request.meta is same)
    }
    proxy = None # 'http://127.0.0.1:8888'

    def start_requests(self):
        def mk_url_headers():
            def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='utf-8'),encoding='utf-8'), url)
            url = (
                'https://www.aqistudy.cn/html/city_realtime.php'
                '?v=2.3'
            )
            url = quote_val(url)
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers()
        meta = {}
        meta['proxy'] = self.proxy
        r = Request(
                url,
                headers  = headers,
                callback = self.parse,
                meta     = meta,
            )
        yield r

    def parse(self, response):
        content = response.body.decode()
        url = response.urljoin(re.findall(r'src="(\.\./js/encrypt_[^"]+)', content)[0])
        def mk_url_headers(url):
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            return url,headers
        url,headers = mk_url_headers(url)
        meta = {}
        meta['proxy'] = self.proxy
        r = Request(
                url,
                headers  = headers,
                callback = self.parse_js,
                meta     = meta,
            )
        yield r

    def parse_js(self, response):
        # \|WEB\|dff933b853a2e91437794937ac0e164b\|type\|post\|php\|1000\|try\|s2CLYmMydSVoLi\|undefined\|hyfNUtabf\|
        print(response.body.decode())
        key = re.findall(r'[\|\'](h[a-zA-Z0-9]{8})[\|\']', response.body.decode())[0]
        par = re.findall(r'[\|\']([a-zA-Z0-9]{32})[\|\']', response.body.decode())[0]
        print(key)
        print(par)
        
        def mk_url_headers_body(city):
            def mk_body(city):
                _pkey = re.findall(r'[\|\'](h[a-zA-Z0-9]{8})[\|\']', response.body.decode())[0]
                appid = re.findall(r'[\|\']([a-zA-Z0-9]{32})[\|\']', response.body.decode())[0]
                import json, time, hashlib, base64
                _my_md5 = lambda string:hashlib.md5(string.encode()).hexdigest()
                _my_dumps = lambda obj:json.dumps(obj,ensure_ascii=False,separators=(',',':'))
                appId = appid
                method = "GETDATA"
                timestamp = int(time.time()*1000)
                clienttype = "WEB"
                _object = {"city":city}
                secret = _my_md5(appId+method+str(timestamp)+clienttype+_my_dumps(_object))
                info = _my_dumps({
                    "appId":appId,
                    "method":method,
                    "timestamp":timestamp,
                    "clienttype":clienttype,
                    "object":_object,
                    "secret":secret,
                })
                binfo = base64.b64encode(info.encode())
                return {_pkey: binfo}
            url = (
                'https://www.aqistudy.cn/apinew/aqistudyapi.php'
            )
            headers = {
                "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "accept-language": "zh-CN,zh;q=0.9",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
            }
            body = mk_body(city)
            return url,headers,body
        url,headers,body = mk_url_headers_body('上海')
        print(body)
        meta = {}
        meta['proxy'] = self.proxy
        r = Request(
                url,
                method   = 'POST',
                headers  = headers,
                body     = urlencode(body),
                callback = self.parse_info,
                meta     = meta,
            )
        yield r

    def parse_info(self, response):
        pass
        print(response.body.decode())





# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/lPqLaXSGBd'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

    p = CrawlerProcess({
        'TELNETCONSOLE_ENABLED':    False,        # 几乎没人使用到这个功能，直接关闭提高爬虫启动时间
        'MEDIA_ALLOW_REDIRECTS':    True,         # 允许图片下载地址重定向，存在图片下载需求时，请尽量使用该设置
        'LOG_LEVEL':                'INFO',       # DEBUG , INFO , WARNING , ERROR , CRITICAL
        # 'JOBDIR':                   jobdir,     # 解开注释则增加断点续爬功能
                                                  # 任务队列、任务去重指纹、任务状态存储空间(简单来说就是一个文件夹)
        # 'FEED_URI':                 filename,   # 下载数据到文件
        # 'FEED_EXPORT_ENCODING':     'utf-8',    # 在某种程度上，约等于 ensure_ascii=False 的配置选项
        # 'FEED_FORMAT':              'json',     # 下载的文件格式，不配置默认以 jsonlines 方式写入文件，
                                                  # 支持的格式 json, jsonlines, csv, xml, pickle, marshal
        # 'DOWNLOAD_TIMEOUT':         8,          # 全局请求超时，默认180。也可以在 meta 中配置单个请求的超时( download_timeout )
        # 'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
    })
    p.crawl(VSpider)
    p.start()
