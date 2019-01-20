# encoding=utf-8

import re
import requests
from lxml import etree

def get_simple_path(e):
    root = e.getroottree()
    xp = root.getelementpath(e)
    v = xp.count('/')
    # 优先找路径上的id和class项优化路径
    for i in range(v):
        xpa = xp.rsplit('/',i)[0]
        rke = '/'.join(xp.rsplit('/',i)[1:])
        ele = root.xpath(xpa)[0].attrib
        tag = root.xpath(xpa)[0].tag
        if 'id' in ele:
            key = ele["id"]
            rke = '/'+rke if rke else ""
            val = '//%s[@id="%s"]%s'%(xpa.rsplit('/',1)[1],ele["id"],rke)
            return xp,val
        if 'class' in ele:
            key = ele["class"]
            rke = '/'+rke if rke else ""
            val = '//%s[@class="%s"]%s'%(xpa.rsplit('/',1)[1],ele["class"],rke)
            if not key.strip():
                continue
            return xp,val

def get_xpath_by_str(strs, html_content_or_element):
    if isinstance(html_content_or_element,(str, bytes)):
        e = etree.HTML(html_content_or_element)
    else:
        e = html_content_or_element.getroottree()
    p = []
    for i in e.xpath('//*'):
        xps = get_simple_path(i)
        if xps:
            xp, sxp = xps
            if [xp, sxp] not in p:
                p.append([xp, sxp])
    p.sort(key=lambda i: -len(i[0]))
    for xp, sxp in p:
        v = e.xpath('string({})'.format(xp))
        if strs in v:
            print(xp, sxp)
            #return xp, sxp

url = (
    'https://www.baidu.com/'
)
headers = {
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-CN,zh;q=0.9",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
}

def get(url,headers):
    s = requests.get(url,headers=headers)
    e = etree.HTML(s.content)
    return e,s.content

e,content = get(url,headers)
get_xpath_by_str('百度',content)
