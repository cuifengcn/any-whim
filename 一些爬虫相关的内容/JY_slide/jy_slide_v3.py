# 处理 selenium 移动滑块时候的卡顿问题
import selenium.webdriver.common.actions.pointer_input as pointer
pointer.PointerInput.DEFAULT_MOVE_DURATION = 20
pointer.PointerInput._bak_create_pointer_move = pointer.PointerInput.create_pointer_move
def create_pointer_move(self, *a, **kw):
    kw['duration'] = 1
    return self._bak_create_pointer_move(*a, **kw)
pointer.PointerInput.create_pointer_move = create_pointer_move

import cv2
import numpy as np
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as wbw

import time
import base64
import random
import threading
from io import BytesIO

def read_from_bytes(bytes_img, size=None):
    image_data = BytesIO(bytes_img)
    img = Image.open(image_data)
    if size:
        img = img.resize(size)
    img = np.asarray(img)
    return img

def read_from_b64string(str_img, size=None):
    image_data = BytesIO(base64.b64decode(str_img.split('base64,', 1)[1]))
    img = Image.open(image_data)
    if size:
        img = img.resize(size)
    img = np.asarray(img)
    return img

def findmatchtemplate_np(front_np, bg_np):
    def canny(v, left=180, right=240):
        s = cv2.cvtColor(v, cv2.COLOR_BGR2GRAY)
        s = cv2.Canny(s, left, right)
        return s
    bg_np = cv2.pyrMeanShiftFiltering(bg_np, 5, 50)
    img1 = canny(front_np)
    img2 = canny(bg_np)
    w, h = img1.shape[:2]
    v = cv2.matchTemplate(img2,img1,cv2.TM_CCOEFF)
    a, b, c, left_top = cv2.minMaxLoc(v)
    def accurate(left_top, canny_img1):
        s = canny_img1
        v = []
        for idx,i in enumerate(s):
            if any(i):
                v.append(idx)
        gt = v[0]
        h = v[-1] - v[0]
        s = s.T
        v = []
        for idx,i in enumerate(s):
            if any(i):
                v.append(idx)
        gl = v[0]
        w = v[-1] - v[0]
        t, l = left_top[1]+gt, left_top[0]+gl
        return t, l, w, h
    t, l, w, h = accurate(left_top, img1)
    def test():
        cv2.imshow('nier1', img1)
        cv2.imshow('nier2', img2)
        img3 = bg_np
        img3 = cv2.rectangle(img3, (l, t), (l+h, t+w), (0,255,0), 2)
        cv2.imshow('nier', img3)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    test() # 使用时注释这行就可以了
    return t, l, w, h

def get_geetest_slide_bg_img(img):
    cop = np.zeros((160, 260, 3))
    sls = [
      [ 157, 80 ], [ 145, 80 ], [ 265, 80 ], [ 277, 80 ],
      [ 181, 80 ], [ 169, 80 ], [ 241, 80 ], [ 253, 80 ],
      [ 109, 80 ], [ 97, 80 ],  [ 289, 80 ], [ 301, 80 ],
      [ 85, 80 ],  [ 73, 80 ],  [ 25, 80 ],  [ 37, 80 ],
      [ 13, 80 ],  [ 1, 80 ],   [ 121, 80 ], [ 133, 80 ],
      [ 61, 80 ],  [ 49, 80 ],  [ 217, 80 ], [ 229, 80 ],
      [ 205, 80 ], [ 193, 80 ], [ 145, 0 ],  [ 157, 0 ],
      [ 277, 0 ],  [ 265, 0 ],  [ 169, 0 ],  [ 181, 0 ],
      [ 253, 0 ],  [ 241, 0 ],  [ 97, 0 ],   [ 109, 0 ],
      [ 301, 0 ],  [ 289, 0 ],  [ 73, 0 ],   [ 85, 0 ],
      [ 37, 0 ],   [ 25, 0 ],   [ 1, 0 ],    [ 13, 0 ],
      [ 133, 0 ],  [ 121, 0 ],  [ 49, 0 ],   [ 61, 0 ],
      [ 229, 0 ],  [ 217, 0 ],  [ 193, 0 ],  [ 205, 0 ]
    ]
    for i in range(len(sls)):
        n_l, n_t = i % 26 * 10, int(i / 26) * 80
        o_l, o_t = sls[i]
        cop[n_t:n_t+80:,n_l:n_l+10,:] = img[o_t:o_t+80:,o_l:o_l+10,:]
    return cop.astype('uint8')

