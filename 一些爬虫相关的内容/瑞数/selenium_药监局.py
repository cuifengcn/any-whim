# 区别于直接用调试模式打开浏览器，这里可以绕过大部分浏览器指纹检测
# 这里的原理是，通过正常启动一个浏览器，并且让这个浏览器打开 remote-debugging-port 端口
# 让 selenium 在其正常启动之后再以调试模式连接上来，经测试，能绕过瑞数加密。
# 并且很有用的一点是，你这样绕过检测还能设置代理，这样
#   使用 mitmdump 做中间代理的时候就能更好的调试各个请求的配置处理

def get_driver():
    def get_win_chrome_path():
        # 注意，要使用非硬盘版安装的 chrome 软件才会在注册表里面留有痕迹，才能使用这个函数快速定位软件地址
        # 通常来说 chrome 的安装一般都是非硬盘版的安装，所以这个函数算是在 windows 系统下获取 chrome.exe 路径的通解。
        import os, winreg
        sub_key = ['SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall', 'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall']
        def get_install_list(key, root):
            try:
                _key = winreg.OpenKey(root, key, 0, winreg.KEY_ALL_ACCESS)
                for j in range(0, winreg.QueryInfoKey(_key)[0]-1):
                    try:
                        each_key = winreg.OpenKey(root, key + '\\' + winreg.EnumKey(_key, j), 0, winreg.KEY_ALL_ACCESS)
                        displayname, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayName')
                        install_loc, REG_SZ = winreg.QueryValueEx(each_key, 'InstallLocation')
                        display_var, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayVersion')
                        yield displayname, install_loc, display_var
                    except WindowsError:
                        pass
            except:
                pass
        for key in sub_key:
            for root in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
                for name, local, var in get_install_list(key, root):
                    if name == 'Google Chrome':
                        return os.path.join(local, 'chrome.exe')
    chrome = get_win_chrome_path() # 尝试自动获取 chrome.exe 的地址
    driver = None # 如果有设置 chromedriver.exe 的环境变量，这里可以不用主动设置
    # driver = r'D:/Python/Python36/Scripts/chromedriver.exe'
    remote_port = 9223
    proxy_port = None # 8888 # 使用代理调试则将这里设置成代理端口既可，方便 mitmdump 等工具使用

    import os, shutil, subprocess
    chrome_path = shutil.which('chrome')       if not chrome else chrome # 在环境变量里面找文件的绝对地址
    driver_path = shutil.which('chromedriver') if not driver else driver # 在环境变量里面找文件的绝对地址
    assert chrome_path, "pls set chrome.exe path in env or set chrome=$abs_path(chrome.exe)."
    assert driver_path, "pls set chromedriver.exe path in env or set driver=$abs_path(chromedriver.exe)."

    # 临时 chrome 配置文件存放地址，防止破环日常使用的 chrome 配置
    # 另外，经过测试，如果删除掉旧的临时配置文件的地址，启动会块很多很多
    home = os.environ.get('HOME')
    home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
    home = os.path.join(home, 'auto_selenium', 'AutomationProfile')
    cache_path = os.path.split(home)[0]
    if os.path.isdir(cache_path):
        # print('cache_path clear: {}'.format(cache_path))
        shutil.rmtree(cache_path)
    # 如果想要使用代理
    if proxy_port: chrome_exe = '''"{}" --remote-debugging-port={} --user-data-dir="{}" --proxy-server=http://127.0.0.1:{}'''.format(chrome_path, remote_port, home, proxy_port)
    else:          chrome_exe = '''"{}" --remote-debugging-port={} --user-data-dir="{}"'''.format(chrome_path, remote_port, home)
    subprocess.Popen(chrome_exe)
    # print('driver_path: {}'.format(driver_path))
    # print('chrome_path: {}'.format(chrome_path))
    # print('chrome_exe: {}'.format(chrome_exe))

    import selenium
    from selenium import webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{}".format(remote_port))

    # 处理 document.$cdc_asdjflasutopfhvcZLmcfl_ 参数的指纹的检测
    def check_magic_word(driver_path, rollback=False):
        with open(driver_path, 'rb') as f: filebit = f.read()
        a, b = b'$cdc_asdjflasutopfhvcZLmcfl_', b'$pqp_nfqwsynfhgbcsuipMYzpsy_'
        a, b = (b, a) if rollback else (a, b)
        mgc_o, mgc_t = a, b
        if mgc_o in filebit: 
            with open(driver_path, 'wb') as f: f.write(filebit.replace(mgc_o, mgc_t))
    check_magic_word(driver_path, rollback=False)

    # 启动 webdriver
    webdriver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
    webdriver.set_page_load_timeout(5) # 让所有的 get 网页的加载都限制在 n秒钟内，防止无限加载的问题。
    _bak_get = webdriver.get
    def get(url):
        try:
            _bak_get(url)
        except selenium.common.exceptions.TimeoutException:
            print('selenium.common.exceptions.TimeoutException: {}'.format(url))
            get(url)
    webdriver.get = get

    # 设置:当你直接关闭浏览器时自动关闭 chromedriver.exe，防止进程残留
    import time, threading
    def hook_close_window():
        chrome_close = False
        while not chrome_close:
            time.sleep(.3) # 每0.3秒检测一次，如果强制关闭浏览器，则自动关闭 chromedriver.exe
            try:    driver_logs = webdriver.get_log('driver')
            except: driver_logs = []
            for i in driver_logs:
                if 'Unable to evaluate script: disconnected: not connected to DevTools' in i.get('message'):
                    chrome_close = True
                    webdriver.quit()
    threading.Thread(target=hook_close_window).start()
    return webdriver

