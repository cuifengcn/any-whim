# -*- coding: utf-8 -*-

# 完全依赖 js2py
# 开发于 python3
# 直接执行脚本即可测试
# 需要依赖安装 node(需要有npm) 的环境，用以下载 escodegen.js 的文件，只会下载一次。

# 通过生成语法树，快速修改内部的某些混肴处理，从而简化代码
# 直接使用 js2py 非常方便，因为其内部已经自带了一些 js 库的 python 化代码
# 使用其中的 escodegen 模块就可以重新将语法树重构成代码。代码如下。
# 这里用的是某个时期的文书网的 sojson 代码块，目前来看，貌似解码效果还行。
# 纯粹个人兴趣写的，所以代码写得过于粗暴，以后有机会再改进。

script = r'''
var encode_version = 'sojson.v5',
    qxpgb = '__0x31a2a',
    __0x31a2a = ['dhvCugsb', 'c8OqwoYrQQ==', 'AMO/woHCnUnDhigI', 'w7hubn3DisOcT8OiSsO8w4BUwo4=', 'wovDuVLDtcKQ', 'w5vDgHzCnw==', 'RCVufcKFwqPCo0TCsT7DrA==', 'ccKsw7HDtA==', 'w7fCg0rCt8KkBcOjwpLDhG7CkA==', 'M8KyRS/ClQ==', 'b8KAYMK7w50=', 'w7rDuxrCjiNXCQ==', 'TSvCoi4F', 'AcOcwojDvk7Cn8O4dQ==', 'H8OYcAc1', 'w6bCv2nCnsKT', 'w6rDm8OnwozCgw==', 'cgrCsg==', 'woNKTxvDssO4Yj4=', 'wq/Cp8KYwrjCrcKISMKpfsO7', '5Lq46IGc5Yix6ZqeLlfDgcKIwpDCt21fwpY=', 'cCwfKXMtXsKgWA==', 'w5EuwrfDuG5Twrwgcw==', 'wpvDmUrDm8KR', 'w6vDjsOGwoLCmQ==', 'w6XCjkDCosKe', 'B8O+SMOwHg==', 'wr8Uw6hOBzs=', 'wpvDoV/DrsKnGsK4amTDqQ==', 'wpvDoV/DrsKlAQ==', 'w6fDqiTChyU=', 'w4NEOsKtRQ==', 'eW3CvMOYTA==', 'f8KceMKlw7sXw45iFTo=', 'w7g7ZMOGw4hh', 'w5kXVcOdw4A=', 'wposMMK6wowz', 'w5cnUcOnw7w=', 'w5fDksOsw5A1', 'w5sVwojDgkM=', 'woHCl8Kww5TDhgY=', 'wrIww7NWAw==', 'bsO4wqUZQg==', 'w5jDiVgmJsKg', 'w7vDgMO8w5Vpw4k=', 'a8Odw6bCt8ODaSHDiWgHAw==', 'w4IBacOcw6c=', 'ScKTJQF2', 'ZVjCusOm', 'Z8KzMA==', 'w4YzK8K/wr4kw78Dw6sNKz/Dn8KKLw==', 'w6fDisOhw4Y=', 'YAY+AFg=', 'w4/ComPCosKQ', 'JjXDhsOnGcKr', 'w4HCk0bCuMK6Ng==', 'DsOBXcORFsKt', 'w7U5wqXDqlY=', 'GsOkwpbCusK3', 'wpEfw7s=', 'w57ChFjClcKv', 'ejXCihcR', 'TRNXfcK5', 'w4oHwpTDrlM=', 'w4/DnBYIw5w='];
(function(_0x231fd0, _0x4f680a) {
    var _0x5b4826 = function(_0x4a3682) {
        while (--_0x4a3682) {
            _0x231fd0['push'](_0x231fd0['shift']());
        }
    };
    var _0x18d5c9 = function() {
        var _0x4ce2f1 = {
            'data': {
                'key': 'cookie',
                'value': 'timeout'
            },
            'setCookie': function(_0x333808, _0x432180, _0x2ab90b, _0x991246) {
                _0x991246 = _0x991246 || {};
                var _0x981158 = _0x432180 + '=' + _0x2ab90b;
                var _0x57b080 = 0x0;
                for (var _0x57b080 = 0x0, _0x441e3a = _0x333808['length']; _0x57b080 < _0x441e3a; _0x57b080++) {
                    var _0x2cc193 = _0x333808[_0x57b080];
                    _0x981158 += ';\x20' + _0x2cc193;
                    var _0x5f41ea = _0x333808[_0x2cc193];
                    _0x333808['push'](_0x5f41ea);
                    _0x441e3a = _0x333808['length'];
                    if (_0x5f41ea !== !![]) {
                        _0x981158 += '=' + _0x5f41ea;
                    }
                }
                _0x991246['cookie'] = _0x981158;
            },
            'removeCookie': function() {
                return 'dev';
            },
            'getCookie': function(_0x503809, _0xe42b77) {
                _0x503809 = _0x503809 || function(_0x56465b) {
                    return _0x56465b;
                };
                var _0x52cace = _0x503809(new RegExp('(?:^|;\x20)' + _0xe42b77['replace'](/([.$?*|{}()[]\/+^])/g, '$1') + '=([^;]*)'));
                var _0x39753a = function(_0xf81284, _0x307b3e) {
                    _0xf81284(++_0x307b3e);
                };
                _0x39753a(_0x5b4826, _0x4f680a);
                return _0x52cace ? decodeURIComponent(_0x52cace[0x1]) : undefined;
            }
        };
        var _0x3ab53f = function() {
            var _0xfeb75b = new RegExp('\x5cw+\x20*\x5c(\x5c)\x20*{\x5cw+\x20*[\x27|\x22].+[\x27|\x22];?\x20*}');
            return _0xfeb75b['test'](_0x4ce2f1['removeCookie']['toString']());
        };
        _0x4ce2f1['updateCookie'] = _0x3ab53f;
        var _0xbd1168 = '';
        var _0x4a4c56 = _0x4ce2f1['updateCookie']();
        if (!_0x4a4c56) {
            _0x4ce2f1['setCookie'](['*'], 'counter', 0x1);
        } else if (_0x4a4c56) {
            _0xbd1168 = _0x4ce2f1['getCookie'](null, 'counter');
        } else {
            _0x4ce2f1['removeCookie']();
        }
    };
    _0x18d5c9();
}(__0x31a2a, 0x1dc));
var _0x213d = function(_0xe8191e, _0x5b709c) {
    _0xe8191e = _0xe8191e - 0x0;
    var _0x32912a = __0x31a2a[_0xe8191e];
    if (_0x213d['initialized'] === undefined) {
        (function() {
            var _0x49d973 = typeof window !== 'undefined' ? window : typeof process === 'object' && typeof require === 'function' && typeof global === 'object' ? global : this;
            var _0x3e050f = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
            _0x49d973['atob'] || (_0x49d973['atob'] = function(_0x15378c) {
                var _0x4a714d = String(_0x15378c)['replace'](/=+$/, '');
                for (var _0x46149c = 0x0, _0xf1b84f, _0xe5f135, _0x36914d = 0x0, _0x2a8f2b = ''; _0xe5f135 = _0x4a714d['charAt'](_0x36914d++); ~_0xe5f135 && (_0xf1b84f = _0x46149c % 0x4 ? _0xf1b84f * 0x40 + _0xe5f135 : _0xe5f135, _0x46149c++ % 0x4) ? _0x2a8f2b += String['fromCharCode'](0xff & _0xf1b84f >> (-0x2 * _0x46149c & 0x6)) : 0x0) {
                    _0xe5f135 = _0x3e050f['indexOf'](_0xe5f135);
                }
                return _0x2a8f2b;
            });
        }());
        var _0xc94208 = function(_0xbf7cb5, _0x14538c) {
            var _0x4b4e10 = [],
                _0x4f827e = 0x0,
                _0x121b41, _0x3198c7 = '',
                _0x390bec = '';
            _0xbf7cb5 = atob(_0xbf7cb5);
            for (var _0x80d343 = 0x0, _0x3b356f = _0xbf7cb5['length']; _0x80d343 < _0x3b356f; _0x80d343++) {
                _0x390bec += '%' + ('00' + _0xbf7cb5['charCodeAt'](_0x80d343)['toString'](0x10))['slice'](-0x2);
            }
            _0xbf7cb5 = decodeURIComponent(_0x390bec);
            for (var _0x2ed4db = 0x0; _0x2ed4db < 0x100; _0x2ed4db++) {
                _0x4b4e10[_0x2ed4db] = _0x2ed4db;
            }
            for (_0x2ed4db = 0x0; _0x2ed4db < 0x100; _0x2ed4db++) {
                _0x4f827e = (_0x4f827e + _0x4b4e10[_0x2ed4db] + _0x14538c['charCodeAt'](_0x2ed4db % _0x14538c['length'])) % 0x100;
                _0x121b41 = _0x4b4e10[_0x2ed4db];
                _0x4b4e10[_0x2ed4db] = _0x4b4e10[_0x4f827e];
                _0x4b4e10[_0x4f827e] = _0x121b41;
            }
            _0x2ed4db = 0x0;
            _0x4f827e = 0x0;
            for (var _0xfae646 = 0x0; _0xfae646 < _0xbf7cb5['length']; _0xfae646++) {
                _0x2ed4db = (_0x2ed4db + 0x1) % 0x100;
                _0x4f827e = (_0x4f827e + _0x4b4e10[_0x2ed4db]) % 0x100;
                _0x121b41 = _0x4b4e10[_0x2ed4db];
                _0x4b4e10[_0x2ed4db] = _0x4b4e10[_0x4f827e];
                _0x4b4e10[_0x4f827e] = _0x121b41;
                _0x3198c7 += String['fromCharCode'](_0xbf7cb5['charCodeAt'](_0xfae646) ^ _0x4b4e10[(_0x4b4e10[_0x2ed4db] + _0x4b4e10[_0x4f827e]) % 0x100]);
            }
            return _0x3198c7;
        };
        _0x213d['rc4'] = _0xc94208;
        _0x213d['data'] = {};
        _0x213d['initialized'] = !![];
    }
    var _0x253d5a = _0x213d['data'][_0xe8191e];
    if (_0x253d5a === undefined) {
        if (_0x213d['once'] === undefined) {
            var _0xe2055f = function(_0xac42b6) {
                this['rc4Bytes'] = _0xac42b6;
                this['states'] = [0x1, 0x0, 0x0];
                this['newState'] = function() {
                    return 'newState';
                };
                this['firstState'] = '\x5cw+\x20*\x5c(\x5c)\x20*{\x5cw+\x20*';
                this['secondState'] = '[\x27|\x22].+[\x27|\x22];?\x20*}';
            };
            _0xe2055f['prototype']['checkState'] = function() {
                var _0x3d707c = new RegExp(this['firstState'] + this['secondState']);
                return this['runState'](_0x3d707c['test'](this['newState']['toString']()) ? --this['states'][0x1] : --this['states'][0x0]);
            };
            _0xe2055f['prototype']['runState'] = function(_0x3ebbf7) {
                if (!Boolean(~_0x3ebbf7)) {
                    return _0x3ebbf7;
                }
                return this['getState'](this['rc4Bytes']);
            };
            _0xe2055f['prototype']['getState'] = function(_0x57b0a7) {
                for (var _0x88219d = 0x0, _0x330957 = this['states']['length']; _0x88219d < _0x330957; _0x88219d++) {
                    this['states']['push'](Math['round'](Math['random']()));
                    _0x330957 = this['states']['length'];
                }
                return _0x57b0a7(this['states'][0x0]);
            };
            new _0xe2055f(_0x213d)['checkState']();
            _0x213d['once'] = !![];
        }
        _0x32912a = _0x213d['rc4'](_0x32912a, _0x5b709c);
        _0x213d['data'][_0xe8191e] = _0x32912a;
    } else {
        _0x32912a = _0x253d5a;
    }
    return _0x32912a;
};
if (typeof encode_version !== _0x213d('0x0', 'XkR5') && encode_version === _0x213d('0x1', '!]@N')) {
    function _0x553680(_0x32d249) {
        var _0x1c847c = {
            'cPtGu': '0|7|3|4|5|6|2|1',
            'aVkgN': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=',
            'WhdwM': function _0x2029b6(_0x484c89, _0x2e22a4) {
                return _0x484c89 < _0x2e22a4;
            },
            'zZtSk': function _0x4b483e(_0x225021, _0x5322d4) {
                return _0x225021 & _0x5322d4;
            },
            'yxMyj': function _0x6d0532(_0x310c89, _0x2a03ba) {
                return _0x310c89 << _0x2a03ba;
            },
            'BDPiI': function _0x304a66(_0x3ff9d0, _0x3c82e9) {
                return _0x3ff9d0 >> _0x3c82e9;
            },
            'LtTSu': function _0x48419d(_0x286b15, _0x960eb) {
                return _0x286b15 | _0x960eb;
            },
            'yTUIB': function _0x2782eb(_0x5338f7, _0x3bb613) {
                return _0x5338f7 & _0x3bb613;
            },
            'VhjDq': function _0x3e7647(_0x161d3c, _0x4c997b) {
                return _0x161d3c | _0x4c997b;
            },
            'nLzjE': function _0x23c4f3(_0x33ac1f, _0x5ca1f7) {
                return _0x33ac1f & _0x5ca1f7;
            },
            'iddHe': function _0x17025a(_0x818a42, _0x44b28e) {
                return _0x818a42 & _0x44b28e;
            }
        };
        var _0x1da315 = _0x1c847c[_0x213d('0x2', 'DE2z')][_0x213d('0x3', 'Z@gv')]('|'),
            _0x15b147 = 0x0;
        while (!![]) {
            switch (_0x1da315[_0x15b147++]) {
                case '0':
                    var _0x177543 = _0x1c847c['aVkgN'];
                    continue;
                case '1':
                    return _0x112513;
                case '2':
                    while (_0x1c847c[_0x213d('0x4', 'dP^[')](_0x24ff86, _0x23d27d)) {
                        _0x73b9cc = _0x1c847c[_0x213d('0x5', 'yNIT')](_0x32d249['charCodeAt'](_0x24ff86++), 0xff);
                        if (_0x24ff86 == _0x23d27d) {
                            _0x112513 += _0x177543['charAt'](_0x73b9cc >> 0x2);
                            _0x112513 += _0x177543[_0x213d('0x6', 'cLs0')]((_0x73b9cc & 0x3) << 0x4);
                            _0x112513 += '==';
                            break;
                        }
                        _0x4190cc = _0x32d249[_0x213d('0x7', 'DE2z')](_0x24ff86++);
                        if (_0x24ff86 == _0x23d27d) {
                            _0x112513 += _0x177543['charAt'](_0x73b9cc >> 0x2);
                            _0x112513 += _0x177543[_0x213d('0x8', 'DE2z')](_0x1c847c[_0x213d('0x9', '5KjR')](_0x73b9cc & 0x3, 0x4) | _0x1c847c['BDPiI'](_0x1c847c[_0x213d('0xa', 'T5XA')](_0x4190cc, 0xf0), 0x4));
                            _0x112513 += _0x177543['charAt'](_0x1c847c[_0x213d('0xb', '&c)N')](_0x4190cc, 0xf) << 0x2);
                            _0x112513 += '=';
                            break;
                        }
                        _0x2c7076 = _0x32d249[_0x213d('0xc', '!#1F')](_0x24ff86++);
                        _0x112513 += _0x177543[_0x213d('0xd', 'i2Wk')](_0x1c847c[_0x213d('0xe', 'i2Wk')](_0x73b9cc, 0x2));
                        _0x112513 += _0x177543[_0x213d('0xf', 'WRpw')](_0x1c847c[_0x213d('0x10', 'i2Wk')](_0x1c847c[_0x213d('0x11', 'GSaA')](_0x73b9cc, 0x3) << 0x4, _0x1c847c[_0x213d('0x12', '!]@N')](_0x4190cc, 0xf0) >> 0x4));
                        _0x112513 += _0x177543[_0x213d('0x13', 'nh*[')](_0x1c847c['VhjDq'](_0x1c847c['yxMyj'](_0x1c847c[_0x213d('0x14', 'cLs0')](_0x4190cc, 0xf), 0x2), _0x1c847c[_0x213d('0x15', '7l7L')](_0x2c7076, 0xc0) >> 0x6));
                        _0x112513 += _0x177543[_0x213d('0x16', 'Qau5')](_0x2c7076 & 0x3f);
                    }
                    continue;
                case '3':
                    var _0x73b9cc, _0x4190cc, _0x2c7076;
                    continue;
                case '4':
                    _0x23d27d = _0x32d249[_0x213d('0x17', 'o)%3')];
                    continue;
                case '5':
                    _0x24ff86 = 0x0;
                    continue;
                case '6':
                    _0x112513 = '';
                    continue;
                case '7':
                    var _0x112513, _0x24ff86, _0x23d27d;
                    continue;
            }
            break;
        }
    }

    function _0x5221bc() {
        var _0x434d12 = {
            'YRlhn': _0x213d('0x18', '(Y3$'),
            'BQzMZ': function _0x2407d1(_0x2aed36, _0x448ece) {
                return _0x2aed36 < _0x448ece;
            },
            'nxjDT': function _0x1d5251(_0x22a0b4, _0x494b97) {
                return _0x22a0b4 + _0x494b97;
            },
            'csKNI': 'WZWS_CONFIRM_PREFIX_LABEL'
        };
        var _0x1881a1 = _0x434d12[_0x213d('0x19', 'i2Wk')]['split']('|'),
            _0x386713 = 0x0;
        while (!![]) {
            switch (_0x1881a1[_0x386713++]) {
                case '0':
                    for (_0x710a7 = 0x0; _0x434d12[_0x213d('0x1a', 'x&tC')](_0x710a7, wzwsquestion['length']); _0x710a7++) {
                        _0x4de8cc += wzwsquestion['charCodeAt'](_0x710a7);
                    }
                    continue;
                case '1':
                    _0x4de8cc *= wzwsfactor;
                    continue;
                case '2':
                    var _0x4de8cc = 0x0;
                    continue;
                case '3':
                    _0x4de8cc += 0x1b207;
                    continue;
                case '4':
                    var _0x710a7 = 0x0;
                    continue;
                case '5':
                    return _0x434d12['nxjDT'](_0x434d12['csKNI'], _0x4de8cc);
            }
            break;
        }
    }

    function _0x3b5c6a(_0x1dd18a, _0x3a861f) {
        var _0x25fab3 = {
            'eDELM': '0|1|5|7|3|4|2|6',
            'YQYpZ': _0x213d('0x1b', '&c)N'),
            'Fxxhk': function _0x2437c8(_0x292d56, _0x42c325) {
                return _0x292d56 != _0x42c325;
            },
            'WxxaW': function _0x207b2d(_0x438adc, _0x263f95) {
                return _0x438adc < _0x263f95;
            },
            'CEDqD': function _0x56b710(_0x177835, _0x214522) {
                return _0x177835 !== _0x214522;
            },
            'pKuTQ': _0x213d('0x1c', 'x&tC'),
            'HwbGe': function _0x1bdf9e(_0x3baa96) {
                return _0x3baa96();
            },
            'yvILb': function _0x58097e(_0x282f40, _0x32384a) {
                return _0x282f40(_0x32384a);
            },
            'hFIeR': function _0x40fe55(_0x336474, _0x2adcd0) {
                return _0x336474 + _0x2adcd0;
            },
            'MYAlY': _0x213d('0x1d', 'WRpw'),
            'dnJUw': function _0x4b56f3(_0x1c1f2a, _0x536528) {
                return _0x1c1f2a == _0x536528;
            },
            'uXyPh': _0x213d('0x1e', 'o)%3'),
            'tvGzf': function _0x158de7(_0x469c35, _0xdf78fa, _0xae209f) {
                return _0x469c35(_0xdf78fa, _0xae209f);
            }
        };
        var _0x5dfc86 = _0x25fab3[_0x213d('0x1f', 'XkR5')]['split']('|'),
            _0x2af038 = 0x0;
        while (!![]) {
            switch (_0x5dfc86[_0x2af038++]) {
                case '0':
                    var _0x4dd19b = document['createElement'](_0x25fab3[_0x213d('0x20', 'VFJZ')]);
                    continue;
                case '1':
                    _0x4dd19b[_0x213d('0x21', '%1j1')] = _0x1dd18a;
                    continue;
                case '2':
                    _0x4dd19b[_0x213d('0x22', 'dP^[')]();
                    continue;
                case '3':
                    if (_0x25fab3['Fxxhk'](_0x3a861f[_0x213d('0x23', 'yNIT')]('='), -0x1)) {
                        var _0x554240 = _0x3a861f['split']('&');
                        for (var _0x3ee145 = 0x0; _0x25fab3[_0x213d('0x24', '!]@N')](_0x3ee145, _0x554240['length']); _0x3ee145++) {
                            if (_0x25fab3[_0x213d('0x25', '(Y3$')](_0x25fab3['pKuTQ'], _0x213d('0x26', '(M6F'))) {
                                var _0x55bbef = _0x25fab3[_0x213d('0x27', 'VFJZ')](_0x5221bc);
                                var _0x58ba9d = _0x25fab3[_0x213d('0x28', '#eYs')](_0x553680, _0x55bbef['toString']());
                                var _0x3ddd13 = _0x25fab3[_0x213d('0x29', '9382')](_0x25fab3[_0x213d('0x2a', '!]@N')](dynamicurl, _0x25fab3['MYAlY']), _0x58ba9d);
                                if (_0x25fab3[_0x213d('0x2b', 'aky8')](wzwsmethod, _0x25fab3[_0x213d('0x2c', '#eYs')])) {
                                    _0x25fab3[_0x213d('0x2d', '7l7L')](_0x3b5c6a, _0x3ddd13, _0x3a861f);
                                } else {
                                    window[_0x213d('0x2e', '!QBG')] = _0x3ddd13;
                                }
                            } else {
                                var _0x2b6cfa = document[_0x213d('0x2f', 'BJN7')]('textarea');
                                var _0x3d8aa1 = _0x554240[_0x3ee145];
                                var _0x258367 = _0x3d8aa1[_0x213d('0x30', 'DE2z')]('=');
                                _0x2b6cfa[_0x213d('0x31', '41Yz')] = _0x258367[0x0];
                                _0x2b6cfa['value'] = _0x258367[0x1];
                                _0x4dd19b[_0x213d('0x32', '9382')](_0x2b6cfa);
                            }
                        }
                    }
                    continue;
                case '4':
                    document[_0x213d('0x33', 'jq9O')][_0x213d('0x34', 'VFJZ')](_0x4dd19b);
                    continue;
                case '5':
                    _0x4dd19b['method'] = _0x25fab3[_0x213d('0x35', 'yZ6K')];
                    continue;
                case '6':
                    return _0x4dd19b;
                case '7':
                    _0x4dd19b[_0x213d('0x36', '!#1F')][_0x213d('0x37', '5KjR')] = 'none';
                    continue;
            }
            break;
        }
    }

    function _0xd1b242() {
        var _0x1acce7 = function() {
            var _0x6488f9 = !![];
            return function(_0x3bbd97, _0x5627c2) {
                var _0x523fa8 = _0x6488f9 ? function() {
                    if (_0x5627c2) {
                        var _0x4760bb = _0x5627c2['apply'](_0x3bbd97, arguments);
                        _0x5627c2 = null;
                        return _0x4760bb;
                    }
                } : function() {};
                _0x6488f9 = ![];
                return _0x523fa8;
            };
        }();
        var _0x2e3aa7 = _0x1acce7(this, function() {
            var _0x577165 = function() {
                    return '\x64\x65\x76';
                },
                _0x4c97b9 = function() {
                    return '\x77\x69\x6e\x64\x6f\x77';
                };
            var _0x1f9cea = function() {
                var _0x154e1f = new RegExp('\x5c\x77\x2b\x20\x2a\x5c\x28\x5c\x29\x20\x2a\x7b\x5c\x77\x2b\x20\x2a\x5b\x27\x7c\x22\x5d\x2e\x2b\x5b\x27\x7c\x22\x5d\x3b\x3f\x20\x2a\x7d');
                return !_0x154e1f['\x74\x65\x73\x74'](_0x577165['\x74\x6f\x53\x74\x72\x69\x6e\x67']());
            };
            var _0x278471 = function() {
                var _0x137a46 = new RegExp('\x28\x5c\x5c\x5b\x78\x7c\x75\x5d\x28\x5c\x77\x29\x7b\x32\x2c\x34\x7d\x29\x2b');
                return _0x137a46['\x74\x65\x73\x74'](_0x4c97b9['\x74\x6f\x53\x74\x72\x69\x6e\x67']());
            };
            var _0x5ac1b3 = function(_0x25c7a2) {
                var _0x58da58 = ~-0x1 >> 0x1 + 0xff % 0x0;
                if (_0x25c7a2['\x69\x6e\x64\x65\x78\x4f\x66']('\x69' === _0x58da58)) {
                    _0x1a1ca1(_0x25c7a2);
                }
            };
            var _0x1a1ca1 = function(_0x36a02a) {
                var _0x302e37 = ~-0x4 >> 0x1 + 0xff % 0x0;
                if (_0x36a02a['\x69\x6e\x64\x65\x78\x4f\x66']((!![] + '')[0x3]) !== _0x302e37) {
                    _0x5ac1b3(_0x36a02a);
                }
            };
            if (!_0x1f9cea()) {
                if (!_0x278471()) {
                    _0x5ac1b3('\x69\x6e\x64\u0435\x78\x4f\x66');
                } else {
                    _0x5ac1b3('\x69\x6e\x64\x65\x78\x4f\x66');
                }
            } else {
                _0x5ac1b3('\x69\x6e\x64\u0435\x78\x4f\x66');
            }
        });
        _0x2e3aa7();
        var _0x358b35 = {
            'Nhauv': function _0x5d1188(_0x3351bf, _0x3aabb7) {
                return _0x3351bf(_0x3aabb7);
            },
            'hZZjg': function _0x37d045(_0xa6bd2e, _0x40e6c3) {
                return _0xa6bd2e + _0x40e6c3;
            },
            'gqmoA': '?wzwschallenge=',
            'DRDzI': 'post',
            'pLSLY': function _0xe34b61(_0xa24fd2, _0x555c76, _0xfd859) {
                return _0xa24fd2(_0x555c76, _0xfd859);
            },
            'reMgn': function _0x1152c8(_0x3c545f, _0xf3ec93) {
                return _0x3c545f !== _0xf3ec93;
            }
        };
        var _0x23c204 = _0x5221bc();
        var _0x21ccbd = _0x358b35[_0x213d('0x38', '#eYs')](_0x553680, _0x23c204[_0x213d('0x39', 'eymL')]());
        var _0xcd071f = _0x358b35[_0x213d('0x3a', 'xtNn')](dynamicurl + _0x358b35['gqmoA'], _0x21ccbd);
        if (wzwsmethod == _0x358b35['DRDzI']) {
            _0x358b35[_0x213d('0x3b', 'VFJZ')](_0x3b5c6a, _0xcd071f, wzwsparams);
        } else {
            if (_0x358b35[_0x213d('0x3c', 'Z@gv')](_0x213d('0x3d', '#eYs'), 'eOa')) {
                window[_0x213d('0x3e', 'NS17')] = _0xcd071f;
            } else {
                hash += wzwsquestion[_0x213d('0x3f', 'WXxL')](i);
            }
        }
    }
    _0xd1b242();
} else {
    alert(_0x213d('0x40', '41Yz'));
};
encode_version = 'sojson.v5';

'''































