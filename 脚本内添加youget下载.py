
# 获取信息
import builtins
import threading
import you_get.common
from you_get.common import url_to_module
from you_get.common import any_download
you_get.common.skip_existing_file_size_check = True # 跳过存在检查

def get_info_from_url(url): # 这里的挂钩不适用于多线程
    m, url = url_to_module(url)
    q = {}
    _org_print = print
    def _new_print(*a,**k):
        if len(a) >= 2:
            if a[0].startswith('Site'): q['Site'] = a[1]
            elif a[0].startswith('Title'): q['Title'] = a[1]
            elif a[0].startswith('Type'): q['Type'] = a[1]
            elif a[0].startswith('Size'): q['Size'] = a[1] # 单位(M)兆
            else: _org_print('uncatch info: {}'.format(a))
    builtins.print = _new_print
    m.download(url, info_only=True)
    builtins.print = _org_print
    return q

gt = threading.RLock()
def download_video_limit_size(url, output_dir='.', minsize=0, maxsize=float('inf')):
    with gt:
        info = get_info_from_url(url)
        size = info.get('Size')
        if size and size > minsize and size < maxsize:
            any_download(url, output_dir=output_dir)
            return info

url = 'http://vd4.bdstatic.com/mda-jiqbqq6evan2m0is/mda-jiqbqq6evan2m0is.mp4'
download_video_limit_size(url, 'asdf你好')
# 不考虑信息的话直接用 any_download 下载会更方便。 不过无法约束大小进行数据下载了。

# 使用 pyinstaller 打包的时候需要额外添加如下命令行内容
# --add-data "e:\python\python36\Lib\site-packages\you_get;you_get" --add-data "e:\python\python36\Lib\xml;xml" --add-data "e:\python\python36\Lib\html;html" --add-binary "e:\python\python36\Lib\_markupbase.py;."
# 其中上面的全部 e:\python\python36 改成 python.exe 所在的地址即可，
# 如果不知道请使用 import os, sys; print(os.path.dirname(sys.executable)) 查看