import re
import json
from urllib.parse import unquote, quote

import requests
from lxml import etree

def get_font_dict():
    # 生成请求参数函数
    def mk_url_headers():
        url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/a611dc09acc5449dc110cb378b42c19c.svg'
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        return url,headers
    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers)
    font_list = re.findall(r'<text x="0" y="(.*?)">(.*?)</text>', s.content.decode())
    font_size = 14
    start_y = 23
    font_dict = {}
    for y, string in font_list:
        y_offset = start_y - int(y)
        for j, font in enumerate(string):
            x_offset = -j * font_size
            font_dict[(x_offset, y_offset)] = font
    return font_dict

def get_css_dict():
    def mk_url_headers():
        url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/6977f24cb12f17c2b63888656a6b52b9.css'
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        return url,headers
    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers)
    content = s.content.decode()
    css_dict = {}
    for a,b,c in re.findall(r'\.(.{5}){background:(.*?).0px (.*?).0px;}', content, flags=re.S):
        css_dict[a] = (int(b), int(c))
    return css_dict


def get_html_content():
    # 请配置头信息中的的 cookie 内容让正常的加密 HTML 文本结果返回，后再进行解密！！！！！！！！！
    def mk_url_headers():
        url = 'http://www.dianping.com/shop/9972787/review_all/p1'
        headers = {
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        return url,headers
    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers)
    return s.content.decode()

if __name__ == '__main__':
    css_dict = get_css_dict()
    font_dict = get_font_dict()
    content = get_html_content()# 请配置头信息中的的 cookie 内容让正常的加密 HTML 文本结果返回，后再进行解密！！！！！！！！！
    for svg in re.findall('<svgmtsi class="(.*?)"></svgmtsi>', content):
        font = font_dict.get(css_dict.get(svg))
        content = re.sub(r'<svgmtsi class="%s"></svgmtsi>' % svg, font, content)
    print(content) # 解密后的 html 文本