import re
import base64
class SojsonRc4:
    def __init__(self, str_list, num):
        self.init_str = str_list
        self.init_num = num
        self.init_str = self.init_str[self.init_num%len(self.init_str):] + self.init_str[:self.init_num%len(self.init_str)]
    def _rc4(self, data, key):
        S, j, key = list(range(256)), 0, key.encode()
        for i in range(256):
            j = (j + S[i] + key[i%len(key)]) % 256
            S[i], S[j] = S[j], S[i]
        i, j = 0, 0
        R = []
        for c in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            t = c ^ (S[(S[i] + S[j]) % 256])
            R.append(t)
        return R
    def rc4(self, data, key):
        data = [ord(i) if ord(i) < 256 else int(i.encode('unicode_escape')[2:], 16) for i in base64.b64decode(data).decode()]
        R = self._rc4(data, key)
        return ''.join([chr(i) if i < 256 else (b'\\u' + hex(i)[2:].encode()).decode('unicode_escape') for i in R])
    def sojsonrc4(self, idxstr, key):
        ret = self.rc4(self.init_str[int(idxstr, 16)], key)
        return ret




import json, copy
import js2py
import pyjsparser
from js2py.pyjs import JS_BUILTINS

def convenience_tree_null(tree):
    if isinstance(tree, dict):
        cover_undefined_null(tree)
        for key in tree:
            if isinstance(tree[key], dict):
                convenience_tree_null(tree[key])
            elif isinstance(tree[key], list):
                for idx, _tree in enumerate(tree[key]):
                    convenience_tree_null(_tree)