def get_driver():
    from selenium import webdriver
    option = webdriver.ChromeOptions()
    extset = ['enable-automation', 'ignore-certificate-errors']
    ignimg = "profile.managed_default_content_settings.images"
    mobile = {'deviceName':'Galaxy S5'}

    # 需要哪些 driver 功能，请解开对应的代码注释再启动
    option.add_argument("--disable-infobars")                       # 关闭调试信息
    option.add_experimental_option("excludeSwitches", extset)       # 关闭调试信息
    option.add_experimental_option("useAutomationExtension", False) # 关闭调试信息
    # option.add_argument('--start-maximized')                        # 最大化
    # option.add_experimental_option('mobileEmulation', mobile)     # 手机模式
    # option.add_experimental_option("prefs", {ignore_image: 2})    # 不加载图片
    # option.add_argument('--headless')                             # 【*】 无界面
    # option.add_argument('--no-sandbox')                           # 【*】 沙箱模式
    # option.add_argument('--disable-dev-shm-usage')                # 【*】 in linux
    # option.add_argument('--window-size=1920,1080')                # 无界面最大化
    # option.add_argument('--disable-gpu')                          # 禁用 gpu 加速
    # option.add_argument("--auto-open-devtools-for-tabs")          # F12
    # option.add_argument("--user-agent=Mozilla/5.0 VILAME")        # 修改 UA
    # option.add_argument('--proxy-server=http://127.0.0.1:8888')   # 代理

    webdriver = webdriver.Chrome(options=option, executable_path='chromedriver')
    webdriver.set_page_load_timeout(5)
    _bak_get = webdriver.get
    def get(url):
        import selenium
        try:
            _bak_get(url)
        except selenium.common.exceptions.TimeoutException:
            print('selenium.common.exceptions.TimeoutException: {}'.format(url))
            get(url)
    webdriver.get = get
    webdriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": r"""
            function get_url_params(url) {
                let arrObj = url.split("?");
                let params = Object.create(null)
                if (arrObj.length > 1) {
                    arrObj = arrObj[1].split("&");
                    arrObj.forEach(item=>{
                        item = item.split("=");
                        params[item[0]] = item[1]
                    }
                    )
                }
                return params;
            }
            window.v_cache_src = []
            var v_appendChild = Node.prototype.appendChild
            Node.prototype.appendChild = function(v){
                if (v.src && v.src.indexOf('_BBF=') != -1){
                    var x = /&callback=(geetest_\d+)/.exec(v.src)
                    if (x){
                        var func = window[x[1]]
                        var params = get_url_params(v.src)
                        window[x[1]] = function(data){
                            var temp = Object.assign(data, params)
                            var ret = {}
                            ret.gt = temp.gt
                            ret.validate = temp.validate
                            ret.challenge = temp.challenge
                            ret.client_type = temp.client_type
                            ret.lang = temp.lang
                            ret.message = temp.message
                            ret.score = temp.score
                            window.v_cache_src.push(ret)
                            return func.apply(this, arguments)
                        }
                    }
                }
                return v_appendChild.apply(this, arguments)
            }
            var _drawImage = CanvasRenderingContext2D.prototype.drawImage
            window.image_draw_cache = []
            CanvasRenderingContext2D.prototype.drawImage = function(a,b,c){
                if (window.image_draw_cache.indexOf(a) == -1){
                    window.image_draw_cache.push(a)
                }
                return _drawImage.apply(this, arguments)
            }
        """
    })
    webdriver.execute_cdp_cmd("Network.enable", {})
    toggle = { "chrome_close": False }
    webdriver._quit = webdriver.quit
    def quit(*a, **kw):
        toggle['chrome_close'] = True
        return webdriver._quit(*a, **kw)
    webdriver.quit = quit
    webdriver._close = webdriver.close
    def close(*a, **kw):
        toggle['chrome_close'] = True
        return webdriver._close(*a, **kw)
    webdriver.close = close
    import time, threading
    def hook_close_window():
        toggle['chrome_close'] = False
        while not toggle['chrome_close']:
            time.sleep(.3)
            try:    driver_logs = webdriver.get_log('driver')
            except Exception as e: 
                if 'Failed to establish a new connection' in str(e):
                    toggle['chrome_close'] = True
                driver_logs = []
            for i in driver_logs:
                if 'Unable to evaluate script: disconnected: not connected to DevTools' in i.get('message'):
                    toggle['chrome_close'] = True
                    webdriver.quit()
    threading.Thread(target=hook_close_window).start()
    return webdriver

def wait_exit(driver,xpath,sec=10):
    locator = (By.XPATH, xpath)
    wbw(driver,sec).until(EC.visibility_of_element_located(locator)) # 判断某个元素是否被添加到了dom里并且可见，即宽和高都大于0

def get_verify_src(driver):
    driver.get('https://www.geetest.com/demo/slide-float.html')
    wait_exit(driver, '//div[@class="geetest_radar_tip"]')
    driver.find_element(by=By.XPATH, value='//div[@class="geetest_radar_tip"]').click()
    time.sleep(1) # （滑块出现时，会有短暂的自动滑动动画，等待自动滑动结束）
    wait_exit(driver, '//canvas[@class="geetest_canvas_bg geetest_absolute"]')
    imgs = driver.execute_script('''return (function(){
        function getBase64(img) {
            var canvas = document.createElement("canvas")
            canvas.width = img.width
            canvas.height = img.height
            canvas.getContext("2d").drawImage(img, 0, 0, img.width, img.height)
            return canvas.toDataURL('image/jpeg')
        };
        var ret = {}
        for (var i = 0; i < window.image_draw_cache.length; i++) {
            if (window.image_draw_cache[i].src.indexOf("/slice/") != -1){
                ret.front = getBase64(window.image_draw_cache[i])
            }
            if (window.image_draw_cache[i].src.indexOf("/bg/") != -1){
                ret.bg = getBase64(window.image_draw_cache[i])
            }
        }
        return ret
    })()''')
    front_np = read_from_b64string(imgs['front'])
    bg_np = get_geetest_slide_bg_img(read_from_b64string(imgs['bg']))
    return front_np, bg_np

def drag_and_drop(driver, xpath, vlen):
    move_ele = driver.find_element(by=By.XPATH, value=xpath)
    from selenium.webdriver import ActionChains
    action_chains = ActionChains(driver)
    action_chains.drag_and_drop_by_offset(move_ele, vlen, 0).click_and_hold(move_ele).perform()

def drag_and_drop_tracks(driver, xpath, tracks):
    move_ele = driver.find_element(by=By.XPATH, value=xpath)
    from selenium.webdriver import ActionChains
    ActionChains(driver).click_and_hold(move_ele).perform()
    for idx, (x, y) in enumerate(tracks):
        if idx > len(tracks) * 0.9: time.sleep(0.05)
        if idx > len(tracks) * 0.8: time.sleep(0.05)
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=y).perform()
    ActionChains(driver).release(move_ele).perform()

def get_slide_track(distance):
    v = 0
    t = 0.2
    tracks = []
    current = 0
    mid = distance * 5/8
    distance += 10
    while current < distance:
        t = random.randint(1,4)/10
        a = random.randint(1,3) if current < mid else random.randint(2,4)
        v0 = v
        s = v0*t + 0.5*a*(t**2)
        current += s
        tracks.append(round(s))
        v = v0 + a*t
    temp = 10+round(current-distance)
    for i in range(5):
        num = -random.randint(1,3)
        tracks.append(num)
        temp += num
    tracks.append(abs(temp))if temp<0 else tracks.append(-temp)
    for idx,i in enumerate(tracks):
        tracks[idx] = [i, (i % 3)]
    return tracks

def chech_geetest_slide(driver, times=0):
    status = driver.execute_script('''return (function(){
        var ret = {}
        var x = document.getElementsByClassName('geetest_success_radar_tip_content')
        if (x.length && x[0].innerHTML.trim()){
            ret.status = 'success'
            ret.info = x[0].innerHTML
            return ret
        }
        var x = document.getElementsByClassName('geetest_radar_error_code')
        if (x.length && x[0].innerHTML.trim()){
            ret.status = 'fail'
            ret.info = x[0].innerHTML
            return ret
        }
        return {status: 'unknown'}
    })()''')
    if status['status'] == 'success':
        return True
    if status['status'] == 'fail':
        return False
    if status['status'] == 'unknown':
        if times > 5:
            return False
        time.sleep(.5)
        return chech_geetest_slide(driver, times+1)

def run_by_thread(func):
    threading.Thread(target=func).start()

def verify_login_slide(times=0):
    driver = get_driver()
    try:
        front_np, bg_np = get_verify_src(driver)
        tlwh = findmatchtemplate_np(front_np, bg_np)
        tracks = get_slide_track(tlwh[1]-5)
        drag_and_drop_tracks(driver, '//div[@class="geetest_slider_button"]', tracks)
        if chech_geetest_slide(driver):
            data = driver.execute_script('return window.v_cache_src')
            run_by_thread(driver.quit)
            if data:
                return data[0]
            raise Exception('unknown error')
        else:
            time.sleep(0.5)
            print('verify error retring...')
            run_by_thread(driver.quit)
            return verify_login_slide(times+1)
    except Exception as e:
        print(e)
        time.sleep(0.5)
        print('unknown error retring...')
        run_by_thread(driver.quit)
        return verify_login_slide(times+1)

for i in range(3):
    info = verify_login_slide()
    print(info)


# driver = get_driver()
# front_np, bg_np = get_verify_src(driver)
# tlwh = findmatchtemplate_np(front_np, bg_np)
# tracks = get_slide_track(tlwh[1]-5)
# drag_and_drop_tracks(driver, '//div[@class="geetest_slider_button"]', tracks)
# print('验证状态(true为成功)', chech_geetest_slide(driver))
# # driver.quit()