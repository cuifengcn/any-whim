# 学习透视相关的内容
# 尝试写一个 AssaultCube 游戏的透视外挂以便测试结果

# 开发环境 win10 python3.6
# 只能在局域网透视别人，目前没调试出 bot 的追踪。
# 由于用的画框的函数性能问题，追个一两个人还行，追踪太多人的轨迹可能还是有点卡。

import struct
from ctypes import *
from ctypes.wintypes import *

def get_all_pids_names():
    ret = []
    lpidProcess = (c_ulong * 256)()
    cb          = sizeof(lpidProcess)
    cbNeeded    = c_ulong()
    hModule     = c_ulong()
    count       = c_ulong()
    modname     = c_buffer(30)
    flag        = 0x0010 | 0x0400 # PROCESS_VM_READ|PROCESS_QUERY_INFORMATION
    windll.psapi.EnumProcesses(byref(lpidProcess), cb, byref(cbNeeded))
    pidProcess = [i for i in lpidProcess][:int(cbNeeded.value/sizeof(c_ulong()))]
    for pid in pidProcess:
        hProcess = windll.kernel32.OpenProcess(flag, False, pid)
        if hProcess:
            windll.psapi.EnumProcessModules(hProcess, byref(hModule), sizeof(hModule), byref(count))
            windll.psapi.GetModuleBaseNameA(hProcess, hModule.value, modname, sizeof(modname))
            ret.append((pid, b"".join([ i for i in modname if i != b'\x00'])))
            for i in range(modname._length_):
                modname[i] = b'\x00'
            windll.kernel32.CloseHandle(hProcess)
    return ret
def get_pid_from_name(name):
    pids_names = get_all_pids_names()
    name = name.encode() if isinstance(name,str) else name
    for pid, _name in pids_names:
        if name == _name:
            return pid

# 通过进程名获取进程的句柄
def get_process_handle(name):
    return windll.kernel32.OpenProcess(0x1f0fff, False, get_pid_from_name(name))

def read_buffer(hProcess, lpBaseAddress, nSize):
    lpBuffer = create_string_buffer(nSize)
    result = windll.kernel32.ReadProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize, 0)
    if result is None or result == 0:
        raise Exception('Error: %s' % GetLastError())
    return lpBuffer.raw

def byte_to_float(bytes):
    return struct.unpack('<f', struct.pack('4B', *bytes))[0]

def read_matrix(handle, addr):
    ret = []
    for g in range(16):
        if g % 4 == 0: ret.append([])
        bt = read_buffer(handle, addr+(g*4), 4)
        ret[-1].append(byte_to_float(bt))
    return ret

def read_list_float(handle, addr, num):
    ret = []
    for g in range(num):
        bt = read_buffer(handle, addr+(g*4), 4)
        ret.append(byte_to_float(bt))
    return ret

def read_addr(handle, addr):
    bt = read_buffer(handle, addr, 4)
    return int(''.join([hex(i)[2:] for i in bt][::-1]), 16)

# 在窗口画一个矩形
windc = None
def draw_rect(x1,y1,x2,y2):
    global windc
    if not windc: windc = windll.user32.GetDC(0)
    r = RECT(x1,y1,x2,y2)
    windll.user32.FrameRect(windc, byref(r), windll.gdi32.GetStockObject(0))

# 通过进程名获取该进程的窗口句柄
def get_window_size(handle):
    rect = RECT()
    try: # win10 的处理方式
        windll.dwmapi.DwmGetWindowAttribute(HWND(handle),
            ctypes.wintypes.DWORD(9),
            ctypes.byref(rect),
            ctypes.sizeof(rect) )
    except:
        windll.user32.GetWindowRect(handle, byref(rect))
    return rect.left, rect.top, rect.right, rect.bottom

# 通过进程名获取进程的窗口句柄
def get_window_handle(name):
    pid = get_pid_from_name(name)
    top = ctypes.windll.user32.GetTopWindow(None)
    handle = HWND()
    while top:
        hd = windll.user32.GetWindowThreadProcessId(top, byref(handle))
        if hd != 0 and pid == handle.value:
            if not windll.user32.GetParent(top) and windll.user32.IsWindowVisible(top):
                return top
        top = windll.user32.GetWindow(top, 2) # GW_HWNDNEXT

def read_value(hProcess, lpBaseAddress, nSize):
    lpBuffer = create_string_buffer(nSize)
    result = windll.kernel32.ReadProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize, 0)
    if result is None or result == 0:
        raise Exception('Error: %s' % GetLastError())
    return lpBuffer

def read_addr_list(handle, start_addr, offset_list=None):
    v = read_addr(handle, start_addr)
    if offset_list:
        for offset in offset_list:
            v = read_addr(handle, v + offset)
    return v

def get_enemies_addr_float(handle):
    # 获取其他玩家的坐标地址，需要从CE中调试出来
    ret = []
    for i in range(1,16):
        try:
            v = read_addr_list(handle, 0x0050F4F8, offset_list=[4*i])
            r = read_list_float(handle, v+0x34, 3)
            ret.append(r)
        except:
            pass
    return ret

def draw_enemies_rect(handle, whandle):
    M = read_matrix(handle, 0x00501AE8) # 自己矩阵信息，即摄像机信息，需要从CE中调试出来
    # Px, Py, Pz = [73.10000610351562, 118.89999389648438, -4] # 目标的世界坐标
    for Px, Py, Pz in get_enemies_addr_float(handle):
        head = 4 
        feet = -.5
        G = windll.user32.GetSystemMetrics
        if windll.user32.IsZoomed(whandle):
            L, T, R, B, H = 0, 0, G(0), G(1), 0
        else:
            (L, T, R, B), H = get_window_size(whandle), 0#G(4)
        Gx = int((R-L)/2)
        Gy = int((B-T)/2)
        VieW = Px * M[0][3] + Py * M[1][3] + Pz * M[2][3] + M[3][3]
        if VieW > 0:
            VieW = 1 / VieW
            Bx  = Gx + (Px * M[0][0] + Py * M[1][0] + Pz * M[2][0] + M[3][0]) * VieW * Gx
            By  = Gy - (Px * M[0][1] + Py * M[1][1] + (Pz+head) * M[2][1] + M[3][1]) * VieW * Gy
            By2 = Gy - (Px * M[0][1] + Py * M[1][1] + (Pz+feet) * M[2][1] + M[3][1]) * VieW * Gy
            wid = abs(By - By2)*.23
            x1, y1, x2, y2 = int(Bx-wid), int(By), int(Bx+wid), int(By2)
            x1, y1, x2, y2 = x1+int(L), y1+int(T)+H, x2+int(L), y2+int(T)+H
            draw_rect(x1, y1, x2, y2)

process_name = 'ac_client.exe' # 注意这里是进程名字，不是窗口名字
handle  = get_process_handle(process_name)
whandle = get_window_handle(process_name)

def run():
    while 1:
        draw_enemies_rect(handle, whandle)
        # import time
        # time.sleep(.01)

run()