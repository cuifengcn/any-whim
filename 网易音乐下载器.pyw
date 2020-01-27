# 开发环境 python3，开发日期 20200127
# 依赖环境 pip3 install requests cryptography youtube-dl
# 直接执行即可使用，一个带有搜索和下载功能的图形化下载工具。

import requests
import os,sys,re,json,random,base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
def get_encryptor(key, iv=None):
    algoer = algorithms.AES(key)
    mode   = modes.CBC(iv)
    cipher = Cipher(algoer, mode, backend=default_backend())
    def enc(bitstring):
        padder    = padding.PKCS7(algoer.block_size).padder()
        bitstring = padder.update(bitstring) + padder.finalize()
        encryptor = cipher.encryptor()
        return encryptor.update(bitstring) + encryptor.finalize()
    def dec(bitstring):
        decryptor = cipher.decryptor()
        ddata     = decryptor.update(bitstring) + decryptor.finalize()
        unpadder  = padding.PKCS7(algoer.block_size).unpadder()
        return unpadder.update(ddata) + unpadder.finalize()
    class f:pass
    f.encrypt = enc
    f.decrypt = dec
    return f
def get_postbody(realparams):
    def mk_rdkey():
        rdstring = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return ''.join([random.choice(rdstring) for i in range(16)])
    def get_params(rdkey, data):
        key  = '0CoJUm6Qyw8W8jud'.encode()
        iv   = '0102030405060708'.encode()
        encryptor = get_encryptor(key, iv)
        edata = base64.b64encode(encryptor.encrypt(data.encode())).decode()
        encryptor = get_encryptor(rdkey.encode(), iv)
        edata = base64.b64encode(encryptor.encrypt(edata.encode())).decode()
        return edata
    def get_encSecKey(rdkey):
        def parse_base2int(string):
            v = 0
            for i in range(0,len(string)):
                p = len(string) - i - 1
                t = ord(string[p]) << p*8
                v += t
            return v
        return hex(pow(parse_base2int(rdkey),65537,157794750267131502212476817800345498121872783333389747424011531025366277535262539913701806290766479189477533597854989606803194253978660329941980786072432806427833685472618792592200595694346872951301770580765135349259590167490536138082469680638514416594216629258349130257685001248172188325316586707301643237607))[2:]
    rdkey = mk_rdkey()
    params = get_params(rdkey, realparams)
    encSecKey = get_encSecKey(rdkey)
    return params, encSecKey
def mk_mp3_url_headers_body(songid):
    url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    realparams = '''{"encodeType": "aac", "ids": "[''' +str(songid)+ ''']", "level": "standard"}'''
    params,encSecKey = get_postbody(realparams)
    body = { "params": params, "encSecKey": encSecKey }
    return url,headers,body
def mk_search_url_headers_body(searchkey):
    url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    realparams = {"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":searchkey,"type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}
    params,encSecKey = get_postbody(json.dumps(realparams))
    body = { "params": params, "encSecKey": encSecKey }
    return url,headers,body
def get_mp3_attr_by_songid(songid):
    url,headers,body = mk_mp3_url_headers_body(songid)
    r = requests.post(url,headers=headers,data=body)
    return json.loads(r.text)['data'][0]['url']
def get_infos_by_searchkey(searchkey):
    url,headers,body = mk_search_url_headers_body(searchkey)
    content = requests.post(url,headers=headers,data=body).text
    jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])
    infos = []
    for i in jsondata['result']['songs']:
        d = {}
        d["id"]   = i.get("id")
        d['name'] = '[{}]-[{}]-[{}]'.format(i.get("name"), '/'.join([i.get('name') for i in i.get("ar")]), i.get("al").get('name'))
        d['name'] = re.sub(r'[/\\:\*"<>\|\?]', '_', d['name']).strip()
        infos.append(d)
    return infos
# 尝试一个函数多次
def dosomething(func, *a, times=0, **kw):
    try:
        info = func(*a, **kw)
        assert info is not None
        return info
    except:
        print('retry:{}'.format(times))
        if times < 5: dosomething(func, *a, times=times+1, **kw)
        else: print('error retry times:{}'.format(times))
import tkinter
from tkinter.font import Font
t = tkinter.Tk()
ft = Font(family='Consolas',size=10)
f1 = tkinter.Frame(); f1.pack()
f2 = tkinter.Frame(); f2.pack()
f3 = tkinter.Frame(); f3.pack()
def search_btn(*a):
    lbx.delete(0, tkinter.END)
    msg = e1.get().strip()
    if msg:
        infos = dosomething(get_infos_by_searchkey, msg)
        for i in infos:
            info = '[id]{:<13}{}'.format(i.get('id'), i.get('name'))
            lbx.insert("end", info)
from youtube_dl import YoutubeDL
def double_click(*a):
    content = lbx.get(lbx.curselection())
    _id = re.findall(r'\[id\](\d+)', content)[0]
    _name = re.findall(r'\[id\]\d+(.*$)', content)[0].strip()
    url = dosomething(get_mp3_attr_by_songid, _id)
    localpage = os.path.dirname(os.path.realpath(sys.argv[0]))
    ytdl = YoutubeDL({'outtmpl': localpage+'/music/{}.mp3'.format(_name)})
    info = dosomething(ytdl.extract_info, url, download=True)
lb = tkinter.Label(f1,text='输入关键词点击搜索(回车)，双击需要的歌曲即可下载'); lb.pack(side=tkinter.LEFT)
e1 = tkinter.Entry(f1); e1.pack(side=tkinter.LEFT); e1.bind("<Return>", search_btn)
bt = tkinter.Button(f1,text='搜索歌曲', command=search_btn); bt.pack(side=tkinter.LEFT)
lbx = tkinter.Listbox(f2,width=80,height=25,font=ft); lbx.pack(); lbx.bind('<Double-Button-1>', double_click)
lb = tkinter.Label(f3,text='日志'); lb.pack()
tx = tkinter.Text(f3,height=13); tx.pack()
class mystdout:
    def write(msg): tx.insert(tkinter.END, msg+'\n')
    def flush(): tx.see(tkinter.END); tx.update()
sys.stdout = mystdout
t.mainloop()