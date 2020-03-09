# -*- coding: utf-8 -*-

# 完全依赖 js2py

# 通过生成语法树，快速修改内部的某些混肴处理，从而简化代码
# 直接使用 js2py 非常方便，因为其内部已经自带了一些 js 库的 python 化代码
# 使用其中的 escodegen 模块就可以重新将语法树重构成代码。代码如下。



script = r'''
/*
 * 加密工具已经升级了一个版本，目前为 sojson.v5 ，主要加强了算法，以及防破解【绝对不可逆】配置，耶稣也无法100%还原，我说的。;
 * 已经打算把这个工具基础功能一直免费下去。还希望支持我。
 * 另外 sojson.v5 已经强制加入校验，注释可以去掉，但是 sojson.v5 不能去掉（如果你开通了VIP，可以手动去掉），其他都没有任何绑定。
 * 誓死不会加入任何后门，sojson JS 加密的使命就是为了保护你们的Javascript 。
 * 警告：如果您恶意去掉 sojson.v5 那么我们将不会保护您的JavaScript代码。请遵守规则 */
 
;var encode_version = 'sojson.v5', jdbia = '',  _0x3c82=['5Liq6IKi5Yil6ZqARcOsEk96bRFBwr8=','56mL6ZWe5oyl6amU57iEFuKCpnvDkOWJt+WsgeKAiETlk57DqOKAssKpR+inqeWtnuKAhzLvvJHkv6TljpLkvaXnm4Qow5p744OM','5aeT5pyf5oG755iew5nDt+mHvuW0ieWmhuS4rsK8w45i776ZwobClMOe5qCU56y277yI566/566m5YaW5Lm+6Z2EdwQ+MCFDw4o3WsKd55ml5Lmn56Kl77yI6K6e5oy/5Yym5YeP5pyM5YSp5YmO5a+x44OM6L6p5Lq55bWE5YaO5LqQ6IO45Ym55a2Hw47DqyzjgaPDuHvCu+etseapr+eJkuWFqOWshA==','w7tPw6bDow==','U8KFwrDDv8Ou','wqY4wpTCvBMt','w5nDpCxVwoc=','w5rCpcKrworDmMObwrg=','bE/CvHp+','wqHDiEliw4bDjcOQw5HCpw==','AMKLQDnDpA=='];(function(_0x585741,_0x2d1462){var _0x8dba70=function(_0xf7c352){while(--_0xf7c352){_0x585741['push'](_0x585741['shift']());}};_0x8dba70(++_0x2d1462);}(_0x3c82,0x12a));var _0xa087=function(_0xe626a8,_0x543a49){_0xe626a8=_0xe626a8-0x0;var _0x378c5d=_0x3c82[_0xe626a8];if(_0xa087['initialized']===undefined){(function(){var _0x4c4fd4=typeof window!=='undefined'?window:typeof process==='object'&&typeof require==='function'&&typeof global==='object'?global:this;var _0x1ab0e6='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';_0x4c4fd4['atob']||(_0x4c4fd4['atob']=function(_0xc95f7c){var _0x95b729=String(_0xc95f7c)['replace'](/=+$/,'');for(var _0x4fc580=0x0,_0x107800,_0x29275a,_0x25758a=0x0,_0x76ae45='';_0x29275a=_0x95b729['charAt'](_0x25758a++);~_0x29275a&&(_0x107800=_0x4fc580%0x4?_0x107800*0x40+_0x29275a:_0x29275a,_0x4fc580++%0x4)?_0x76ae45+=String['fromCharCode'](0xff&_0x107800>>(-0x2*_0x4fc580&0x6)):0x0){_0x29275a=_0x1ab0e6['indexOf'](_0x29275a);}return _0x76ae45;});}());var _0x58b570=function(_0x2c6ea7,_0x423b52){var _0x418844=[],_0x3f01e8=0x0,_0x4f82d4,_0x4ae1a7='',_0xb4be10='';_0x2c6ea7=atob(_0x2c6ea7);for(var _0x1c1d06=0x0,_0x42f4aa=_0x2c6ea7['length'];_0x1c1d06<_0x42f4aa;_0x1c1d06++){_0xb4be10+='%'+('00'+_0x2c6ea7['charCodeAt'](_0x1c1d06)['toString'](0x10))['slice'](-0x2);}_0x2c6ea7=decodeURIComponent(_0xb4be10);for(var _0xce3311=0x0;_0xce3311<0x100;_0xce3311++){_0x418844[_0xce3311]=_0xce3311;}for(_0xce3311=0x0;_0xce3311<0x100;_0xce3311++){_0x3f01e8=(_0x3f01e8+_0x418844[_0xce3311]+_0x423b52['charCodeAt'](_0xce3311%_0x423b52['length']))%0x100;_0x4f82d4=_0x418844[_0xce3311];_0x418844[_0xce3311]=_0x418844[_0x3f01e8];_0x418844[_0x3f01e8]=_0x4f82d4;}_0xce3311=0x0;_0x3f01e8=0x0;for(var _0x23353a=0x0;_0x23353a<_0x2c6ea7['length'];_0x23353a++){_0xce3311=(_0xce3311+0x1)%0x100;_0x3f01e8=(_0x3f01e8+_0x418844[_0xce3311])%0x100;_0x4f82d4=_0x418844[_0xce3311];_0x418844[_0xce3311]=_0x418844[_0x3f01e8];_0x418844[_0x3f01e8]=_0x4f82d4;_0x4ae1a7+=String['fromCharCode'](_0x2c6ea7['charCodeAt'](_0x23353a)^_0x418844[(_0x418844[_0xce3311]+_0x418844[_0x3f01e8])%0x100]);}return _0x4ae1a7;};_0xa087['rc4']=_0x58b570;_0xa087['data']={};_0xa087['initialized']=!![];}var _0x3c6679=_0xa087['data'][_0xe626a8];if(_0x3c6679===undefined){if(_0xa087['once']===undefined){_0xa087['once']=!![];}_0x378c5d=_0xa087['rc4'](_0x378c5d,_0x543a49);_0xa087['data'][_0xe626a8]=_0x378c5d;}else{_0x378c5d=_0x3c6679;}return _0x378c5d;};(function(_0x51c68b,_0x352bf5){var _0x410248={'cgGFI':'这是一个一系列js操作。','QTjxi':_0xa087('0x0','Na@a'),'atuAs':_0xa087('0x1','$tsE')};_0x51c68b[_0xa087('0x2','Na@a')]=_0x410248[_0xa087('0x3','ovpO')];_0x352bf5[_0xa087('0x4','lpGj')]=_0x410248[_0xa087('0x5','lb5B')];_0x352bf5[_0xa087('0x6','nV3[')]=_0x410248[_0xa087('0x7','9Unm')];}(window,document));;if(!(typeof encode_version!==_0xa087('0x8','#Bz]')&&encode_version==='sojson.v5')){window[_0xa087('0x9','U]5w')](_0xa087('0xa','T($H'));};encode_version = 'sojson.v5';
'''













































