from multiprocessing.managers import BaseManager
import multiprocessing,time,os,json,glob

class man(BaseManager):pass
job = multiprocessing.Queue()
ret = multiprocessing.Queue()
data = multiprocessing.Queue()
control = multiprocessing.Queue()
error = multiprocessing.Queue()
master = multiprocessing.Queue()
settable = multiprocessing.Queue()
center = multiprocessing.Queue()
datacontrol = multiprocessing.Queue()
def _job():return job
def _ret():return ret
def _data():return data
def _control():return control
def _master():return master
def _error():return error
def _settable():return settable
def _center():return center
def _datacontrol():return datacontrol
man.register('joblists',callable=_job)
man.register('retlists',callable=_ret)
man.register('datalists',callable=_data)
man.register('controllist',callable=_control)
man.register('exceptlist',callable=_error)
man.register('mastercontrol',callable=_master)
man.register('settablelist',callable=_settable)
man.register('centercontrol',callable=_center)
man.register('datacontrol',callable=_datacontrol)

def add_job(lists):
    job = manager.joblists()
    for i in lists:
        print i
        job.put(i)

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
    manager.start()
    initf()

def initf():
    ret = manager.retlists()
    job = manager.joblists()
    error = manager.exceptlist()
    settable = manager.settablelist()
    fnames = []
    for i in glob.glob('*'):
        if i.split('@')[0] == 'save_queue':
            fnames.append(i)
    fnames.sort()
    try:
        fname = fnames[-1]
        print 'loading queue: ',fname
        f = open(fname,'r').read()
        queues = json.loads(f)
        if queues['joblist'] != []:
            for i in queues['joblist']:
                job.put(i)
        if queues['retlist'] != []:
            for i in queues['retlist']:
                ret.put(i)
        if queues['error'] != []:
            for i in queues['error']:
                error.put(i)
        if queues['settable'] != []:
            for i in queues['settable']:
                settable.put(i)
        print 'load ok'
    except:
        print 'save_queue loads fail or history file not exist'
    print '---------------------'

def run():
    init()
    center=manager.centercontrol()
    while 1:
        if center.empty():
            print 'center working: '+str(time.strftime("%H:%M:%S"))
            time.sleep(3)
            continue
        else:
            ends()
            print 'center out'
            break
    manager.shutdown()

def times(t = time.localtime()):
    return ''.join([str(i).rjust(2,'0') for i in t[0:6]])

def ends():
    job = manager.joblists()
    ret = manager.retlists()
    error = manager.exceptlist()
    settable = manager.settablelist()
    data = manager.datalists()
    s = {'joblist':[],'retlist':[],'error':[],'settable':[]}
    while 1:
        if data.qsize()==0:
            try:
                f = open('save_queue@'+times()+'.txt','w')
                if job.qsize() != 0:
                    for i in range(job.qsize()):
                        s['joblist'].append(job.get())
                if ret.qsize() != 0:
                    for i in range(ret.qsize()):
                        s['retlist'].append(ret.get())
                if error.qsize() != 0:
                    for i in range(error.qsize()):
                        s['error'].append(error.get())
                if settable.qsize() != 0:
                    for i in range(settable.qsize()):
                        s['settable'].append(settable.get())
                s['joblist'] = list(set(s['joblist']))
                s['retlist'] = list(set(s['retlist']))
                s['error'] = list(set(s['error']))
                f.write(json.dumps(s))
                f.close()
                print 'save ends ok.'
                break
            except:
                print 'ends error!!!'
        else:
            print 'please ensure your datalist has clear'
            time.sleep(3)

if __name__ == '__main__':
    run()
    os.system('pause')












