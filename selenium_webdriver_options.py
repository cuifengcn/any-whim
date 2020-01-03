from selenium import webdriver

option = webdriver.ChromeOptions()
extset = ['enable-automation', 'ignore-certificate-errors']
ignimg = "profile.managed_default_content_settings.images"
mobile = {'deviceName':'Galaxy S5'}
option.add_argument("--disable-infobars")                       # 旧版本关闭“chrome正受到自动测试软件的控制”信息
option.add_experimental_option("excludeSwitches", extset)       # 新版本关闭“chrome正受到自动测试软件的控制”信息
option.add_experimental_option("useAutomationExtension", False) # 新版本关闭“请停用以开发者模式运行的扩展程序”信息
# option.add_experimental_option('mobileEmulation', mobile)     # 是否使用手机模式打开浏览器
# option.add_experimental_option("prefs", {ignore_image: 2})    # 开启浏览器时不加载图片(headless模式该配置无效)
# option.add_argument('--start-maximized')                      # 开启浏览器时是否最大化(headless模式该配置无效)
# option.add_argument('--headless')                             # 无界面打开浏览器
# option.add_argument('--window-size=1920,1080')                # 无界面打开浏览器时候只能用这种方式实现最大化
# option.add_argument('--disable-gpu')                          # 禁用 gpu 硬件加速
# option.add_argument("--auto-open-devtools-for-tabs")          # 开启浏览器时候是否打开开发者工具(F12)
# option.add_argument("--user-agent=Mozilla/5.0 HELL")          # 修改 UA 信息
# option.add_argument('--proxy-server=http://127.0.0.1:8888')   # 增加代理

if __name__ == '__main__':
    wb = webdriver.Chrome(chrome_options=option)
    wb.get('http://baidu.com')