def get_script_from_tree(tree):
    # 需要依赖安装 node 以及 npm 的环境
    # 用以下载 escodegen.js 的文件，只会下载一次。
    # 下载过后就会自动被js2py转成py代码，放在 js2py.py_node_modules 中。
    # 以下是解决 win10 上面下载时可能会出现的 bug，
    # 有时 powershell 才可以执行 有时 command 才可以执行，这么丑的写法，我也很绝望。
    try:
        escodegen = js2py.require('escodegen')
    except:
        import subprocess
        def _call(*a, **k):
            _a = list(a)
            _a[0] = 'powershell '+a[0]
            return _call_bak(*a, **k) if _call_bak(*_a, **k) != 0 else 0
        _call_bak = subprocess.call
        subprocess.call = _call
        escodegen = js2py.require('escodegen')
    return escodegen.generate(tree)

def cover_undefined_null(node):
    # 如果不使用 js2py 内部的数据结构来包装一下这类的数据，反编译回 js 代码时就会出现问题。
    if node.get('raw') == 'null' and node.get('value', '') is None:
        node['value'] = JS_BUILTINS['null']
    elif node.get('raw') == 'undefined' and node.get('value', '') is None:
        node['value'] = JS_BUILTINS['undefined']
    if node.get('raw', '') is None and node.get('value', '') is None:
        node.clear()
        node['type'] = 'Identifier'
        node['name'] = 'null'

