from multiprocessing.managers import BaseManager
from threading import Thread,Lock
from lxml import etree
import multiprocessing,time,urllib2,json,re,threading,os,random

class man(BaseManager):pass
man.register('joblists')
man.register('retlists')
man.register('datalists')
man.register('controllist')
man.register('exceptlist')

def init():
    global manager
    try:
        ip = '127.0.0.1'
        port = 9888
        authkey = 'abcdefg'
        for i in open('init.info','r').readlines():
            if i.split('=')[0].strip() == 'ip':
                ip = i.split('=')[1].strip()
            if i.split('=')[0].strip() == 'port':
                port = int(i.split('=')[1].strip())
            if i.split('=')[0].strip() == 'authkey':
                authkey = i.split('=')[1].strip()
        manager=man(address=(ip,port),authkey=authkey)
        print 'ip:',ip
        print 'port:',port
        print 'authkey:',authkey
    except:
        print 'error init'
        print 'use default ip,port,authkey'
        print 'ip:','127.0.0.1'
        print 'port:',9888
        print 'authkey:','abcdefg'
        manager=man(address=('127.0.0.1',9888),authkey='abcdefg')
    manager.connect()

def work(lock,t=0):
    job = manager.joblists()
    ret = manager.retlists()
    data = manager.datalists()
    error = manager.exceptlist()
    control = manager.controllist()
    while 1:
        if not control.empty():break
        if job.empty():
            lock.acquire()
            print 'sleep: '+str(threading.currentThread())+str(time.strftime("%H:%M:%S"))
            lock.release()
            time.sleep(5)
            continue
        try:
            get = job.get_nowait()
            lock.acquire()
            print 'get: '+str(get)
            lock.release()
        except:
            print 'get error: '+str(threading.currentThread())+str(time.strftime("%H:%M:%S"))
            continue
        try:
            datas, urls = douban_crawl(get)
            if data == 0 and urls == 0:
                continue
            data.put(datas)
            for i in urls:
                ret.put(i)
                #lock.acquire()
                #print 'ret:'+str(i)
                #lock.release()
            time.sleep(t)
        except:
            lock.acquire()
            print 'except:'+str(get)+str(threading.currentThread())
            #job.put(get)
            error.put(get)
            lock.release()
            time.sleep(2)
        time.sleep(0.1)

def douban_crawl(url):
    headers = {'User-Agent':'Mozilla/5.0',
               'Cookie':'bid="pxr19V1X5yM"; gr_user_id=a0ca327f-c73e-45ad-99ad-3319971dbd1b; ll="118339"; ue="2473495041@qq.com"; ps=y; _vis_opt_s=1%7C; _vwo_uuid=1B553A71D99B4028C957BD345F1D9FCB; _vis_opt_exp_30_combi=1; ap=1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1481703778%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; viewed="1770782_1046265_3259440_1084336_3354490_4777393_1148282_26414485_11530329_1443597"; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=397c834a-b328-42be-85bb-5e0b04c55760; gr_cs1_397c834a-b328-42be-85bb-5e0b04c55760=user_id%3A0; _pk_id.100001.'+\
               hex(random.randint(4096,65535))[2:]+'=17a778331075'+hex(random.randint(4096,65535))[2:]+'.1461581520.43.'+\
               str(time.mktime(time.localtime()))[:-2]+'.1481707989.; _pk_ses.100001.3ac3=*; __utmt_douban=1; __utma=30149280.281212701.1460152041.1481565913.1481703779.87; __utmb=30149280.2.10.1481703779; __utmc=30149280; __utmz=30149280.1481337419.85.67.utmcsr=so.com|utmccn=(organic)|utmcmd=organic|utmctr=%E8%A5%BF%E9%83%A8%E4%B8%96%E7%95%8C%20%E8%B1%86%E7%93%A3; __utmv=30149280.13292; __utmt=1; __utma=81379588.1949161896.1477731820.1481565922.1481703779.6; __utmb=81379588.2.10.1481703779; __utmc=81379588; __utmz=81379588.1481565922.5.4.utmcsr=so.com|utmccn=(organic)|utmcmd=organic|utmctr=douban; _vwo_uuid_v2=3632BE2EEBAF9B94277E4F17ED61C559|dd92049a894444d3b5b2d9bc5d39c665'}
    request = urllib2.Request(url,headers=headers)
    response = urllib2.urlopen(request,timeout=10)
    if response.getcode() == 200:
        page = response.read().decode('utf-8')
        e = etree.HTML(page)
        name_book = e.xpath('//*[@id="wrapper"]/h1/span/text()')[0]
        cover_url = e.xpath('//*[@id="mainpic"]/a/@href')[0]
        urls = re.findall('https://book.douban.com/subject/\d+/',page)
        return json.dumps([name_book,cover_url]), set(urls)
    else:
        return 0, 0

lock=Lock()
def usethread(func,num,t,lock=lock):
    a = [Thread(target=func,args=(lock,t)) for i in range(num)]
    for i in a:i.start()
    for i in a:i.join()

def add_job(lists):
    job = manager.joblists()
    for i in lists:
        print i
        job.put(i)

if __name__ == '__main__':
    init()
    usethread(work,7,0)
    os.system('pause')