import json
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
    import js2py.py_node_modules.escodegen as escodegen
    escodegen = escodegen.var.get('escodegen')
    generate = escodegen.get('generate')
    return generate(tree).to_python()

def cover_undefined_null(node):
    # 如果不使用 js2py 内部的数据结构来包装一下这类的数据，反编译回 js 代码时就会出现问题。
    if node.get('raw') == 'null' and node.get('value', '') is None:
        node['value'] = JS_BUILTINS['null']
    elif node.get('raw') == 'undefined' and node.get('undefined', '') is None:
        node['value'] = JS_BUILTINS['undefined']

def get_sojson_encoder(script):
    tree = pyjsparser.parse(script)
    for idx, node in enumerate(tree['body']):
        if node['type'] == 'VariableDeclaration' and \
                        node.get('declarations') and \
                        node.get('declarations')[0].get('init') and \
                        node.get('declarations')[0].get('init').get('type') == 'FunctionExpression':
            break
    oldtree = tree['body'].copy()
    tree['body'] = oldtree[:idx+1]
    funcname = node.get('declarations')[0].get('id').get('name')
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
    except:
        import traceback
        print(traceback.format_exc())


hmaps = {}
lmaps = {}
hldel = []
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
                    parent_body[curr_key] = lmaps[kname][int(vname)]

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
            node = node['callee']
            if node.get('type') and node['type'] == 'FunctionExpression':
                if node['body']['type'] == 'BlockStatement':
                    ret = node['body']['body']
                    prm = node['params']
                    if len(ret) == 1 and len(prm) == 2 and ret[0]['argument']['type'] == 'BinaryExpression':
                        if  ret[0]['argument']['left']['name'] == node['params'][0]['name'] and\
                            ret[0]['argument']['left']['name'] == node['params'][0]['name']:
                            return ret[0]['argument']
    except:
        pass

def remake_binary_exp():
    for node, parent_body, curr_key, curr_idx in packer:
        catchnode = catch_simple_func(node)
        if catchnode:
            if node['arguments'][0].get('type') == 'Literal' and node['arguments'][1].get('type') == 'Literal':
                catchnode['left'] = node['arguments'][0]
                catchnode['right'] = node['arguments'][1]
                parent_body[curr_key] = catchnode

# def handle_simple_eval():
#     for node, parent_body, curr_key, curr_idx in packer:
#         if node.get('type') == 'CallExpression':
#             try:
#                 s = js2py.eval_js(get_script_from_tree(node))
#                 parent_body[curr_key] = {'type': 'Literal', 'value':s, 'raw':repr(s)}
#                 print('success',s)
#             except:
#                 print('error.')









# 通过脚本对js代码切分，将rc4算法切出来单独封装，后续先将代码中的 rc4 加密全部解析
# 后面再继续通过其他的方式将代码重构一遍，这里算是第一步，结构 rc4 加密
# 这里可以先打印看看解密出函数的样子，由于rc4 这一步有时候会耗时非常长
# 所以我在开发的时候是在这里中断一下将目前脚本打印出来，然后直接用目前的脚本从下面的步骤直接解析开始
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

v = get_script_from_tree(tree)
print(v)






# script = r'''
# var k = [1,2,'3']
# var t = {
#     'key1': '2|1',
#     'key2': function(a,b){
#         return a+b
#     },
# };
# var s = t['key1']['split']('|') , i = 0;
# while (!![]){
#     switch (s[i++]){
#         case '1':
#             var some = t['key2'](1, 2);
#             console.log(s[i], i, 111);
#             continue;
#         case '2':
#             console.log(s[i], i, 222);
#             continue;
#     }
#     break;;
# }
# '''
# tree = pyjsparser.parse(script)
# convenience_tree_remake(tree)
# handle_key_value()
# handle_key_value_input()
# remake_switch()
# remake_binary_exp()

# v = get_script_from_tree(tree)
# print(v)
# print()











# script = r'''
# var ttt= function(a, b){
#     return a+b+1
# }
# var some = function (a, b) {
#     return a + b;
# }(1, 3);
# 1 + 2
# '''
# tree = pyjsparser.parse(script)
# convenience_tree_remake(tree)
# handle_key_value()
# handle_key_value_input()
# remake_switch()
# remake_binary_exp()
# handle_simple_eval()

# v = get_script_from_tree(tree)
# print(v)