def get_sojson_encoder(script):
    tree = pyjsparser.parse(script)
    encsname,encseles,encsnumb = None,None,None
    for idx, node in enumerate(tree['body']):
        if node['type'] == 'VariableDeclaration' and \
                        node.get('declarations'):
            for encs in node.get('declarations'):
                if encs.get('type') == 'VariableDeclarator' and encs.get('init').get('type') == 'ArrayExpression':
                    encsname = encs.get('id').get('name')
                    encseles = [i.get('value') for i in encs.get('init').get('elements')]
        if node['type'] == 'ExpressionStatement' and node['expression'].get('type') == 'CallExpression':
            encsnumb = node.get('expression').get('arguments')[1].get('value')
        if node['type'] == 'VariableDeclaration' and \
                        node.get('declarations') and \
                        node.get('declarations')[0].get('init') and \
                        node.get('declarations')[0].get('init').get('type') == 'FunctionExpression':
            break
    oldtree = tree['body'].copy()
    tree['body'] = oldtree[:idx+1]
    funcname = node.get('declarations')[0].get('id').get('name')
    use_my_rc4 = True
    if use_my_rc4:
        s = SojsonRc4(encseles, encsnumb)
        decoder = {}
        decoder[funcname] = s.sojsonrc4
    else:
        decoder = js2py.EvalJs()
        convenience_tree_null(tree)
        decoder.execute(get_script_from_tree(tree))
    tree['body'] = oldtree[idx+1:]
    return funcname, decoder, tree

