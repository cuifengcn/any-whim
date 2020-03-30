s = r'''

        _$Kh = _$3v(_$CB(18));
        _$Zr = _$3v(_$CB(17));
        _$Ph = _$3v(_$CB(16));
        _$s8 = _$3v(_$CB(31));

    function _$IE(_$Jb) {
        var _$6H = [0, 1, 3, 7, 0xf, 0x1f];
        return (_$Jb >> _$u3._$u3) | ((_$Jb & _$6H[_$u3._$u3]) << (6 - _$u3._$u3));
    }

    function _$g7(_$Jb) {
        var _$6H = _$Jb.length, _$hS = 0, _$yA, _$Iz = 0;
        var _$ML = _$9M();
        var _$qf = new _$el(_$ML);
        while (_$hS < _$6H) {
            _$yA = _$9M();
            _$qf[_$Iz++] = _$du[_$Jx[0]](_$Jb, _$hS, _$yA);
            _$hS += _$yA;
        }
        _$CB = _$b2;
        function _$9M() {
            var _$6H = _$fI[_$K9[_$Jx[0]](_$Jb, _$hS++)];
            if (_$6H < 0) {
                return _$fI[_$K9[_$Jx[0]](_$Jb, _$hS++)] * 7396 + _$fI[_$K9[_$Jx[0]](_$Jb, _$hS++)] * 86 + _$fI[_$K9[_$Jx[0]](_$Jb, _$hS++)];
            } else if (_$6H < 64) {
                return _$6H;
            } else if (_$6H <= 86) {
                return _$6H * 86 + _$fI[_$K9[_$Jx[0]](_$Jb, _$hS++)] - 5440;
            }
        }
        function _$b2(_$if) {
            var _$6H = _$if % 64;
            var _$yA = _$if - _$6H;
            _$6H = _$IE(_$6H);
            _$6H ^= _$u3._$mz;
            _$yA += _$6H;
            return _$qf[_$yA];
        }
    }

    function _$tp(_$Jb) {
        var _$6H = _$Jb.length
          , _$yA = new _$el(_$tK[_$Jx[5]](_$6H * 3 / 4));
        var _$Iz, _$ML, _$9M, _$b2;
        var _$M8 = 0
          , _$Dm = 0
          , _$LV = _$6H - 3;
        for (_$M8 = 0; _$M8 < _$LV; ) {
            _$Iz = _$K9[_$Jx[0]](_$Jb, _$M8++);
            _$ML = _$K9[_$Jx[0]](_$Jb, _$M8++);
            _$9M = _$K9[_$Jx[0]](_$Jb, _$M8++);
            _$b2 = _$K9[_$Jx[0]](_$Jb, _$M8++);
            _$yA[_$Dm++] = _$cC[_$Iz] | _$Ok[_$ML];
            _$yA[_$Dm++] = _$Yj[_$ML] | _$le[_$9M];
            _$yA[_$Dm++] = _$_N[_$9M] | _$fI[_$b2];
        }
        if (_$M8 < _$6H) {
            _$Iz = _$K9[_$Jx[0]](_$Jb, _$M8++);
            _$ML = _$K9[_$Jx[0]](_$Jb, _$M8++);
            _$yA[_$Dm++] = _$cC[_$Iz] | _$Ok[_$ML];
            if (_$M8 < _$6H) {
                _$9M = _$K9[_$Jx[0]](_$Jb, _$M8);
                _$yA[_$Dm++] = _$Yj[_$ML] | _$le[_$9M];
            }
        }
        return _$yA;
    }
    function _$8o(_$Jb) {
        var _$6H = _$tp(_$Jb), _$yA = (_$6H[0] << 8) + _$6H[1], _$Iz = _$6H.length, _$ML;
        for (_$ML = 2; _$ML < _$Iz; _$ML += 2) {
            _$6H[_$ML] ^= (_$yA >> 8) & 0xFF;
            if (_$ML + 1 < _$Iz)
                _$6H[_$ML + 1] ^= _$yA & 0xFF;
            _$yA++;
        }
        return _$6H[_$Jx[1]](2);
    }
    function _$O7(_$Jb) {
        return _$sX(_$8o(_$Jb), _$hs(2, _$3n(9)));
    }
    function _$3n(_$Jb) {
        if (_$3n) {
            return;
        }
        _$3n = true;
        _$BC(_$9M, 0);
        var _$6H = _$PH && new _$PH();
        if (_$6H) {
            var _$yA = _$6H[_$Jx[428]];
            if (!_$yA) {
                return;
            }
            var _$Iz = _$yA[_$Jx[58]]();
            var _$ML = _$6B[_$Jx[0]](_$Iz, '\n');
            _$Iz = _$ML.pop();
            if (_$Iz === '' && _$ML.length > 0)
                _$Iz = _$ML.pop();
            if (_$Dv[_$Jx[0]](_$Iz, _$Jx[104]) !== -1 || _$6D(_$Iz, _$Jx[165]) || _$Iz === _$Jx[457]) {
                _$gW(_$Jb, 1);
                return true;
            }
        }
        function _$9M() {
            _$3n = false;
        }
    }
    function _$hs(_$Jb, _$_M) {
        _$Rm |= _$Jb;
        if (_$_M)
            _$8Y |= _$Jb;
    }


    function _$sX(_$Jb) {
        var _$6H = [], _$yA, _$Iz, _$ML, _$9M = _$K9[_$Jx[0]]('?', 0);
        for (_$yA = 0; _$yA < _$Jb.length; ) {
            _$Iz = _$Jb[_$yA];
            if (_$Iz < 0x80) {
                _$ML = _$Iz;
            } else if (_$Iz < 0xc0) {
                _$ML = _$9M;
            } else if (_$Iz < 0xe0) {
                _$ML = ((_$Iz & 0x3F) << 6) | (_$Jb[_$yA + 1] & 0x3F);
                _$yA++;
            } else if (_$Iz < 0xf0) {
                _$ML = ((_$Iz & 0x0F) << 12) | ((_$Jb[_$yA + 1] & 0x3F) << 6) | (_$Jb[_$yA + 2] & 0x3F);
                _$yA += 2;
            } else if (_$Iz < 0xf8) {
                _$ML = _$9M;
                _$yA += 3;
            } else if (_$Iz < 0xfc) {
                _$ML = _$9M;
                _$yA += 4;
            } else if (_$Iz < 0xfe) {
                _$ML = _$9M;
                _$yA += 5;
            } else {
                _$ML = _$9M;
            }
            _$yA++;
            _$6H.push(_$ML);
        }
        return _$0p(_$6H);
    }
    function _$0p(_$Jb, _$_M, _$nm) {
        _$_M = _$_M || 0;
        if (_$nm === _$W3)
            _$nm = _$Jb.length;
        var _$6H = new _$el(_$tK[_$Jx[55]](_$Jb.length / 40960))
          , _$yA = _$nm - 40960
          , _$Iz = 0;
        while (_$_M < _$yA) {
            _$6H[_$Iz++] = _$nR[_$Jx[32]](null, _$Jb[_$Jx[1]](_$_M, _$_M += 40960));
        }
        if (_$_M < _$nm)
            _$6H[_$Iz++] = _$nR[_$Jx[32]](null, _$Jb[_$Jx[1]](_$_M, _$nm));
        return _$6H.join('');
    }



    function _$l6(_$Jb) {
        var _$6H, _$yA = 0, _$Iz;
        _$Jb = _$lz(_$Jb);
        _$Iz = _$Jb.length;
        _$6H = new _$el(_$Iz);
        _$Iz -= 3;
        while (_$yA < _$Iz) {
            _$6H[_$yA] = _$K9[_$Jx[0]](_$Jb, _$yA++);
            _$6H[_$yA] = _$K9[_$Jx[0]](_$Jb, _$yA++);
            _$6H[_$yA] = _$K9[_$Jx[0]](_$Jb, _$yA++);
            _$6H[_$yA] = _$K9[_$Jx[0]](_$Jb, _$yA++);
        }
        _$Iz += 3;
        while (_$yA < _$Iz)
            _$6H[_$yA] = _$K9[_$Jx[0]](_$Jb, _$yA++);
        return _$6H;
    }
    function _$70(_$Jb, _$_M) {
        if (typeof _$Jb === _$Jx[6])
            _$Jb = _$l6(_$Jb);
        _$_M = _$_M || _$uu;
        var _$6H, _$yA = _$QJ = 0, _$Iz = _$Jb.length, _$ML, _$9M;
        _$6H = new _$el(_$tK[_$Jx[55]](_$Iz * 4 / 3));
        _$Iz = _$Jb.length - 2;
        while (_$yA < _$Iz) {
            _$ML = _$Jb[_$yA++];
            _$6H[_$QJ++] = _$_M[_$ML >> 2];
            _$9M = _$Jb[_$yA++];
            _$6H[_$QJ++] = _$_M[((_$ML & 3) << 4) | (_$9M >> 4)];
            _$ML = _$Jb[_$yA++];
            _$6H[_$QJ++] = _$_M[((_$9M & 15) << 2) | (_$ML >> 6)];
            _$6H[_$QJ++] = _$_M[_$ML & 63];
        }
        if (_$yA < _$Jb.length) {
            _$ML = _$Jb[_$yA];
            _$6H[_$QJ++] = _$_M[_$ML >> 2];
            _$9M = _$Jb[++_$yA];
            _$6H[_$QJ++] = _$_M[((_$ML & 3) << 4) | (_$9M >> 4)];
            if (_$9M !== _$W3) {
                _$6H[_$QJ++] = _$_M[(_$9M & 15) << 2];
            }
        }
        return _$6H.join('');
    }


    function _$W9(_$Jb) {
        var _$6H = _$Jb.length;
        var _$yA, _$Iz = new Array(_$6H - 1), _$ML = _$Jb.charCodeAt(0) - 97;
        for (var _$9M = 0, _$b2 = 1; _$b2 < _$6H; ++_$b2) {
            _$yA = _$Jb.charCodeAt(_$b2);
            if (_$yA >= 40 && _$yA < 92) {
                _$yA += _$ML;
                if (_$yA >= 92)
                    _$yA = _$yA - 52;
            } else if (_$yA >= 97 && _$yA < 127) {
                _$yA += _$ML;
                if (_$yA >= 127)
                    _$yA = _$yA - 30;
            }
            _$Iz[_$9M++] = _$yA;
        }
        return _$nR.apply(null, _$Iz);
    }

    function _$6t(_$s6, _$DS) {
        if (_$DS === _$Sj || _$DS)
            _$W_ |= _$s6;
    }
    function _$Tg(_$s6) {
        var _$K5 = _$MF.Math[_$k1[55]](_$MF.Math[_$k1[550]]() * 256);
        _$s6 = _$s6[_$k1[8]](_$jn(_$3n()));
        for (var _$k9 = 0; _$k9 < _$s6.length; _$k9++) {
            _$s6[_$k9] ^= _$K5;
        }
        _$s6[_$k9] = _$K5;
        return _$s6;
    }
    function _$jn(_$s6) {
        return [(_$s6 >>> 24) & 0xFF, (_$s6 >>> 16) & 0xFF, (_$s6 >>> 8) & 0xFF, _$s6 & 0xFF];
    }


    function _$9t(_$s6) {
        var _$K5 = _$s6[_$k1[1]](0);
        if (_$K5.length < 5) {
            return;
        }
        var _$k9 = _$K5.pop();
        var _$Eo = 0
          , _$Ye = _$K5.length;
        while (_$Eo < _$Ye) {
            _$K5[_$Eo++] ^= _$k9;
        }
        var _$td = _$K5.length - 4;
        var _$fI = _$3n() - _$rH(_$K5[_$k1[1]](_$td))[0];
        _$K5 = _$K5[_$k1[1]](0, _$td);
        var _$b8 = _$MF.Math[_$k1[5]](_$MF[_$k1[78]].log(_$fI / 1.164 + 1));
        var _$E3 = _$K5.length;
        var _$sZ = [0, _$rL._$S1][_$U$];
        _$Eo = 0;
        while (_$Eo < _$E3) {
            _$K5[_$Eo] = _$b8 | (_$K5[_$Eo++] ^ _$sZ);
        }
        _$yk(8, _$b8);
        return _$K5;
    }


    function _$5J(_$cK) {
        var _$fz = _$cK.length;
        var _$xA, _$F1 = new Array(_$fz - 1), _$vR = _$cK.charCodeAt(0) - 97;
        for (var _$Li = 0, _$cU = 1; _$cU < _$fz; ++_$cU) {
            _$xA = _$cK.charCodeAt(_$cU);
            if (_$xA >= 40 && _$xA < 92) {
                _$xA += _$vR;
                if (_$xA >= 92)
                    _$xA = _$xA - 52;
            } else if (_$xA >= 97 && _$xA < 127) {
                _$xA += _$vR;
                if (_$xA >= 127)
                    _$xA = _$xA - 30;
            }
            _$F1[_$Li++] = _$xA;
        }
        return _$hT.apply(null, _$F1);
    }


    function _$TM() {
        var _$fz = [];
        for (var _$xA = 0; _$xA < 256; ++_$xA) {
            var _$F1 = _$xA;
            for (var _$vR = 0; _$vR < 8; ++_$vR) {
                if ((_$F1 & 0x80) !== 0)
                    _$F1 = (_$F1 << 1) ^ 7;
                else
                    _$F1 <<= 1;
            }
            _$fz[_$xA] = _$F1 & 0xff;
        }
        return _$fz;
'''

