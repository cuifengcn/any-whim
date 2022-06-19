import ctypes
import ctypes.wintypes
import threading
user32 = ctypes.windll.user32
class HotkeyHooker:
    EXIT = False
    regdict = {}
    combins = set()
    tempids = list(range(1000))
    EXIT_ID = 1000
    def run(self):
        for tid in self.regdict:
            if not user32.RegisterHotKey(None, tid, self.regdict[tid]['combine'], self.regdict[tid]['key']):
                print("rebind register id", self.regdict[tid]['key'])
                user32.UnregisterHotKey(None, self.regdict[tid]['key'])
        try:  
            msg = ctypes.wintypes.MSG()  
            while True:
                for modkey in self.combins:
                    if user32.GetMessageA(ctypes.byref(msg), None, modkey, 0) != 0:
                        if msg.message == 786: # win32con.WM_HOTKEY
                            if msg.wParam in self.regdict:
                                self.regdict[msg.wParam]['callback']()
                                if msg.wParam == self.EXIT_ID:
                                    return
                        user32.TranslateMessage(ctypes.byref(msg))
                        user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            for key in self.regdict:
                user32.UnregisterHotKey(None, key)

    def start(self, ensure_exit=True):
        if ensure_exit:
            if self.EXIT_ID not in self.regdict:
                raise KeyError('exit callback not included, pls use "HotkeyHooker.regexit" func reg it.')
        threading.Thread(target=self.run).start()
    def parse_combine(self, combine):
        if type(combine) == str:
            _combine = 0
            _combine = _combine|1 if 'alt'      in combine.lower() else _combine
            _combine = _combine|2 if 'control'  in combine.lower() else _combine
            _combine = _combine|4 if 'shift'    in combine.lower() else _combine
            _combine = _combine|8 if 'win'      in combine.lower() else _combine
            combine = _combine
        return combine
    def reg(self, key, combine=0, callback=lambda:None):
        if type(key) == str and len(key) == 1:
            key = ord(key.upper())
        combine = self.parse_combine(combine)
        self.combins.add(combine)
        self.regdict[self.tempids.pop()] = {
            'key':      key, 
            'callback': callback, 
            'combine':  combine,
        }
    def regexit(self, key, combine=0, callback=lambda:None):
        combine = self.parse_combine(combine)
        self.combins.add(combine)
        self.regdict[self.EXIT_ID] = {
            'key':      key, 
            'callback': callback, 
            'combine':  combine,
        }














# 遍历当前页面所有窗口的窗口名字
def enumerate_all_window_names():
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    titles = []
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titles

# 通过名字获取窗口的 numpy 类型的图片数据
import cv2
import numpy as np
from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND

GetDC = windll.user32.GetDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
GetClientRect = windll.user32.GetClientRect
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
SelectObject = windll.gdi32.SelectObject
BitBlt = windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = windll.gdi32.GetBitmapBits
DeleteObject = windll.gdi32.DeleteObject
ReleaseDC = windll.user32.ReleaseDC
def get_window_behind_by_name(name, x1x2y1y2=None):
    handle = ctypes.windll.User32.FindWindowW(None,name)
    windll.user32.SetProcessDPIAware()
    r = RECT()
    GetClientRect(handle, byref(r))
    width, height = r.right, r.bottom
    dc = GetDC(handle)
    cdc = CreateCompatibleDC(dc)
    bitmap = CreateCompatibleBitmap(dc, width, height)
    SelectObject(cdc, bitmap)
    BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)
    total_bytes = width*height*4
    buffer = bytearray(total_bytes)
    byte_array = c_ubyte*total_bytes
    GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
    DeleteObject(bitmap)
    DeleteObject(cdc)
    ReleaseDC(handle, dc)
    npimg = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
    b,g,r = map(lambda i:i[...,None],[npimg[...,0],npimg[...,1],npimg[...,2]])
    npimg = np.concatenate((b,g,r),axis=-1)
    if x1x2y1y2:
        x1, x2, y1, y2 = x1x2y1y2
        npimg = npimg[x1:x2, y1:y2]
    def test():
        cv2.imshow('123',npimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # test()
    return npimg

# 发送按键指令给窗口
from ctypes import windll
from ctypes.wintypes import HWND
import string
import time
PostMessageW = windll.user32.PostMessageW
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA
WM_KEYDOWN = 0x100
WM_KEYUP = 0x101
VkCode = {
    "back": 0x08,      "snapshot": 0x2C,  "separator": 0x6C, "end": 0x23,       "numpad5": 0x65,   "f7": 0x76,
    "tab": 0x09,       "insert": 0x2D,    "subtract": 0x6D,  "home": 0x24,      "numpad6": 0x66,   "f8": 0x77,
    "return": 0x0D,    "delete": 0x2E,    "decimal": 0x6E,   "left": 0x25,      "numpad7": 0x67,   "f9": 0x78,
    "shift": 0x10,     "lwin": 0x5B,      "divide": 0x6F,    "up": 0x26,        "numpad8": 0x68,   "f10": 0x79,
    "control": 0x11,   "rwin": 0x5C,      "f1": 0x70,        "right": 0x27,     "numpad9": 0x69,   "f11": 0x7A,
    "menu": 0x12,      "numpad0": 0x60,   "f2": 0x71,        "down": 0x28,      "multiply": 0x6A,  "f12": 0x7B,
    "pause": 0x13,     "numpad1": 0x61,   "f3": 0x72,        "print": 0x2A,     "add": 0x6B,       "numlock": 0x90,
    "capital": 0x14,   "numpad2": 0x62,   "f4": 0x73,        "scroll": 0x91,    "lshift": 0xA0,    "rshift": 0xA1,
    "escape": 0x1B,    "numpad3": 0x63,   "f5": 0x74,        "lcontrol": 0xA2,  "rcontrol": 0xA3,  "lmenu": 0xA4,
    "space": 0x20,     "numpad4": 0x64,   "f6": 0x75,        "rmenu": 0XA5
}
def get_virtual_keycode(key: str):
    return (VkKeyScanA(ord(key)) & 0xff) if len(key) == 1 and key in string.printable else VkCode[key]
def key_down(handle, key: str):
    if type(handle) == str: handle = ctypes.windll.User32.FindWindowW(None,handle)
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    wparam = vk_code
    lparam = (scan_code << 16) | 1
    PostMessageW(handle, WM_KEYDOWN, wparam, lparam)
def key_up(handle, key: str):
    if type(handle) == str: handle = ctypes.windll.User32.FindWindowW(None,handle)
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    wparam = vk_code
    lparam = (scan_code << 16) | 0XC0000001
    PostMessageW(handle, WM_KEYUP, wparam, lparam)

















import ctypes
import time

SendInput = ctypes.windll.user32.SendInput
MapVirtualKey = ctypes.windll.user32.MapVirtualKeyW
MAPVK_VK_TO_VSC = 0
PUL = ctypes.POINTER(ctypes.c_ulong)
VkCodeList = {
    "back": 0x08,      "snapshot": 0x2C,  "separator": 0x6C, "end": 0x23,       "numpad5": 0x65,   "f7": 0x76,
    "tab": 0x09,       "insert": 0x2D,    "subtract": 0x6D,  "home": 0x24,      "numpad6": 0x66,   "f8": 0x77,
    "return": 0x0D,    "delete": 0x2E,    "decimal": 0x6E,   "numpad7": 0x67,   "f9": 0x78,        "left": MapVirtualKey(0x25, MAPVK_VK_TO_VSC),
    "shift": 0x10,     "lwin": 0x5B,      "divide": 0x6F,    "numpad8": 0x68,   "f10": 0x79,       "up": MapVirtualKey(0x26, MAPVK_VK_TO_VSC),
    "control": 0x11,   "rwin": 0x5C,      "f1": 0x70,        "numpad9": 0x69,   "f11": 0x7A,       "right": MapVirtualKey(0x27, MAPVK_VK_TO_VSC),
    "menu": 0x12,      "numpad0": 0x60,   "f2": 0x71,        "multiply": 0x6A,  "f12": 0x7B,       "down": MapVirtualKey(0x28, MAPVK_VK_TO_VSC),
    "pause": 0x13,     "numpad1": 0x61,   "f3": 0x72,        "print": 0x2A,     "add": 0x6B,       "numlock": 0x90,
    "capital": 0x14,   "numpad2": 0x62,   "f4": 0x73,        "scroll": 0x91,    "lshift": 0xA0,    "rshift": 0xA1,
    "escape": 0x1B,    "numpad3": 0x63,   "f5": 0x74,        "lcontrol": 0xA2,  "rcontrol": 0xA3,  "lmenu": 0xA4,
    "space": 0x20,     "numpad4": 0x64,   "f6": 0x75,        "rmenu": 0XA5
}
def get_vkcode(key: str):
    return (VkKeyScanA(ord(key)) & 0xff) if len(key) == 1 and key in string.printable else VkCodeList[key]
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
def down_up(key, times=0.5):
    code = get_vkcode(key)
    PressKey(code)
    import time
    time.sleep(times)
    ReleaseKey(code)


















def get_match(exp, titles):
    import re
    rets = []
    for title in titles:
        if re.findall(exp, title):
            rets.append(title)
    return rets

def get_jwt_window_bg(name):
    return get_window_behind_by_name(name, [530, 530+65, 150, 150+750])

def get_jwt_window_bar(name):
    return get_window_behind_by_name(name)

def findmatchtemplate_np_muti(front_np, bg_np, match_threshold=0.96, nms_threshold=0.5):
    def pre_deal(v, left=180, right=240):
        # v = cv2.cvtColor(v, cv2.COLOR_BGR2GRAY)
        # v = cv2.Canny(v, left, right)
        return v
    bg_np = cv2.pyrMeanShiftFiltering(bg_np, 5, 50)
    img1 = pre_deal(front_np)
    img2 = pre_deal(bg_np)
    w, h = img1.shape[:2]
    v = cv2.matchTemplate(img2,img1,cv2.TM_CCORR_NORMED)
    index = np.where(v > match_threshold)
    infos = []
    for idx, i in enumerate(zip(*index[::-1])):
        xy1xy2 = [i[0], i[1], i[0]+w, i[1]+h]
        infos.append(xy1xy2)
    def nms(infos):
        if not infos: return infos
        def iou(xyxyA,xyxyB):
            ax1,ay1,ax2,ay2 = xyxyA
            bx1,by1,bx2,by2 = xyxyB
            minx, miny = max(ax1,bx1), max(ay1, by1)
            maxx, maxy = min(ax2,bx2), min(ay2, by2)
            intw, inth = max(maxx-minx, 0), max(maxy-miny, 0)
            areaA = (ax2-ax1)*(ay2-ay1)
            areaB = (bx2-bx1)*(by2-by1)
            areaI = intw*inth
            return areaI/(areaA+areaB-areaI)
        rets = []
        infos = infos[::-1]
        while infos:
            curr = infos.pop()
            if rets and any([iou(r, curr) > nms_threshold for r in rets]):
                continue
            rets.append(curr)
        return rets
    infos = nms(infos)
    def test():
        timg = img2.copy()
        for x1, y1, x2, y2 in infos:
            timg = cv2.rectangle(timg, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.imshow('nier', timg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # test()
    return infos

class JWT:
    def __init__(self, name):
        self.np_up = cv2.imread('./up.png')
        self.np_down = cv2.imread('./down.png')
        self.np_left = cv2.imread('./left.png')
        self.np_right = cv2.imread('./right.png')
        self.np_l_up = cv2.imread('./l_up.png')
        self.np_l_down = cv2.imread('./l_down.png')
        self.np_r_up = cv2.imread('./r_up.png')
        self.np_r_down = cv2.imread('./r_down.png')

        self.np_red_up = cv2.imread('./red_up.png')
        self.np_red_down = cv2.imread('./red_down.png')
        self.np_red_left = cv2.imread('./red_left.png')
        self.np_red_right = cv2.imread('./red_right.png')
        self.np_red_l_up = cv2.imread('./red_l_up.png')
        self.np_red_l_down = cv2.imread('./red_l_down.png')
        self.np_red_r_up = cv2.imread('./red_r_up.png')
        self.np_red_r_down = cv2.imread('./red_r_down.png')
        titles = get_match(name, enumerate_all_window_names())
        if not titles:
            raise Exception('没有找到窗口')
        self.window_name = titles[0]

    def get_side(self, np_side, np_bg, name):
        ret = []
        for i in findmatchtemplate_np_muti(np_side, np_bg):
            ret.append([name, i])
        return ret

    def get_list(self):
        np_bg = get_jwt_window_bg(self.window_name)
        v_list = []
        v_list.extend(self.get_side(self.np_up, np_bg, 'up'))
        v_list.extend(self.get_side(self.np_down, np_bg, 'down'))
        v_list.extend(self.get_side(self.np_left, np_bg, 'left'))
        v_list.extend(self.get_side(self.np_right, np_bg, 'right'))
        v_list.extend(self.get_side(self.np_l_up, np_bg, 'l_up'))
        v_list.extend(self.get_side(self.np_l_down, np_bg, 'l_down'))
        v_list.extend(self.get_side(self.np_r_up, np_bg, 'r_up'))
        v_list.extend(self.get_side(self.np_r_down, np_bg, 'r_down'))

        v_list.extend(self.get_side(self.np_red_up, np_bg, 'red_up'))
        v_list.extend(self.get_side(self.np_red_down, np_bg, 'red_down'))
        v_list.extend(self.get_side(self.np_red_left, np_bg, 'red_left'))
        v_list.extend(self.get_side(self.np_red_right, np_bg, 'red_right'))
        v_list.extend(self.get_side(self.np_red_l_up, np_bg, 'red_l_up'))
        v_list.extend(self.get_side(self.np_red_l_down, np_bg, 'red_l_down'))
        v_list.extend(self.get_side(self.np_red_r_up, np_bg, 'red_r_up'))
        v_list.extend(self.get_side(self.np_red_r_down, np_bg, 'red_r_down'))

        v_list = sorted(v_list, key=lambda a:a[1][0])
        v_list = [i[0] for i in v_list]
        return v_list

    def run(self, s_list):
        print(s_list)
        # 暂时无法实现模拟键盘操作，后面再看情况搞搞。


        # import time
        # time.sleep(3)
        # from pykeyboard import PyKeyboard
        # k = PyKeyboard()
        # k.press_key('H')
        # time.sleep(0.2)
        # k.release_key('H')
        # down_up('a')

        # import pydirectinput
        # import time; time.sleep(2)
        # for key in s_list:
        #     print(key)
        #     pydirectinput.press(key)
        #     pydirectinput.keyDown(key)
        #     pydirectinput.keyUp(key)


        # for key in s_list:
        #     print(key)
        #     key_down(self.window_name, key)
        #     key_up(self.window_name, key)

        # sider = {
        #     "left": 0x25,
        #     "up": 0x26,
        #     "right": 0x27,
        #     "down": 0x28,
        # }
        # import time; time.sleep(2)
        # for key in s_list:
        #     print(key)
        #     PressKey(sider[key])
        #     ReleaseKey(sider[key])
 



jwt = JWT('劲舞团[^区]+区')
jwt.run(jwt.get_list())

# import time
# jwt = JWT()
# VK_F1 = 112
# VK_F2 = 113
# hotkey = HotkeyHooker()  
# hotkey.regexit(VK_F2, 'alt')
# hotkey.reg(VK_F1, 'alt', lambda:jwt.run(jwt.get_list()))
# hotkey.start()