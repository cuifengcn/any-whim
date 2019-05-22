# pyinstaller 打包 scrapy 项目成一个 exe 文件的方式

r'''
# 通过 pyinstaller 将 scrapy 的项目打包成一个 exe 文件
# 这里不考虑说明 scrapy 需要怎么通过脚本配置命令行那些简单就能实现的功能，
# 就为了简单的说明怎么将项目和依赖库打包成一个 exe 的功能过程，下面的代码将只是简单执行一次爬虫，什么都不配置
# 下面的这段就是需要打包的脚本，很像是一个很简单的执行 scrapy 的脚本
# 不过需要注意的是下面关于工作空间的那三行，这里的理由我不会说得太清楚，
# 简短的说就是 pyinstaller 打包的单个exe文件执行过程是将所有的依赖和数据先释放在 TEMP 空间
#     然后再在 TEMP 临时文件空间里面执行，执行完毕然后删除 TEMP 空间缓存。
#     所以要在生成项目文件的时候找到项目空间的地址，转移执行空间才能通过 get_project_settings 找到项目
#     才能通过名字找到需要执行的爬虫

import os
import sys
import redis # 如果需要使用 scrapy_redis 那么就需要引入 redis
ocwd = os.getcwd()
tcwd = os.path.join(sys._MEIPASS)
os.chdir(tcwd)
# 通过 os.chdir 将工作空间转到实际存放了项目文件地址的地方。
# 这样 get_project_settings 才能找到项目，才能通过名字找到需要启动的爬虫
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
sett = {'host': '47.99.126.229', 'port': 6379, 'password': 'vilame'}
settings['REDIS_PARAMS'].update(sett) # 配置连接方式
process = CrawlerProcess(settings)
process.crawl('v')
os.chdir(ocwd)
process.start()

# 上面的脚本注意：
# 注意 $myproject 这个关键字就是项目包的名字
# 也就是 startproject 这个参数不含路径的文件夹的名字

打包步骤：
0. 找到你的 startproject 的文件夹地址，就是里面有 scrapy.cfg 文件的文件夹地址改写该脚本的 startproject 参数
    （因为该工具是将项目也打包进一个exe文件，所以需要项目的地址）
    （地址还是怕搞错的话，这里多啰嗦一点）
    （按照我的示例，我的 scrapy.cfg 地址在：C:\Users\Administrator\Desktop\mytest1\scrapy.cfg）
    （所以我要将下面的代码改成 startproject = r'C:\Users\Administrator\Desktop\mytest1'）
1. 在随便一个非scrapy项目地址创建一个任意名字python的脚本 scriptname.py，把上面的注释内的脚本内容拷贝进去
    （注意 $myproject 的修改，修改成 startproject 不含路径的文件夹的名字）
    （按照我的例子我就应该修改成 tcwd = os.path.join(sys._MEIPASS, 'mytest1') 即可）
2. 先直接 pyinstaller -F scriptname.py 生成 scriptname.spec 文件
3. 执行本脚本（注意要修改 startproject 的值后再实行），将打印出的所有可能几千行的内容直接复制，
    以文本编辑器模式打开 scriptname.spec 文件，将复制到的内容全部粘贴到
    binaries=[] 这的中括号里面，注意不要复制粘贴错了。注意不要删除中括号。
4. 直接执行 pyinstaller -F scriptname.spec 这样就可以生成想要的exe文件了。
    （注意这里的命令是对 spec 文件使用的。）

*5. 需要注意的是，脚本实际执行的地址是TEMP空间，所以如果需要考虑生成文件或是其他的时候。
    程序执行地址不是exe所在地址，所以，以上脚本有使用到生成文件功能时注意使用绝对地址。
    或者直接拼接以上脚本内的 ocwd 这个参数生成在 exe 文件处即可。

后续要进行更多的配置的话，通过修改 scriptname.py 来增加各种配置
打包的话，还是要 pyinstaller -F scriptname.spec 来进行打包。
以后我说不定会考虑一键打包的功能，不过现在感觉已经把该说的都说得很清楚了，感觉应该够用了。
'''

import os
import sys
import types
import shutil

spec_path = []
def mk_contain_binaries(*files_paths):
    for files_path in files_paths:
        rfiles_path = os.path.split(files_path)[0]
        for path,_,files in os.walk(files_path):
            for file in files:
                filepath = os.path.join(path,file)
                if not path.endswith('__pycache__'):
                    p1 = filepath
                    p2 = path.replace(rfiles_path,'')
                    fmt = r'({},{}),'.format(repr(p1),repr(p2))
                    spec_path.append(fmt)

def mk_contain_startproject(file_path):
    rfiles_path,rname = os.path.split(file_path)
    for path,_,files in os.walk(file_path):
        for file in files:
            filepath = os.path.join(path,file)
            if not path.endswith('__pycache__'):
                p1 = filepath
                p2 = '.' + path.replace(rfiles_path,'').split(rname,1)[1]
                fmt = r'({},{}),'.format(repr(p1),repr(p2))
                spec_path.append(fmt)

def mk_contain_dlls():
    dlls = os.path.join(os.path.split(sys.executable)[0],'DLLs')
    for path,_,files in os.walk(dlls):
        for file in files:
            p1 = os.path.join(path,file)
            p2 = '.'
            fmt = r'({},{}),'.format(repr(p1),repr(p2))
            spec_path.append(fmt)

def mk_comtain_modules(*modules):
    pas = []
    for md in modules:
        import importlib
        p = importlib.import_module(md)
        s = os.path.dirname(p.__file__)
        r = 'c:\\'+md
        v = 'copyfile {} to {}'.format(s,r)
        try:
            shutil.copytree(s,r)
        except:
            pass

        s = '''
import {}
if type({}) == types.ModuleType:
    pa,fi = os.path.split({}.__file__)
    pas.append(pa)
'''.format(md,md,md)
        exec(s)
    mk_contain_binaries(*pas)

# 需要直接包进去的 scrapy 项目包（注意修改）
startproject = r'C:\Users\zhoulin08\Desktop\pj\vscrapy'

# 需要包入函数库的函数包（对 scrapy 项目打包必须要下列几个函数库包）
modules = (
    'scrapy',
    'email',
    'twisted',
    'queuelib',
    'sqlite3',
)

mk_comtain_modules(*modules)
mk_contain_startproject(startproject)
mk_contain_dlls()
for i in spec_path:
    print(i)
