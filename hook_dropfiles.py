def hook_dropfiles(hwnd,func=lambda i:print(i)):
    import ctypes
    from ctypes.wintypes import DWORD
    prototype = ctypes.WINFUNCTYPE(DWORD,DWORD,DWORD,DWORD,DWORD)
    WM_DROPFILES = 0x233
    GWL_WNDPROC = -4

    def py_drop_func(hwnd,msg,wp,lp):
        if msg == WM_DROPFILES:
            count = ctypes.windll.shell32.DragQueryFile(wp,-1,None,None)
            szFile = ctypes.c_buffer(260)
            for i in range(count):
                ctypes.windll.shell32.DragQueryFile(wp,i,szFile,ctypes.sizeof(szFile))
                dropname = szFile.value
                func(dropname)
            ctypes.windll.shell32.DragFinish(wp)
        return ctypes.windll.user32.CallWindowProcW(org_wndproc,hwnd,msg,wp,lp)

    global org_wndproc,new_wndproc
    org_wndproc = None
    new_wndproc = prototype(py_drop_func)

    ctypes.windll.shell32.DragAcceptFiles(hwnd,True)
    org_wndproc = ctypes.windll.user32.GetWindowLongW(hwnd,GWL_WNDPROC)
    ctypes.windll.user32.SetWindowLongW(hwnd,GWL_WNDPROC,new_wndproc)