import re
RETURN = True # 是否存在换行处理
s = re.sub(r'(\n *)function', r'\1def', s)
for _ in range(10): s = re.sub(r'(\n *\}\n)', r'\n', s)
s = re.sub(r'(\n *\}\n)', r'\n', s)
s = re.sub(r'(\n *)\} *([^\n]+\n)', r'\1\2', s)
s = re.sub(r' *\{ *\n', r':\n', s)
s = re.sub(r'(\n *)(if *\([^\(\)]+\)) *([^\n\{:]+\n)', r'\1\2:\1    \3', s)   

# 这里考虑处理简单的for循环条件的置换处理,不过这里有很大的变数要处理，后续再搞
def deal_for(e):
    g = e.group(1)
    a,b,c = e.group(2),e.group(3),e.group(4)
    v = g + a.strip() + g + 'while ({}):'.format(b.strip()) + '  [{}]'.format(c.strip())
    return v
s = re.sub(r'(\n *)for *\(([^;]*);([^;]*);([^;]*)\):', deal_for, s)
def deal_while_1(s):
    q = []
    g = None
    k = None
    t = 0
    for i in s.splitlines():
        if t == 1:
            v = re.findall(r'^( *)', i)[0]
            if i.strip() != '':
                if g is None:
                    g = len(v)
                else:
                    if len(v) < g:
                        q.append(' '*g + k)
                        t = 2
        else:
            v = re.findall(r'^( *)(while[^\n]+)\[([^\n]+)\] *$', i)
            if v:
                i = (v[0][0] + v[0][1]).rstrip()
                k = v[0][2].strip()
                t = 1
        q.append(i)
    q = '\n'.join(q)
    if re.findall(r'while[^\n]+\[([^\n]+)\]', q):
        return deal_while_1(q)
    else:
        return q
