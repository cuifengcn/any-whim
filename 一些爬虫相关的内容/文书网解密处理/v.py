# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

import re
import json
import time
from urllib.parse import quote,unquote,urlencode



import execjs
import js2py
from js2py.pyjs import *
var = Scope( JS_BUILTINS )
set_global_object(var)
@Js
def _jseval(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    return var.get('eval')(var.get('s').callprop('substr', Js(0.0), (var.get('s').get('length')-Js(1.0))).callprop('slice', Js(0.0), (-Js(2.0))))

with open('./get_docid.js',   encoding='utf-8') as f: _get_docid    = execjs.compile(f.read())
with open('./get_vl5x.js',    encoding='utf-8') as f: _get_vl5x     = execjs.compile(f.read())
with open('./get_wzws_cid.js',encoding='utf-8') as f: _get_wzws_cid_string = f.read()

def _get_wzws_cid_next_url_with_replace_eval_string(content):
    evalstring = re.findall('eval[^\n]+', content)[0]
    estring = _get_wzws_cid_string.replace('$evalfunction', evalstring)
    return 'http://wenshu.court.gov.cn' + js2py.eval_js(estring)()

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # use my create cookie in headers
    }

    def start_requests(self):
        def mk_url_headers_body(vjkl5=None, vl5x=None):
            vjkl5 = 'vjkl5={}; '.format(vjkl5) if vjkl5 else ''
            def quote_val(url):
                url = unquote(url)
                for i in re.findall('=([^=&]+)',url):
                    url = url.replace(i,'{}'.format(quote(i)))
                return url
            url = (
                'http://wenshu.court.gov.cn/List/ListContent'
            )
            url = quote_val(url)
            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": (
                    "{}"
                ).format(vjkl5),
                "Host": "wenshu.court.gov.cn",
                "Origin": "http://wenshu.court.gov.cn",
                "Pragma": "no-cache",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }
            body = {
                "Param": "裁判日期:2019-05-23 TO 2019-05-23,文书类型:全部",
                "Index": "1",
                "Page": "20",
                "Order": "法院层级",
                "Direction": "asc",
                "vl5x": "{}".format(vl5x),
                "guid": "afdf14af-4983-fd6317bd-67b00948c87d"
            }
            return url,headers,body

        vjkl5 = '7296294ffe11329010518a2f6e558eca46fbc65a'
        vl5x  = '8cc72057ae7af071d71c135e'
        url,headers,body = mk_url_headers_body(vjkl5, vl5x)
        meta = {}
        r = Request(
                url,
                method   = 'POST',
                headers  = headers,
                body     = urlencode(body),
                callback = self.parse,
                meta     = meta,
            )
        yield r

    def parse(self, response):
        try:
            jsondata = json.loads(json.loads(response.body.decode()))
        except:
            yield self._revalidation(response) # 更新验证信息后自动重新请求。
            return
        runeval = jsondata[0]['RunEval']
        content = jsondata[1:]
        for i in content:
            docid = self._decrypt_docid(runeval, i['文书ID'])
            casejudgedate = i.get('裁判日期', '')
            url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}'.format(docid)
            meta = {}
            meta['casejudgedate'] = casejudgedate
            r = Request(
                url, 
                callback = self.parse_info, 
                meta     = meta,
                dont_filter=True
            )
            yield r
            return




    def parse_info(self, response):
        '''获取每条案件详情'''
        html = response.text

        if '请开启JavaScript并刷新该页.' in html:
            yield self._revalidation_wzws_cid(response)
            return


        content_1 = json.loads(re.search(r'JSON\.stringify\((.*?)\);\$\(document', html).group(1))  # 内容详情字典1
        content_3 = re.search(r'"Html\\":\\"(.*?)\\"}"', html).group(1)  # 内容详情字典3(doc文档正文)
        reg = re.compile(r'<[^>]+>', re.S)
        # 存储到item
        d = {}
        d['casecourt'] = {
            'casecourtid': content_1.get('法院ID', ''),
            'casecourtname': content_1.get('法院名称', ''),
            'casecourtprovince': content_1.get('法院省份', ''),
            'casecourtcity': content_1.get('法院地市', ''),
            'casecourtdistrict': content_1.get('法院区县', ''),
            'casecourtarea': content_1.get('法院区域', ''),
        }
        d['casecontent'] = {
            'casebasecontent': content_1.get('案件基本情况段原文', ''),
            'caseaddcontent': content_1.get('附加原文', ''),
            'caseheadcontent': content_1.get('文本首部段落原文', ''),
            'casemaincontent': content_1.get('裁判要旨段原文', ''),
            'casecorrectionscontent': content_1.get('补正文书', ''),
            'casedoccontent': content_1.get('DocContent', ''),
            'caselitigationcontent': content_1.get('诉讼记录段原文', ''),
            'casepartycontent': content_1.get('诉讼参与人信息部分原文', ''),
            'casetailcontent': content_1.get('文本尾部原文', ''),
            'caseresultcontent': content_1.get('判决结果段原文', ''),
            'casestrcontent': reg.sub('', content_3),  # 去除html标签后的文书内容
        }
        d['casetype'] = content_1.get('案件类型', '')  # 案件类型
        d['casejudgedate'] = response.meta['casejudgedate']  # 裁判日期
        d['caseprocedure'] = content_1.get('审判程序', '')
        d['casenumber'] = content_1.get('案号', '')
        d['casenopublicreason'] = content_1.get('不公开理由', '')
        d['casedocid'] = content_1.get('文书ID', '')
        d['casename'] = content_1.get('案件名称', '')
        d['casecontenttype'] = content_1.get('文书全文类型', '')
        d['caseuploaddate'] = time.strftime("%Y-%m-%d",
                                               time.localtime(int(content_1['上传日期'][6:-5]))) if 'Date' in content_1[
            '上传日期'] else ''
        d['casedoctype'] = content_1.get('案件名称').split('书')[0][-2:] if '书' in content_1.get(
            '案件名称') else '令'  # 案件文书类型:判决或者裁定...还有令
        d['caseclosemethod'] = content_1.get('结案方式', '')
        d['caseeffectivelevel'] = content_1.get('效力层级', '')

        yield d









    # 用于处理获取 vl5x 参数的方法
    def _revalidation(self, response):
        '''
        抛出对 /list/list 页面的请求以获取 vjkl5 参数，
        并且将之前跑失败的请求重新包装一遍准备在获取到新的验证时再请求
        '''
        def _mk_get_vl5x_req(plusmeta):
            def mk_url_headers_body():
                def quote_val(url):
                    url = unquote(url)
                    for i in re.findall('=([^=&]+)',url):
                        url = url.replace(i,'{}'.format(quote(i)))
                    return url
                url = (
                    'http://wenshu.court.gov.cn/list/list'
                )
                url = quote_val(url)
                headers = {
                }
                body = {
                }
                return url,headers,body
            url,headers,body = mk_url_headers_body()
            meta = {}
            meta.update({'plusmeta': plusmeta}) 
            r = Request(
                    url,
                    method   = 'POST',
                    headers  = headers,
                    body     = urlencode(body),
                    callback = self._parse_get_vl5x,
                    meta     = meta,
                    dont_filter = True,
                )
            return r
        o = {}
        o['url']     = response.request.url
        o['headers'] = response.request.headers
        o['body']    = response.request.body
        o['callback'] = response.request.callback.__name__
        return _mk_get_vl5x_req(o)

    def _parse_get_vl5x(self, response):
        '''
        获取到请求后的 set-cookie 参数内的 vjkl5
        然后通过js加密函数生成 vl5x 的参数，并对 cookie 以及 vl5x 进行更新操作
        '''
        for i in response.headers.getlist('Set-Cookie'):
            if b'vjkl5' in i: vjkl5 = re.findall(b'vjkl5=([a-zA-Z0-9]+)', i)[0]
        vl5x  = _get_vl5x.call('getvl5x',vjkl5.decode())
        # 整理之前失败的请求
        plusmeta = response.meta.get('plusmeta')
        url      = plusmeta.get('url')
        headers  = plusmeta.get('headers')
        body     = plusmeta.get('body')
        callback = getattr(self, plusmeta.get('callback'))
        # 更新验证参数
        cookie  = headers[b'Cookie']
        ncookie = re.sub(b'vjkl5=[a-zA-Z0-9]+',b'vjkl5='+vjkl5,cookie) if b'vjkl5' in cookie else \
                  b'vjkl5='+vjkl5+b'; ' + cookie
        headers[b'Cookie'] = ncookie
        body    = re.sub(b'vl5x=[a-zA-Z0-9]+',b'vl5x='+vl5x.encode(),body)
        meta = {'vl5x':vl5x, 'vjkl5':vjkl5}
        r = Request(
                url,
                method   = 'POST',
                headers  = headers,
                body     = body,
                callback = callback,
                meta     = meta,
                dont_filter = True,
            )
        yield r

    def _decrypt_docid(self, runeval, node):
        _a = _get_docid.call('unzip', runeval)
        _b = _get_docid.call('unzip', node)
        key = re.findall('="([^"]+)"', str(_jseval(_a)))[0]
        docid = _get_docid.call('getdocid', key, _b)
        return docid




    # 用于重新验证 wswz_cid 函数的处理
    def _revalidation_wzws_cid(self, response):
        def _mk_get_wzws_cid_req(new_url, cookie, response, plusmeta):
            headers = response.headers
            headers[b'Cookie'] = cookie

            for i in headers.items():
                print(11,i)

            url = new_url
            meta = {}
            meta.update({'plusmeta': plusmeta}) 
            meta['dont_redirect'] = True
            meta['handle_httpstatus_list'] = [302]
            r = Request(
                    url,
                    headers  = headers,
                    callback = self._update_wzsw_cid,
                    meta     = meta,
                    dont_filter = True,
                )
            return r

        o = {}
        o['url']     = response.request.url
        o['headers'] = response.request.headers
        o['body']    = response.request.body
        o['meta']    = response.request.meta
        o['callback'] = response.request.callback.__name__
        cookie = response.headers.get('Set-Cookie')
        new_url = _get_wzws_cid_next_url_with_replace_eval_string(response.body.decode())
        return _mk_get_wzws_cid_req(new_url, cookie, response, o)

    def _update_wzsw_cid(self, response):
        for i in response.headers.getlist('Set-Cookie'):
            if b'wzws_cid' in i: wzws_cid = re.findall(b'wzws_cid=[a-zA-Z0-9]+', i)[0]
        plusmeta = response.meta.get('plusmeta')
        url      = plusmeta.get('url')
        headers  = plusmeta.get('headers')
        body     = plusmeta.get('body')
        meta     = plusmeta.get('meta')
        callback = getattr(self, plusmeta.get('callback'))
        ncookie = wzws_cid+b'; '
        headers[b'Cookie'] = ncookie
        r = Request(
            url,
            headers     = headers,
            callback    = callback,
            meta        = meta,
            dont_filter = True,
        )
        return r