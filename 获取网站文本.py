import re

import requests
from lxml import etree

url = 'http://www.gov.cn/yjgl/2006-01/15/content_159236.htm'
s = requests.get(url)

def normal_content(content,tags=['script','style','select','noscript',]):
    try:
        content = content.decode('utf-8')
    except:
        content = content.decode('gbk')
    e = etree.HTML(content)
    q = []
    for i in e.getiterator():
        if i.tag in tags:
            q.append(i)
    for i in q:
        i.getparent().remove(i)
    s = e.xpath('string(//html)')
    s = re.sub('\t+','',s)
    s = re.sub('\r+','',s)
    s = re.sub(' +',' ',s)
    s = re.sub('\n+','\n',s)
    s = re.sub('(:?\n )+','\n ',s)
    return s
        
v = normal_content(s.content)
print(v)