def cover_func_rc4(node):
    if node.get('type') and node['type'] == 'CallExpression':
        args = node['arguments']
        if node['callee'].get('name') and node['callee']['name'] == funcname and args[0]['type'] == 'Literal' and args[1]['type'] == 'Literal':
            _args = args[0]['value'], args[1]['value']
            val = decoder_func(*_args)
            if val == None:
                val = JS_BUILTINS['null']
            print('执行算法解密部分：{}{}: {}'.format(funcname, _args, val))
            node = {
                "type": "Literal",
                "value": val,
                "raw": repr(val) # 这个参数实际上不会影响到js代码的重新生成
            }
            return node

def convenience_tree_rc4(tree):
    if isinstance(tree, dict):
        cover_undefined_null(tree)
        for key in tree:
            if isinstance(tree[key], dict):
                node = cover_func_rc4(tree[key])
                if node:
                    tree[key] = node
                else:
                    convenience_tree_rc4(tree[key])
            elif isinstance(tree[key], list):
                for idx, _tree in enumerate(tree[key]):
                    node = cover_func_rc4(tree[key][idx])
                    if node:
                        tree[key][idx] = node
                    else:
                        convenience_tree_rc4(_tree)


packer = []
def cover_func_remake(node, parent_body=None, curr_key=None, curr_idx=None):
    if node.get('type'):
        packer.append([node, parent_body, curr_key, curr_idx])
    else:
        print('notype =========================', node)

