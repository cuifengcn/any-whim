from multiprocessing.managers import BaseManager
import multiprocessing,time,os

class man(BaseManager):pass
man.register('controllist')
man.register('joblists')
man.register('retlists')
man.register('datalists')
man.register('exceptlist')
man.register('mastercontrol')
man.register('settablelist')
man.register('centercontrol')
man.register('datacontrol')

manager = man(address=('127.0.0.1',9000),authkey='vivivivi')

codes = ['c','stop','stop-','master','master-','all',\
         'showerror','center','center-','datac','datac-']
print 'control codes:'+str(codes)

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

def controler():
    init()
    job = manager.joblists()
    ret = manager.retlists()
    data = manager.datalists()
    control = manager.controllist()
    error = manager.exceptlist()
    master = manager.mastercontrol()
    settable = manager.settablelist()
    center = manager.centercontrol()
    datac = manager.datacontrol()
    while 1:
        code = raw_input('please entry code:')
        if code not in codes:
            try:
                exec(code)
            except:
                print 'not in codes'
                continue
        if code == 'c':
            break
        if code == 'stop':
            control.put_nowait('m')
            continue
        if code == 'center':
            center.put_nowait('m')
            continue
        if code == 'center-':
            try:
                center.get_nowait('m')
                continue
            except:
                print 'center error: error code[0]'
        if code == 'stop-':
            try:
                control.get_nowait()
                continue
            except:
                print 'stop error: error code[0]'
        if code == 'master':
            print 'end state'
            master.put_nowait('m')
            print '----------------------------'
            print 'size of joblist',job.qsize()
            print 'size of retlist',ret.qsize()
            print 'size of datalist',data.qsize()
            print 'size of exceptlist',error.qsize()
            print 'size of settable',settable.qsize()
            print 'state of controllist(not 0 mean off)',control.qsize()
            print 'state of master(not 0 mean off)',master.qsize()
            print 'state of center(not 0 mean off)',center.qsize()
            print 'state of datac(not 0 mean off)',datac.qsize()
            print '----------------------------'
            continue
        if code == 'master-':
            master.get_nowait()
            continue
        if code == 'datac-':
            datac.get_nowait()
            continue
        if code == 'datac':
            datac.put_nowait('m')
            continue
        if code == 'all':
            print '----------------------------'
            print 'size of joblist',job.qsize()
            print 'size of retlist',ret.qsize()
            print 'size of datalist',data.qsize()
            print 'size of exceptlist',error.qsize()
            print 'size of settable',settable.qsize()
            print 'state of work(not 0 mean off)',control.qsize()
            print 'state of master(not 0 mean off)',master.qsize()
            print 'state of center(not 0 mean off)',center.qsize()
            print 'state of data(not 0 mean off)',datac.qsize()
            print '----------------------------'
            continue
        if code == 'showerror':
            for i in range(error.qsize()):
                print error.get()
            continue
        time.sleep(1)
if __name__ == '__main__':
    controler()
    os.system('pause')
