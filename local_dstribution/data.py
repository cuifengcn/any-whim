from multiprocessing.managers import BaseManager
from threading import Thread, Lock
import multiprocessing,time,threading,os,json

class man(BaseManager):pass
man.register('datalists')
man.register('datacontrol')

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

def run(f):
    init()
    data = manager.datalists()
    datac = manager.datacontrol()
    sums = 0
    while 1:
        if not datac.empty():
            break
        if data.empty():
            time.sleep(4)
            continue
        else:
            for i in range(data.qsize()):
                s = json.loads(data.get())
                print sums
                sums += 1
                f.write(s[0].encode('utf-8')+' '+s[1].encode('utf-8')+'\n')
                f.flush()

if __name__ == '__main__':
    print 'start data out put'
    with open('data.txt','a') as f:
        run(f)
    os.system('pause')