def convenience_tree_remake(tree, isstart=True):
    if isstart:
        packer.clear()
    if isinstance(tree, dict):
        cover_undefined_null(tree)
        for key in tree:
            if isinstance(tree[key], dict):
                node = cover_func_remake(tree[key], parent_body=tree, curr_key=key)
                if node:
                    tree[key] = node
                else:
                    convenience_tree_remake(tree[key], False)
            elif isinstance(tree[key], list):
                for idx, _tree in enumerate(tree[key]):
                    node = cover_func_remake(tree[key][idx], parent_body=tree, curr_key=key,curr_idx=idx)
                    if node:
                        tree[key][idx] = node
                    else:
                        convenience_tree_remake(_tree, False)

def remake_while_statement(node, parent_body, curr_key, curr_idx):
    try:
        if js2py.eval_js(get_script_from_tree(node['test'])) == True:
            inblocks = node['body']['body']
            if isinstance(inblocks, list) and inblocks:
                firstone = parent_body['body'][curr_idx-1]
                switchone = [i for i in inblocks if i['type'] == 'SwitchStatement']
                lastone = [i for i in inblocks if i['type'] != 'EmptyStatement'][-1]
                if switchone and lastone['type'] == 'BreakStatement':
                    switchone = switchone[0]
                    sort_str, sort_idx = None, None
                    for i in firstone['declarations']:
                        try:
                            var = js2py.eval_js(get_script_from_tree(i['init']))
                        except:
                            # print(i,'-=-=-=-=-=-=-=-=-=-=-=-=-=')
                            raise
                        if isinstance(var, int):
                            sort_idx = var
                        else:
                            sort_str = var.to_list()
                    if switchone['discriminant']['property']['operator'] == '++':
                        rplpack = [None] * len(sort_str)
                        for case in switchone['cases']:
                            cover_undefined_null(case)
                            rplpack[sort_str.index(case['test']['value'])] = case
                        rpllist = []
                        for case in rplpack:
                            for incas in case['consequent']:
                                if incas['type'] == 'ContinueStatement': break
                                rpllist.append(incas)
                        rpllist.append(lastone)
                        return rpllist
    except Exception as e:
        print('remake_while_statement error. ======',e)
        # import traceback
        # print(traceback.format_exc())

