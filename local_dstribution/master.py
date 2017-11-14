from multiprocessing.managers import BaseManager
from threading import Thread, Lock
import multiprocessing,time,json,threading,os

class man(BaseManager):pass
man.register('joblists')
man.register('retlists')
man.register('mastercontrol')
man.register('settablelist')
man.register('datalists')

crawled = set()

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

def add_job(lists):
    job = manager.joblists()
    for i in lists:
        print i
        job.put(i)

def ret_job():
    init()
    ret = manager.retlists()
    job = manager.joblists()
    master = manager.mastercontrol()
    settable = manager.settablelist()
    initial()
    while 1:
        if not master.empty():
            time.sleep(1)
            print 'master break'
            break
        if ret.qsize() > 2000:
            ret2job(job,ret,settable)
        if job.qsize()==0 and ret.qsize()!=0:
            ret2job(job,ret,settable)
        else:
            print 'master sleep: '+str(time.strftime("%H:%M:%S"))
            time.sleep(3)
            continue

def initial():
    settable = manager.settablelist()
    for i in range(settable.qsize()):
        s = settable.get()
        settable.put(s)

def ret2job(job,ret,settable):
    ret = manager.retlists()
    settable = manager.settablelist()
    for i in set([ret.get() for i in range(ret.qsize())]):
        if i not in crawled:
           crawled.add(i)
           settable.put(i)
           job.put(i)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    ret_job()
    os.system('pause')
    
