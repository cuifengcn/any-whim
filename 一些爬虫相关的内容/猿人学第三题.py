import json
import requests
def get_info(page):
    headers = {
        "Host": "match.yuanrenxue.com",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "yuanrenxue.project",
        "Accept": "*/*",
        "Origin": "http://match.yuanrenxue.com",
        "Referer": "http://match.yuanrenxue.com/match/3",
        "Accept-Encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    session = requests.session()
    session.headers = headers
    url = 'http://match.yuanrenxue.com/logo'
    session.get(url)
    s = session.get('http://match.yuanrenxue.com/api/match/3?page={}'.format(page))
    jsondata = json.loads(s.text)
    return jsondata

allvalues = []
for page in range(1,6):
    jsondata = get_info(page)
    values = [i.get("value") for i in jsondata['data']]
    allvalues.extend(values)
    print('page:{} --> values:{}'.format(page, values))

import collections
v = collections.Counter(allvalues)
v = sorted(v.items(), key=lambda i:-i[1])[0]
print('id:{} count:{}'.format(v[0], v[1]))