driver = get_driver()
print(driver)
driver.get('http://app1.nmpa.gov.cn/data_nmpa/face3/dir.html')
print(driver.title)

# 10秒内，等待某个 xpath 元素出现，出现后立刻点击，若是出现错误，则刷新页面重新执行一遍
def wait_click(driver, xpath, time=10, maxtry=1):
    import traceback
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.wait import WebDriverWait as wbw
    locator = (By.XPATH, xpath)
    try:
        wbw(driver, time).until(EC.presence_of_element_located(locator))
        x = driver.find_element_by_xpath(xpath)
        x.click()
    except:
        print(traceback.format_exc())
        if maxtry <= 0: return
        driver.get(driver.current_url)
        wait_click(driver, xpath, time=10, maxtry=maxtry-1)

wait_click(driver, '/html/body/center/table[1]/tbody/tr[5]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/a')
import time;time.sleep(1)

import re
from lxml import etree

content = driver.page_source
tree = etree.HTML(re.sub(r'^ *<\?xml[^<>]+\?>', '', content))
for x in tree.xpath('//div[@id="content"]/div/table[2]/tbody/tr')[::2]:
    d = {}
    d["href"]  = (x.xpath('./td/p/a[@datas-ts]/@href') or [None])[0] # [cnt:15] [len:107] javascript:commitForECMA(callb...
    d["title"] = re.sub(r'\s+',' ',x.xpath('string(.)')).strip()
    execstr = re.findall(r'commitForECMA\([^\)]+\)', d["href"])[0]
    print('------------------------------ split ------------------------------')
    import pprint
    import time
    pprint.pprint(d)
    def get_info(maxretry=3):
        driver.execute_script(execstr)
        time.sleep(3)
        tempe = etree.HTML(driver.page_source)
        tempx = tempe.xpath('//div[@class="listmain"]/div/table[1]/tbody/tr')
        if not tempx and maxretry>0:
            print('正在重试，maxretry：{}'.format(maxretry))
            time.sleep(3) # 重试多等n秒
            return get_info(maxretry=maxretry-1)
        dd = {}
        for i in tempx:
            td = i.xpath('./td')
            if len(td) == 1:
                key = re.sub(r'\s+',' ',td[0].xpath('string(.)')).strip()
                value = ''
            elif len(td) == 2:
                key = re.sub(r'\s+',' ',td[0].xpath('string(.)')).strip()
                value = re.sub(r'\s+',' ',td[1].xpath('string(.)')).strip()
            else:
                print('error key:{}'.format(td))
            dd[key] = value
        return dd
    dd = get_info()
    pprint.pprint(dd)
    time.sleep(2)