def handle_key_value():
    for node, parent_body, curr_key, curr_idx in packer:
        if node['type'] == 'ObjectExpression' and parent_body.get('type') == 'VariableDeclarator':
            hmaps[parent_body['id']['name']] = d = {}
            for key in node['properties']:
                d[key['key']['value']] = key['value']
            hldel.append([parent_body, curr_key])
        if node['type'] == 'ArrayExpression' and parent_body.get('type') == 'VariableDeclarator':
            lmaps[parent_body['id']['name']] = d = []
            for key in node['elements']:
                d.append(key)
            hldel.append([parent_body, curr_key])

def handle_key_values_delete():
    for parent_body, curr_key in hldel:
        del(parent_body[curr_key])

def handle_key_value_input():
    def cover_list(node):
        if node['type'] == 'MemberExpression' and node['object'].get('name'):
            kname = node['object'].get('name')
            vname = node['property'].get('value')
            if kname in hmaps:
                if vname in hmaps[kname]:
                    return hmaps[kname][vname]
        else:
            return node
    for node, parent_body, curr_key, curr_idx in packer:
        if node['type'] == 'MemberExpression' and node['object'].get('name'):
            kname = node['object'].get('name')
            vname = node['property'].get('value')
            if kname in hmaps:
                if vname in hmaps[kname]:
                    if curr_idx is None:
                        parent_body[curr_key] = cover_list(hmaps[kname][vname])
                    else:
                        parent_body[curr_key][curr_idx] = cover_list(hmaps[kname][vname])
            if kname in lmaps:
                if isinstance(vname, (float,int)):
                    if curr_idx is None:
                        parent_body[curr_key] = lmaps[kname][int(vname)]
                    else:
                        parent_body[curr_key][curr_idx] = lmaps[kname][int(vname)]

def remake_switch():
    for node, parent_body, curr_key, curr_idx in packer:
        if node['type'] == 'WhileStatement':
            rpllist = remake_while_statement(node, parent_body, curr_key, curr_idx)
            if rpllist:
                # node['body']['body'] = rpllist
                rpllist.pop()
                parent_body['body'] = parent_body['body'][:curr_idx] + rpllist + parent_body['body'][curr_idx+1:]

def catch_simple_func(node):
    try:
        if node.get('type') and node['type'] == 'CallExpression':
            _node = node['callee']
            _args = node['arguments']
            if _node.get('type') and _node['type'] == 'FunctionExpression':
                if _node['body']['type'] == 'BlockStatement':
                    ret = _node['body']['body']
                    prm = _node['params']
                    if len(ret) == 1:
                        if ret[0]['argument']['type'] == 'BinaryExpression' and len(prm) == 2:
                            left = ret[0]['argument']['left']
                            right = ret[0]['argument']['right']
                            if  left['name'] == _node['params'][0]['name'] and\
                                right['name'] == _node['params'][1]['name']:
                                return ret[0]['argument'], 1
                            elif left.get('type') in ['Identifier', 'Literal'] or right.get('type') in ['Identifier', 'Literal'] and len(_args) == 2:
                                if ((left.get('type') == 'Identifier' and left.get('name') == _args[0].get('name')) or 
                                    (left.get('type') == 'Literal'    and left.get('value') == _args[0].get('value'))) and \
                                   ((right.get('type') == 'Identifier' and right.get('name') == _args[1].get('name')) or 
                                    (right.get('type') == 'Literal'    and right.get('value') == _args[1].get('value'))):
                                    return ret[0]['argument'], 1
                        elif ret[0]['argument']['type'] == 'CallExpression':
                            call = ret[0]['argument']['callee']
                            args = ret[0]['argument']['arguments']
                            if call.get('name') == prm[0].get('name'):
                                rt = copy.deepcopy(ret[0]['argument'])
                                rt['callee']['name'] = _args[0].get('name')
                                rt['arguments'] = _args[1:]
                                return rt, 2
    except:
        import traceback
        traceback.print_exc()
        pass

