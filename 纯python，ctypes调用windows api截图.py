# mod by: https://github.com/BoboTiG/python-mss/tree/master/mss

import zlib
import ctypes
from struct import pack, calcsize
GetWindowDC             = ctypes.windll.user32.GetWindowDC
GetSystemMetrics        = ctypes.windll.user32.GetSystemMetrics
SelectObject            = ctypes.windll.gdi32.SelectObject
DeleteObject            = ctypes.windll.gdi32.DeleteObject
BitBlt                  = ctypes.windll.gdi32.BitBlt
GetDIBits               = ctypes.windll.gdi32.GetDIBits
CreateCompatibleDC      = ctypes.windll.gdi32.CreateCompatibleDC
CreateCompatibleBitmap  = ctypes.windll.gdi32.CreateCompatibleBitmap

def screenshot():
    def png_bit(data, size, level=6):
        width, height = size
        line = width * 3
        png_filter = pack(">B", 0)
        scanlines = b"".join(
            [png_filter + data[y * line : y * line + line] for y in range(height)][::-1]
        )
        magic = pack(">8B", 137, 80, 78, 71, 13, 10, 26, 10)
        ihdr = [b"", b"IHDR", b"", b""]
        ihdr[2] = pack(">2I5B", width, height, 8, 2, 0, 0, 0)
        ihdr[3] = pack(">I", zlib.crc32(b"".join(ihdr[1:3])) & 0xFFFFFFFF)
        ihdr[0] = pack(">I", len(ihdr[2]))
        idat = [b"", b"IDAT", zlib.compress(scanlines, level), b""]
        idat[3] = pack(">I", zlib.crc32(b"".join(idat[1:3])) & 0xFFFFFFFF)
        idat[0] = pack(">I", len(idat[2]))
        iend = [b"", b"IEND", b"", b""]
        iend[3] = pack(">I", zlib.crc32(iend[1]) & 0xFFFFFFFF)
        iend[0] = pack(">I", len(iend[2]))
        return magic + b"".join(ihdr + idat + iend)

    width, height = GetSystemMetrics(0),GetSystemMetrics(1)
    bmi      = pack('LHhHH', calcsize('LHHHH'), width, height, 1, 32)
    srcdc    = GetWindowDC(0)
    memdc    = CreateCompatibleDC(srcdc)
    svbmp    = CreateCompatibleBitmap(srcdc, width, height)
    SelectObject(memdc, svbmp); BitBlt(memdc, 0, 0, width, height, srcdc, 0, 0, 13369376)
    _data    = ctypes.create_string_buffer(height * width * 4)
    got_bits = GetDIBits(memdc, svbmp, 0, height, _data, bmi, 0)
    DeleteObject(memdc)
    data = bytes(_data)
    rgb = bytearray(width * height * 3)
    rgb[0::3],rgb[1::3],rgb[2::3] = data[2::4],data[1::4],data[0::4]
    size = (width, height)
    return png_bit(rgb, size) # 全屏截图 png bit 数据
    
if __name__ == '__main__':
    with open('screenshot.png','wb') as f:
        f.write(screenshot())
