import re
import json
import requests

def get_info(page):
    def mk_url_headers():
        url = (
            'http://match.yuanrenxue.com/match/13'
        )
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "yuanrenxue.project"
        }
        return url,headers
    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers)
    sessionid = re.findall('sessionid=[^;]+;', s.headers['Set-Cookie'])[0]
    cookie = ''.join(re.findall(r"\('(.)'\)", s.text)).split('=')[-1]
    def mk_url_headers(page, cookie, sessionid):
        url = (
            'http://match.yuanrenxue.com/api/match/13'
            '?page={}'
        ).format(page)
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": (
                sessionid + "yuanrenxue_cookie={}; ".format(cookie)
            ),
            "Host": "match.yuanrenxue.com",
            "Pragma": "no-cache",
            "Referer": "http://match.yuanrenxue.com/match/13",
            "User-Agent": "yuanrenxue.project",
            "X-Requested-With": "XMLHttpRequest"
        }
        return url,headers
    url,headers = mk_url_headers(page, cookie, sessionid)
    s = requests.get(url,headers=headers)
    return json.loads(s.text)

allvalues = []
for page in range(1,6):
    jsondata = get_info(page)
    values = [i.get("value") for i in jsondata['data']]
    allvalues.extend(values)
    print('page:{} --> values:{}'.format(page, values))

print('sum:{}'.format(sum(allvalues)))