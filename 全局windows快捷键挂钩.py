# _*_ coding:UTF-8 _*_  
import win32con
import ctypes
import ctypes.wintypes
import threading
user32 = ctypes.windll.user32

class Hotkey:
    EXIT = False
    regdict = {}
    tempids = list(range(1000))
    EXIT_ID = 1000

    def run(self):
        for tid in self.regdict:
            '''
            需要注意的是，注册函数需要和捕捉任务的线程一致，否则注册无效。
            '''
            if not user32.RegisterHotKey(None, tid, 0, self.regdict[tid]['key']):
                print("rebind register id", self.regdict[tid]['key'])
                user32.UnregisterHotKey(None, self.regdict[tid]['key'])
        try:  
            msg = ctypes.wintypes.MSG()  
            while True:
                if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:  
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
            '''
            默认检测程序是否设计了退出的快捷键，没有则强制报错
            '''
            if self.EXIT_ID not in self.regdict:
                raise KeyError('exit callback not included, pls use "Hotkey.regexit" func reg it.')
        threading.Thread(target=self.run).start()

    def reg(self, key, callback=lambda:None):
        tid = self.tempids.pop()
        self.regdict[tid] = {'key':key, 'callback':callback}

    def regexit(self, key):
        self.regdict[self.EXIT_ID] = {'key':key, 'callback':lambda:None}

if __name__ == '__main__':
    hotkey = Hotkey()  
    hotkey.regexit(win32con.VK_F10)
    hotkey.reg(win32con.VK_F9, lambda:print(123123))
    hotkey.start()
