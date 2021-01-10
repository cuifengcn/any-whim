import re, os
import urllib.parse

appdatapath = os.environ['APPDATA'] or os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')
pippath = os.path.join(appdatapath, 'pip')
pipfile = os.path.join(pippath, 'pip.ini')
if not os.path.isdir(pippath):
    os.mkdir(pippath)

def read_setting():
    if not os.path.isfile(pipfile):
        return None
    else:
        with open(pipfile) as f:
            setstr = f.read()
        mirrors = re.findall('\nmirrors = ([^\n]+)', setstr)[0]
        dic = {
            'http://pypi.douban.com/simple/': '豆瓣',
            'http://mirrors.aliyun.com/pypi/simple/': '阿里云',
            'http://pypi.tuna.tsinghua.edu.cn/simple/': '清华大学',
            'http://pypi.mirrors.ustc.edu.cn/simple/': '中国科学技术大学',
        }
        return dic.get(mirrors)

def write_setting(name):
    setting = '''[global]\nindex-url = {}\n[install]\nuse-mirrors = true\nmirrors = {}\ntrusted-host = {}'''.strip()
    dic = {
        '豆瓣': 'http://pypi.douban.com/simple/',
        '阿里云': 'http://mirrors.aliyun.com/pypi/simple/',
        '清华大学': 'http://pypi.tuna.tsinghua.edu.cn/simple/',
        '中国科学技术大学': 'http://pypi.mirrors.ustc.edu.cn/simple/',
    }
    if name not in dic:
        raise Exception("{} must in {}".format(name, list(dic)))
    mirrors = dic.get(name)
    index_url = mirrors.strip(' /')
    trusted_host = urllib.parse.urlsplit(index_url).netloc
    with open(pipfile, 'w') as f:
        f.write(setting.format(index_url, mirrors, trusted_host))

if __name__ == '__main__':
    write_setting('华中科技大学')
    v = read_setting()
    print(v)