def remake_binary_exp():
    catchtypes = [
        'CallExpression', 
        'BinaryExpression', 
        'Literal', 
        'Identifier', 
        'MemberExpression',
        'CallExpression',
        'UnaryExpression',
    ]
    for node, parent_body, curr_key, curr_idx in packer:
        catchnode = catch_simple_func(node)
        if catchnode:
            catchnode, _type = catchnode
            catchnode = copy.deepcopy(catchnode)
            if _type == 1:
                a = node['arguments'][0]
                b = node['arguments'][1]
                at = a.get('type')
                bt = b.get('type')
                if at in catchtypes and bt in catchtypes:
                    catchnode['left'] = a.copy()
                    catchnode['right'] = b.copy()
                    if curr_idx is None:
                        parent_body[curr_key] = catchnode
                    else:
                        parent_body[curr_key][curr_idx] = catchnode
            else:
                if curr_idx is None:
                    parent_body[curr_key] = catchnode
                else:
                    parent_body[curr_key][curr_idx] = catchnode

# 下面四个函数功能总和为“名字长度的压缩”，主要是 convenience_names 函数，请谨慎使用
def cover_name(node):
    name = node.get('name')
    if name:
        aname.append(name)
        matchname = re.findall('_0x[0-9a-zA-Z]{6}', name)
        if matchname:
            nmaps[matchname[0]] = None

def distribute_name(node):
    global nmaps, aname, name_index, name_chains
    name = node.get('name')
    if name:
        if name in nmaps:
            cname = nmaps.get(name)
            if not cname:
                # _name = 'vv{}'.format(name_index)
                _name = next(name_chains)
                while _name in aname:
                    name_index += 1
                    # _name = 'vv{}'.format(name_index)
                    _name = next(name_chains)
                aname.append(_name)
                nmaps[name] = cname = _name
            node['name'] = cname

def _convenience_names(tree, cover_func):
    if isinstance(tree, dict):
        cover_func(tree)
        for key in tree:
            if isinstance(tree[key], dict):
                _convenience_names(tree[key], cover_func)
            elif isinstance(tree[key], list):
                for idx, _tree in enumerate(tree[key]):
                    _convenience_names(_tree, cover_func)

def convenience_names(tree):
    from itertools import chain, product
    global nmaps, aname, name_index, name_chains
    s = 'abcdefghijklmnopqrstuvwxyz'
    nmaps, aname, name_index, name_chains = {}, [], 0, chain(product(s), product(s,s), product(s,s,s))
    _convenience_names(tree, cover_name)
    _convenience_names(tree, distribute_name)
    return tree



# 通过脚本对js代码切分，将rc4算法切出来单独封装，后续先将代码中的 rc4 加密全部解析
# 后面再继续通过其他的方式将代码重构一遍，这里算是第一步，结构 rc4 加密
# 这里可以先打印看看解密出函数的样子，由于rc4 这一步有时候会耗时非常长
# 所以我在开发的时候是在这里中断一下将目前脚本打印出来，然后直接用目前的脚本从下面的步骤直接解析开始

def sojson_decode(script):
    global funcname, decoder_func, hmaps, lmaps, hldel
    hmaps, lmaps, hldel = {}, {}, []
    funcname, decoder, tree = get_sojson_encoder(script)
    decoder_func = decoder[funcname]
    convenience_tree_rc4(tree)
    # newjscode = get_script_from_tree(tree)
    # print(newjscode)
    # tree = pyjsparser.parse(script)
    convenience_tree_remake(tree)
    handle_key_value()
    handle_key_value_input()
    handle_key_values_delete()
    remake_switch()
    remake_binary_exp()
    # convenience_names(tree) # 函数以及参数名字压缩，只处理固定正则的名字防止销毁某些原始参数，慎用
    # print("注意，自动将匹配 _0x[0-9a-zA-Z]{6} 正则的参数或函数名字压缩，请谨慎使用！！！！")
    return get_script_from_tree(tree)

def normal_decode(script):
    global hmaps, lmaps, hldel
    hmaps, lmaps, hldel = {}, {}, []
    tree = pyjsparser.parse(script)
    convenience_tree_remake(tree)
    handle_key_value()
    handle_key_value_input()
    handle_key_values_delete()
    remake_switch()
    remake_binary_exp()
    # convenience_names(tree) # 函数以及参数名字压缩，只处理固定正则的名字防止销毁某些原始参数，慎用
    # print("注意，自动将匹配 _0x[0-9a-zA-Z]{6} 正则的参数或函数名字压缩，请谨慎使用！！！！")
    return get_script_from_tree(tree)

v = sojson_decode(script)
v = normal_decode(v)
print(v)




script = r'''
var ttt2 = function(a){
    return a+10;
}
var some2 = function (_0xasdfa, b, c) {
    return _0xasdfa(b)
}(ttt2, 123, 33);
'''

# v = normal_decode(script)
# print(v)