s = deal_while_1(s)
# 处理自增应该在处理循环之后
s = re.sub(r'(\n *)([^\n]*?)([a-zA-Z0-9_$]+)( *\+\+)([^\n]*)', r'\1\2\3\5; \3 += 1', s)
s = re.sub(r'(\n *)([^\n]*?)(\+\+ *)([a-zA-Z0-9_$]+)([^\n]*)', r'\1\4 += 1;\2\4\5', s)

def deal_if_1(e):
    if e.group(2).strip().endswith(':'):
        return e.group(0)
    else:
        return e.group(1) + e.group(2) + ':'

s = re.sub(r'(\n *)(if *\([^\n]*\))', deal_if_1, s)   
s = re.sub(r'(\n *)else if', r'\1elif', s)
s = re.sub(r'(\n *)else *', r'\1else:', s)
s = re.sub(r'(\n *)var ', r'\1', s)
s = re.sub(r'; *;', r';', s)
s = re.sub(r': *:', r':', s)
s = re.sub(r'<<<', r'<<', s)
s = re.sub(r'>>>', r'>>', s)
s = re.sub(r'!==', r'!=', s)




# 这里考虑处理赋值的对齐,不过现在还是有点问题
# s = re.sub(r'(\n *)([^\n=]+=[^\n=]+), *', r'\1\2', s)


s = re.sub(r'_\$([a-zA-Z0-9_]{2})', r'_\1', s)    # 文书相关的处理
s = re.sub(r'; *\n', r'\n', s)                    # 去除尾部分号(非必要)
print(s)





