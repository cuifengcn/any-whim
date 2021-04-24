// 从浏览器直接扒各种参数环境的脚本
console.log(make_all()) // 使用时候解开该行注释，然后将生成的代码都放到控制台中直接执行，复制生成的字符出即可。
function get_all(){
    function generatecode4v(name_, key, v, o, be_values) {
        if (be_values.indexOf(key) == -1){
            if (typeof (v) == "object") {
                if (v == null) {
                    return `${name_}["${key}"] = null;\r\n`
                }
                if (o == v){
                    return `${name_}["${key}"] = ${name_};\r\n`
                }
                try {
                    return `${name_}["${key}"] = _vPxy(new class ${v.constructor.name}{}, "${key}");\r\n`
                } catch (error) {
                    return `${name_}["${key}"] = "----------------------------------------------------------------";\r\n`
                }
            }
            if (typeof (v) == "string") {
                if (v.indexOf('"') == -1){
                    return `${name_}["${key}"] = "${v}";\r\n`
                }else if (v.indexOf("'") == -1){
                    return `${name_}["${key}"] = '${v}';\r\n`
                }else{
                    return `${name_}["${key}"] = \`${v}\`;\r\n`
                }
            }
            if (typeof (v) == "function") {
                return `${name_}["${key}"] = function ${v.name}(){_vLog('--- func(*) --- ${v.name}');debugger;};   safefunction(${name_}["${key}"]);\r\n`
            }
        }else{
            return `${name_}["${key}"] = ${JSON.stringify(v)};\r\n`
        }
        return `${name_}["${key}"] = ${v};\r\n`
    }
    function generatecode4v1(name_, key, v, o, be_values) {
        if (be_values.indexOf(key) == -1){
            if (typeof (v) == "object") {
                if (v == null) {
                    return `${name_}.__proto__["${key}"] = null;\r\n`
                }
                try {
                    return `${name_}.__proto__["${key}"] = _vPxy(new class ${v.constructor.name}{}, "${key}");\r\n`
                } catch (error) {
                    return `${name_}.__proto__["${key}"] = "----------------------------------------------------------------";\r\n`
                }
            }
            if (typeof (v) == "string") {
                if (v.indexOf('"') == -1){
                    return `${name_}.__proto__["${key}"] = "${v}";\r\n`
                }else if (v.indexOf("'") == -1){
                    return `${name_}.__proto__["${key}"] = '${v}';\r\n`
                }else{
                    return `${name_}.__proto__["${key}"] = \`${v}\`;\r\n`
                }
            }
            if (typeof (v) == "function") {
                return `${name_}.__proto__["${key}"] = function ${v.name}(){_vLog('--- func(*) --- ${v.name}');debugger;};   safefunction(${name_}["${key}"]);\r\n`
            }
            if (name_ == 'document' && key == 'all'){
                return `${name_}.__proto__["${key}"] = undefined;\r\n`
            }
        }else{
            return `${name_}.__proto__["${key}"] = ${JSON.stringify(v)};\r\n`
        }
        return `${name_}.__proto__["${key}"] = ${v};\r\n`
    }
    function generate4example(example, name_, skips, be_values) {
        var code = "";
        var protos = {}
        if (typeof (example) == "object" && example.prototype == undefined) {
            for (let key in example.__proto__) {
                protos[key] = true;
            }
            for (let key in example) {
                if (protos[key] == undefined) {
                    if (key && skips.indexOf(key) == -1){
                        try{
                           code += generatecode4v(name_, key, example[key], example, be_values);
                        }catch(e){
                            console.log('========== error ==========')
                            console.log(key)
                            console.log(e)
                        }
                    }
                }
            }
        }
        return alignment_safefunction(alignment(code));
    }
    function generate4Prototype(example, name_, skips, be_values) {
        var code = "";
        if (typeof (example) == "object" && example.prototype == undefined) {
            for (let key in example.__proto__) {
                if (skips.indexOf(key) == -1){
                    try{
                        code += generatecode4v1(name_, key, example[key], example, be_values);
                    }catch(e){
                        console.log('========== error ==========')
                        console.log(key)
                        console.log(e)
                    }
                }
            }
        }
        return alignment_safefunction(alignment(code))
    }
    function alignment(str){
        var max_protolen = 0
        if (str.trim().length == 0){
            return str
        }
        var mch = str.match(/(\["[^"]+"\]) *=/g)
        if (!(mch)){
            return str
        }
        mch.map(function(e){
            if (e.length > max_protolen){
                max_protolen = e.length
            }
        })
        return str.replace(/(\["[^"]+"\]) *=/g, function(_, e){
            return e + Array(max_protolen-e.length-1).fill(" ").join("") + '='
        })
    }
    function alignment_safefunction(str){
        var max_protolen = 0
        if (str.trim().length == 0){
            return str
        }
        var mch = str.match(/(=[^=]+); *safefunction/g)
        if (!(mch)){
            return str
        }
        mch.map(function(e){
            if (e.length > max_protolen){
                max_protolen = e.length
            }
        })
        return str.replace(/(=[^=]+;) *safefunction/g, function(_, e){
            return e + Array(max_protolen-e.length-14).fill(" ").join("") + 'safefunction'
        })
    }
    function vall(example, name_, skips, be_values){
        skips = skips || []
        be_values = be_values || []
        var protostr = generate4Prototype(example, name_, skips, be_values)
        var objectstr = generate4example(example, name_, skips, be_values)
        return protostr + objectstr
    }
    vall.generate4example = generate4example
    vall.generate4Prototype = generate4Prototype
    // placeholder1
}
function make_all(){
    var ret;
    ret = Cilame + '\r\n'
    ret += get_all + '\r\n'
    ret = ret.replace('// placeholder1', `
    console.log(
    Cilame + "\\r\\n" +
    "Cilame()\\r\\n" +
    vall(window,                 "window",               ${JSON.stringify(Cilame())}.concat(['_vLog', '_vPxy'])) +
    vall(document,               "document",             ['cookie', 'addEventListener', 'dispatchEvent', 'removeEventListener', "createElement", "getElementsByName"]) +
    vall(Node.prototype,         "Node.prototype",       ["location", 'addEventListener', 'dispatchEvent', 'removeEventListener']) +
    vall(navigator,              "navigator",            ['connection'],    ['languages']) +
    vall(window.location,        "window.location") +
    vall(window.localStorage,    "window.localStorage",   ["clear", "getItem", "key", "removeItem", "setItem", "length"]) +
    vall(window.sessionStorage,  "window.sessionStorage", ["clear", "getItem", "key", "removeItem", "setItem", "length"]) +
\`for (let key in navigator.__proto__) {
    navigator[key] = navigator.__proto__[key];
    if (typeof (navigator.__proto__[key]) != "function") {
        navigator.__proto__.__defineGetter__(key, function() {
            debugger ;var e = new Error();
            e.name = "TypeError";
            e.message = "Illegal invocation";
            e.stack = "VM988:1 Uncaught TypeError: Illegal invocation \\\\r\\\\n at <anonymous>:1:19";
            throw e;
        });
    }
}
window                = VmProxyB(window,                "window")
window.document       = VmProxyB(window.document,       "window.document")
window.navigator      = VmProxyB(window.navigator,      "window.navigator")
window.location       = VmProxyB(window.location,       "window.location")
window.localStorage   = VmProxyB(window.localStorage,   "window.localStorage")
window.sessionStorage = VmProxyB(window.sessionStorage, "window.sessionStorage")

hookFunc('eval')
hookFunc('Function')
start = true  // 主要的 VmProxyB 的log开关
// start1 = true // 一些未被实现的 _vPxy(new class Unknown{}) 的 Proxy 打印日志，让输出更清晰，不过尽量不要使用这个
\`)`)
    ret += '\r\n'
    ret += 'get_all()\r\n// 将生成的代码全部拷贝到 chrome 控制台执行即可'
    return ret
}
















// 以下就是就是一个补环境的简单处理，现在还不成熟，后面慢慢补







function Cilame(){
    // 生成一些重要的参数，比如 screen Screen 这种对应的系统对象
    // 这些系统对象原型结构稍微有点绕，统一成下面模式就行
    ;(function(){
        const $toString = Function.toString;
        const myFunction_toString_symbol = Symbol('('.concat('', ')_', (Math.random() + '').toString(36)));
        const myToString = function() {
            return typeof this == 'function' && this[myFunction_toString_symbol] || $toString.call(this);
        };
        function set_native(func, key, value) {
            Object.defineProperty(func, key, {
                "enumerable": false,
                "configurable": true,
                "writable": true,
                "value": value
            })
        };
        delete Function.prototype['toString'];
        set_native(Function.prototype, "toString", myToString);
        set_native(Function.prototype.toString, myFunction_toString_symbol, "function toString() { [native code] }");
        ;(typeof global=='undefined'?window:global).safefunction = function(func){
            set_native(func, myFunction_toString_symbol, `function ${myFunction_toString_symbol,func.name || ''}() { [native code] }`);
            return func
        };
        function make_constructor(name, Name, name_inject_objs, Name_inject_objs, proto, config){
            config = config !== undefined?config:{}
            var allow_illegal = config['allow_illegal']
            var illegalstr = (!allow_illegal)?'throw new TypeError("Illegal constructor");':''
            var evalstr = `
            var ${name}Constructor = function ${Name=="WindowProperties"?"EventTarget":Name}() { ${illegalstr} }
            safefunction(${name}Constructor);
            var ${name}Prototype = (proto!==undefined?proto:{});
            Object.defineProperties(${name}Prototype, {
                constructor: { value: ${name}Constructor, writable: true, configurable: true },
                [Symbol.toStringTag]: { value: "${Name}", configurable: true }
            });
            ${name}Constructor.prototype = ${name}Prototype;
            var ${Name} = function ${Name}() {}
            safefunction(${Name});
            var ${name} = new ${Name}();
            ${name}.__proto__ = ${name}Prototype;
            __cilame__['n']["${name}"] = ${name}
            __cilame__['N']["${Name}"] = ${Name}
            if (name_inject_objs.length){ name_inject_objs.map(function(e){ Object.defineProperty(e, "${name}", { configurable: true, writable: true, value: ${name} }); }) }
            if (Name_inject_objs.length){ Name_inject_objs.map(function(e){ Object.defineProperty(e, "${Name}", { configurable: true, writable: true, value: ${name}Constructor }); }) }
            `
            eval(evalstr)
        }
        ;(typeof global=='undefined'?window:global).make_constructor = make_constructor
        ;(typeof global=='undefined'?window:global).start = false
        ;(typeof global=='undefined'?window:global).start1 = false
        ;(typeof global=='undefined'?window:global)._vLog = function _vLog(){ if (start1){ 
            console.log.apply(console.log, [].slice.call(arguments))
        }}
        ;(typeof global=='undefined'?window:global)._vPxy = function(G, M){
            var _vLog = (typeof global=='undefined'?window:global)._vLog || console.log
            function LS(T, M, F){ return `${M}[${T.constructor.name}].(Prxoy)${F} ==>>`}
            return new Proxy(G, {
                apply:                    function(T, A, L){    _vLog(LS(G, M, 'apply') );                    return Reflect.apply(T, A, L) },
                construct:                function(T, L, N){    _vLog(LS(G, M, 'construct') );                return Reflect.construct(T, L, N) },
                deleteProperty:           function(T, P){       _vLog(LS(G, M, 'deleteProperty') );           return Reflect.deleteProperty(T, P) },
                get:                      function(T, P, R){    _vLog(LS(G, M, 'get'), P);                    return Reflect.get(T, P, R) },
                // defineProperty:           function(T, P, A){    _vLog(LS(G, M, 'defineProperty') );           return Reflect.defineProperty(T, P, A) },
                // getOwnPropertyDescriptor: function(T, P){       _vLog(LS(G, M, 'getOwnPropertyDescriptor') ); return Reflect.getOwnPropertyDescriptor(T, P) },
                getPrototypeOf:           function(T){          _vLog(LS(G, M, 'getPrototypeOf') );           return Reflect.getPrototypeOf(T) },
                has:                      function(T, P){       _vLog(LS(G, M, 'has') );                      return Reflect.has(T, P) },
                isExtensible:             function(T){          _vLog(LS(G, M, 'isExtensible') );             return Reflect.isExtensible(T) },
                ownKeys:                  function(T){          _vLog(LS(G, M, 'ownKeys') );                  return Reflect.ownKeys(T) },
                preventExtensions:        function(T){          _vLog(LS(G, M, 'preventExtensions') );        return Reflect.preventExtensions(T) },
                set:                      function(T, P, V, R){ _vLog(LS(G, M, 'set'), P);                    return Reflect.set(T, P, V, R) },
                setPrototypeOf:           function(T, P){       _vLog(LS(G, M, 'setPrototypeOf'));            return Reflect.setPrototypeOf(T, P) },
            })
        }
        function logA(tag, G_or_S, objectname, propertyname, value){
            console.table([{tag, G_or_S, objectname, propertyname,value}], ["tag","G_or_S","objectname","propertyname","value"]);
        }
        function logB(tag, GS, objectname, propertyname, value){
            console.info(tag, GS, `[${objectname}]`, `"${propertyname}"`, value);
        }
        function VmProxy(logger, object_, titlename, dont_log_value){
            return new Proxy(object_, {
                get (target, property) { 
                    if (start){
                        logger(titlename, "Get >>", target.constructor.name, property, dont_log_value?'<DONTLOG>':target[property]);
                    }
                    return target[property];
                },
                set (target, property, value) {
                    if (start){
                        logger(titlename, "Set <<", target.constructor.name, property, dont_log_value?'<DONTLOG>':value);
                    }
                    target[property] = value;
                }
            });
        };
        var VmProxyA = function (){return VmProxy.apply(this, [logA].concat([].slice.call(arguments)))}
        var VmProxyB = function (){return VmProxy.apply(this, [logB].concat([].slice.call(arguments)))}
        ;(typeof global=='undefined'?window:global).VmProxyA = VmProxyA
        ;(typeof global=='undefined'?window:global).VmProxyB = VmProxyB
        ;(typeof global=='undefined'?window:global).hookFunc = function hookFunc(H){
            eval(`
            _v${H} = ${H}
            window.${H} = function ${H}(){
                if (window.start){
                    console.log('-------------------- ${H}(*) --------------------')
                    console.log(arguments[0])
                }
                return _v${H}.apply(this, arguments)
            }
            safefunction(window.${H})
            `)
        }
    })();
    // 将核心结构初始化，也就是 window navigator document 等初始化处理好
    var __cilame__ = { 'n':{}, 'N':{}, 'c':{} } // 临时存储空间, n 为 new 对象, N 为原始方法.
    var GL = _global = (typeof global=='undefined'?window:global)
    make_constructor("eventTarget", "EventTarget", [], [GL], undefined, { allow_illegal: true })
    EventTarget.prototype.listeners = {};
    EventTarget.prototype.addEventListener = function(type, callback) {
        if(!(type in this.listeners)) { this.listeners[type] = []; }
        this.listeners[type].push(callback);
    };
    EventTarget.prototype.removeEventListener = function(type, callback) {
        if(!(type in this.listeners)) { return; }
        var stack = this.listeners[type];
        for(var i = 0, l = stack.length; i < l; i++) { if(stack[i] === callback){ stack.splice(i, 1); return this.removeEventListener(type, callback); } }
    };
    EventTarget.prototype.dispatchEvent = function(event) {
        if(!(event.type in this.listeners)) { return; }
        var stack = this.listeners[event.type];
        event.target = this;
        for(var i = 0, l = stack.length; i < l; i++) { stack[i].call(this, event); }
    };
    make_constructor("windowProperties",    "WindowProperties", [], [], new EventTarget, { allow_illegal: true })
    make_constructor("window",              "Window", [GL], [GL],       __cilame__['n']['windowProperties']) // WindowProperties 没有注入 window 环境
    window = new Proxy(window, {
        get: function(a,b,c){
            return a[b] || global[b]
        },
        set: function(a,b,c){
            global[b] = c
            return a[b] = c
        }
    })
    // window 生成之后将 global 内部的常用函数直接传到 window 里面
    var Gkeys = Object.getOwnPropertyNames(global), exclude = ['global', 'process', '_global']
    for (var i = 0; i < Gkeys.length; i++) {
        if (exclude.indexOf(Gkeys[i]) == -1){ window[Gkeys[i]] = global[Gkeys[i]] }
    }
    var EN = normal_env = [window, GL]
    make_constructor("navigator",   "Navigator",    EN, EN)
    window.clientInformation = navigator
    // 处理 document 初始化
    make_constructor("_vNode",      "Node",         [], EN, new EventTarget)
    make_constructor("_vDocument",  "Document",     [], EN, __cilame__["n"]['_vNode'], { allow_illegal: true })
    make_constructor("document",    "HTMLDocument", EN, EN, __cilame__["n"]['_vDocument'])
    ;(function(){
        'use strict';
        var cookie_cache = document.cookie = "";
        Object.defineProperty(document, 'cookie', {
            get: function() {
                console.log('==>> Get Cookie', cookie_cache);
                return cookie_cache;
            },
            set: function(val) {
                console.log('<<== Set Cookie', val);
                var cookie = val.split(";")[0];
                var ncookie = cookie.split("=");
                var flag = false;
                var cache = cookie_cache.split("; ");
                cache = cache.map(function(a) {
                    if (a.split("=")[0] === ncookie[0]) {
                        flag = true;
                        return cookie;
                    }
                    return a;
                })
                cookie_cache = cache.join("; ");
                if (!flag) {
                    cookie_cache += cookie + "; ";
                }
                return cookie_cache;
            }
        });
        global.init_cookie = function init_cookie(str){
            cookie_cache = str
        }
    })();
    // 处理 location 初始化，以及绑定 document
    make_constructor("location",    "Location",     EN, EN)
    location["ancestorOrigins"] = new (class DOMStringList {});
    location["assign"]          = function assign(){debugger;};  safefunction(location["assign"]);
    location["reload"]          = function reload(){debugger;};  safefunction(location["reload"]);
    location["replace"]         = function replace(){debugger;}; safefunction(location["replace"]);
    Object.defineProperty(location, 'href', {
        get: function(){
            return location.protocol + "//" + location.host + (location.port ? ":" + location.port : "") + location.pathname + location.search + location.hash;
        },
        set: function(href){
            var a = href.match(/([^:]+:)\/\/([^/:?#]+):?(\d+)?([^?#]*)?(\?[^#]*)?(#.*)?/);
            location.protocol = a[1] ? a[1] : "";
            location.host     = a[2] ? a[2] : "";
            location.port     = a[3] ? a[3] : "";
            location.pathname = a[4] ? a[4] : "";
            location.search   = a[5] ? a[5] : "";
            location.hash     = a[6] ? a[6] : "";
            location.hostname = location.host;
            location.origin   = location.protocol + "//" + location.host + (location.port ? ":" + location.port : "");
        }
    });
    document.location = location

    // 处理 localStorage 和 sessionStorage 的初始化
    function Storage(){}
    Storage.prototype.clear      = function clear(){            debugger; var self = this; Object.keys(self).forEach(function (key) { self[key] = undefined; delete self[key]; }); }
    Storage.prototype.getItem    = function getItem(key){       debugger; return this.hasOwnProperty(key)?String(this[key]):null }
    Storage.prototype.key        = function key(i){             debugger; return Object.keys(this)[i||0];} 
    Storage.prototype.removeItem = function removeItem(key){    debugger; delete this[key];}       
    Storage.prototype.setItem    = function setItem(key, val){  debugger; this[key] = (val === undefined)?null:String(val) }
    safefunction(Storage)
    _storage_obj = new Storage
    // window.localStorage
    make_constructor("localStorage", "Storage", EN, EN, _storage_obj)
    localStorage.__proto__["clear"]      = safefunction(localStorage.__proto__["clear"]);
    localStorage.__proto__["getItem"]    = safefunction(localStorage.__proto__["getItem"]);
    localStorage.__proto__["key"]        = safefunction(localStorage.__proto__["key"]);
    localStorage.__proto__["removeItem"] = safefunction(localStorage.__proto__["removeItem"]);
    localStorage.__proto__["setItem"]    = safefunction(localStorage.__proto__["setItem"]);
    localStorage["__#classType"] = "localStorage";
    Object.defineProperty(localStorage, 'length', { get: function(){ return Object.keys(this).length }, });
    // window.sessionStorage
    make_constructor("sessionStorage", "Storage", EN, EN, _storage_obj)
    sessionStorage.__proto__["clear"]      = safefunction(sessionStorage.__proto__["clear"]);
    sessionStorage.__proto__["getItem"]    = safefunction(sessionStorage.__proto__["getItem"]);
    sessionStorage.__proto__["key"]        = safefunction(sessionStorage.__proto__["key"]);
    sessionStorage.__proto__["removeItem"] = safefunction(sessionStorage.__proto__["removeItem"]);
    sessionStorage.__proto__["setItem"]    = safefunction(sessionStorage.__proto__["setItem"]);
    Object.defineProperty(sessionStorage, 'length', { get: function(){ return Object.keys(this).length }, });
    // navigator.connection
    make_constructor("_vconnect", "NetworkInformation", EN, EN)
    navigator.connection = _vconnect
    navigator.connection.__proto__["onchange"]            = null;
    navigator.connection.__proto__["effectiveType"]       = "4g";
    navigator.connection.__proto__["rtt"]                 = 50;
    navigator.connection.__proto__["downlink"]            = 10;
    navigator.connection.__proto__["saveData"]            = false;
    // window.performance
    make_constructor("performance", "Performance", EN, EN)
    Object.assign(performance, {
        "timeOrigin": 1619098076582.469,
        "timing": {
            "connectStart": 1619098076595,
            "navigationStart": 1619098076582,
            "loadEventEnd": 1619098077273,
            "domLoading": 1619098076680,
            "secureConnectionStart": 0,
            "fetchStart": 1619098076595,
            "domContentLoadedEventStart": 1619098077192,
            "responseStart": 1619098076668,
            "responseEnd": 1619098076878,
            "domInteractive": 1619098077163,
            "domainLookupEnd": 1619098076595,
            "redirectStart": 0,
            "requestStart": 1619098076602,
            "unloadEventEnd": 1619098076678,
            "unloadEventStart": 1619098076678,
            "domComplete": 1619098077272,
            "domainLookupStart": 1619098076595,
            "loadEventStart": 1619098077272,
            "domContentLoadedEventEnd": 1619098077196,
            "redirectEnd": 0,
            "connectEnd": 1619098076595
        },
        "navigation": {
            "type": 0,
            "redirectCount": 0
        }
    })
    make_constructor("_vtiming", "PerformanceTiming", EN, EN)
    make_constructor("_vnavigation", "PerformanceNavigation", EN, EN)
    performance['timing'] = Object.assign(_vtiming, performance['timing'])
    performance['navigation'] = Object.assign(_vnavigation, performance['navigation'])
    // window.indexedDB
    make_constructor("indexedDB", "IDBFactory", EN, EN)
    window.indexedDB.__proto__["cmp"]            = function cmp(){debugger;};            safefunction(window.indexedDB["cmp"]);
    window.indexedDB.__proto__["databases"]      = function databases(){debugger;};      safefunction(window.indexedDB["databases"]);
    window.indexedDB.__proto__["deleteDatabase"] = function deleteDatabase(){debugger;}; safefunction(window.indexedDB["deleteDatabase"]);
    window.indexedDB.__proto__["open"]           = function open(){debugger;};           safefunction(window.indexedDB["open"]);
    // window.XMLHttpRequest
    make_constructor("XMLHttpRequest", "XMLHttpRequest", EN, EN, undefined, { allow_illegal: true })
    XMLHttpRequest.prototype["UNSENT"]                = XMLHttpRequest["UNSENT"]                = 0;
    XMLHttpRequest.prototype["OPENED"]                = XMLHttpRequest["OPENED"]                = 1;
    XMLHttpRequest.prototype["HEADERS_RECEIVED"]      = XMLHttpRequest["HEADERS_RECEIVED"]      = 2;
    XMLHttpRequest.prototype["LOADING"]               = XMLHttpRequest["LOADING"]               = 3;
    XMLHttpRequest.prototype["DONE"]                  = XMLHttpRequest["DONE"]                  = 4;
    XMLHttpRequest.prototype["abort"]                 = function abort(){debugger;};                 safefunction(XMLHttpRequest.prototype["abort"]);
    XMLHttpRequest.prototype["getAllResponseHeaders"] = function getAllResponseHeaders(){debugger;}; safefunction(XMLHttpRequest.prototype["getAllResponseHeaders"]);
    XMLHttpRequest.prototype["getResponseHeader"]     = function getResponseHeader(){debugger;};     safefunction(XMLHttpRequest.prototype["getResponseHeader"]);
    XMLHttpRequest.prototype["open"]                  = function open(){debugger;};                  safefunction(XMLHttpRequest.prototype["open"]);
    XMLHttpRequest.prototype["overrideMimeType"]      = function overrideMimeType(){debugger;};      safefunction(XMLHttpRequest.prototype["overrideMimeType"]);
    XMLHttpRequest.prototype["send"]                  = function send(){debugger;};                  safefunction(XMLHttpRequest.prototype["send"]);
    XMLHttpRequest.prototype["setRequestHeader"]      = function setRequestHeader(){debugger;};      safefunction(XMLHttpRequest.prototype["setRequestHeader"]);

    // window.screen
    make_constructor("screen", "Screen", EN, EN)
    screen.__proto__["availWidth"]  = 1920;
    screen.__proto__["availHeight"] = 1040;
    screen.__proto__["width"]       = 1920;
    screen.__proto__["height"]      = 1080;
    screen.__proto__["colorDepth"]  = 24;
    screen.__proto__["pixelDepth"]  = 24;
    screen.__proto__["availLeft"]   = 0;
    screen.__proto__["availTop"]    = 0;
    screen.__proto__["orientation"] = new (class ScreenOrientation {});
    make_constructor("_vorientation", "ScreenOrientation", EN, EN)
    _vorientation.__proto__["angle"]               = 0;
    _vorientation.__proto__["type"]                = "landscape-primary";
    _vorientation.__proto__["onchange"]            = null;
    _vorientation.__proto__["lock"]                = function lock(){debugger;};                safefunction(_vorientation["lock"]);
    _vorientation.__proto__["unlock"]              = function unlock(){debugger;};              safefunction(_vorientation["unlock"]);
    _vorientation.__proto__["addEventListener"]    = function addEventListener(){debugger;};    safefunction(_vorientation["addEventListener"]);
    _vorientation.__proto__["dispatchEvent"]       = function dispatchEvent(){debugger;};       safefunction(_vorientation["dispatchEvent"]);
    _vorientation.__proto__["removeEventListener"] = function removeEventListener(){debugger;}; safefunction(_vorientation["removeEventListener"]);
    screen["orientation"] = _vorientation

    // 用于生成代码用，在环境中无影响，保留即可
    var nn = Object.keys(__cilame__['n'])
    var NN = Object.keys(__cilame__['N'])
    var AA = ['addEventListener', 'dispatchEvent', 'removeEventListener', 'clientInformation']
    return nn.concat(NN).concat(AA)
}
Cilame()



// console.log(localStorage)
// console.log(localStorage.length)
// console.log(localStorage.getItem("$_fb"))
// console.log(localStorage.removeItem("$_fb"))
// console.log(localStorage.getItem("$_fb"))
// console.log(localStorage)
// console.log(localStorage.setItem("$_fb", "hahaha"))
// console.log(localStorage.getItem("$_fb"))
// console.log(localStorage)







// sessionStorage.__proto__["length"]     = 2;
// sessionStorage.__proto__["clear"]      = function clear(){debugger;};      safefunction(sessionStorage.__proto__["clear"]);
// sessionStorage.__proto__["getItem"]    = function getItem(){debugger;};    safefunction(sessionStorage.__proto__["getItem"]);
// sessionStorage.__proto__["key"]        = function key(){debugger;};        safefunction(sessionStorage.__proto__["key"]);
// sessionStorage.__proto__["removeItem"] = function removeItem(){debugger;}; safefunction(sessionStorage.__proto__["removeItem"]);
// sessionStorage.__proto__["setItem"]    = function setItem(){debugger;};    safefunction(sessionStorage.__proto__["setItem"]);
// sessionStorage["$_cDro"] = "1";
// sessionStorage["$_YWTU"] = "FEQUsSBVzv0QWk6YXiwmU1rTQu5fgYnAS0QCjp2noTZ";



















// console.log(1,window)
// console.log(1,window.constructor)
// console.log(2,window.__proto__)
// console.log(2,window.__proto__.constructor)
// console.log(3,window.__proto__.__proto__)
// console.log(3,window.__proto__.__proto__.constructor)
// console.log(4,window.__proto__.__proto__.__proto__)
// console.log(4,window.__proto__.__proto__.__proto__.constructor)
// console.log()
// console.log(5,navigator)
// console.log(5,navigator.constructor)
// console.log(6,navigator.__proto__)
// console.log(6,navigator.__proto__.constructor)
// console.log(7,navigator.__proto__.__proto__)
// console.log(7,navigator.__proto__.__proto__.constructor)
// console.log()
// console.log(7,document)
// console.log(7,document.constructor)
// console.log(8,document.__proto__)
// console.log(8,document.__proto__.constructor)
// console.log(9,document.__proto__.__proto__)
// console.log(9,document.__proto__.__proto__.constructor)
// console.log(10,document.__proto__.__proto__.__proto__)
// console.log(10,document.__proto__.__proto__.__proto__.constructor)
// console.log(11,document.__proto__.__proto__.__proto__.__proto__)
// console.log(11,document.__proto__.__proto__.__proto__.__proto__.constructor)






















window.__proto__["TEMPORARY"]  = 0;
window.__proto__["PERSISTENT"] = 1;
window["self"]                            = window;
window["name"]                            = "$_YWTU=FEQUsSBVzv0QWk6YXiwmU1rTQu5fgYnAS0QCjp2noTZ&$_cDro=1&vdFm=";
window["customElements"]                  = new (class CustomElementRegistry {});
window["history"]                         = new (class History {});
window["locationbar"]                     = new (class BarProp {});
window["menubar"]                         = new (class BarProp {});
window["personalbar"]                     = new (class BarProp {});
window["scrollbars"]                      = new (class BarProp {});
window["statusbar"]                       = new (class BarProp {});
window["toolbar"]                         = new (class BarProp {});
window["status"]                          = "";
window["closed"]                          = false;
window["frames"]                          = window;
window["length"]                          = 0;
window["top"]                             = window;
window["opener"]                          = null;
window["parent"]                          = window;
window["frameElement"]                    = null;
window["origin"]                          = "http://app1.nmpa.gov.cn";
window["external"]                        = new (class External {});
window["innerWidth"]                      = 1920;
window["innerHeight"]                     = 969;
window["scrollX"]                         = 0;
window["pageXOffset"]                     = 0;
window["scrollY"]                         = 0;
window["pageYOffset"]                     = 0;
window["visualViewport"]                  = new (class VisualViewport {});
window["screenX"]                         = 0;
window["screenY"]                         = 0;
window["outerWidth"]                      = 1920;
window["outerHeight"]                     = 1040;
window["devicePixelRatio"]                = 1;
window["screenLeft"]                      = 0;
window["screenTop"]                       = 0;
window["defaultStatus"]                   = "";
window["defaultstatus"]                   = "";
window["styleMedia"]                      = new (class Object {});
window["onsearch"]                        = null;
window["isSecureContext"]                 = false;
window["onappinstalled"]                  = null;
window["onbeforeinstallprompt"]           = null;
window["crypto"]                          = new (class Crypto {});
window["webkitStorageInfo"]               = new (class Object {});
window["onabort"]                         = null;
window["onblur"]                          = null;
window["oncancel"]                        = null;
window["oncanplay"]                       = null;
window["oncanplaythrough"]                = null;
window["onchange"]                        = null;
window["onclick"]                         = null;
window["onclose"]                         = null;
window["oncontextmenu"]                   = null;
window["oncuechange"]                     = null;
window["ondblclick"]                      = null;
window["ondrag"]                          = null;
window["ondragend"]                       = null;
window["ondragenter"]                     = null;
window["ondragleave"]                     = null;
window["ondragover"]                      = null;
window["ondragstart"]                     = null;
window["ondrop"]                          = null;
window["ondurationchange"]                = null;
window["onemptied"]                       = null;
window["onended"]                         = null;
window["onerror"]                         = null;
window["onfocus"]                         = null;
window["onformdata"]                      = null;
window["oninput"]                         = null;
window["oninvalid"]                       = null;
window["onkeydown"]                       = null;
window["onkeypress"]                      = null;
window["onkeyup"]                         = null;
window["onload"]                          = null;
window["onloadeddata"]                    = null;
window["onloadedmetadata"]                = null;
window["onloadstart"]                     = null;
window["onmousedown"]                     = null;
window["onmouseenter"]                    = null;
window["onmouseleave"]                    = null;
window["onmousemove"]                     = null;
window["onmouseout"]                      = null;
window["onmouseover"]                     = null;
window["onmouseup"]                       = null;
window["onmousewheel"]                    = null;
window["onpause"]                         = null;
window["onplay"]                          = null;
window["onplaying"]                       = null;
window["onprogress"]                      = null;
window["onratechange"]                    = null;
window["onreset"]                         = null;
window["onresize"]                        = null;
window["onscroll"]                        = null;
window["onseeked"]                        = null;
window["onseeking"]                       = null;
window["onselect"]                        = null;
window["onstalled"]                       = null;
window["onsubmit"]                        = null;
window["onsuspend"]                       = null;
window["ontimeupdate"]                    = null;
window["ontoggle"]                        = null;
window["onvolumechange"]                  = null;
window["onwaiting"]                       = null;
window["onwebkitanimationend"]            = null;
window["onwebkitanimationiteration"]      = null;
window["onwebkitanimationstart"]          = null;
window["onwebkittransitionend"]           = null;
window["onwheel"]                         = null;
window["onauxclick"]                      = null;
window["ongotpointercapture"]             = null;
window["onlostpointercapture"]            = null;
window["onpointerdown"]                   = null;
window["onpointermove"]                   = null;
window["onpointerup"]                     = null;
window["onpointercancel"]                 = null;
window["onpointerover"]                   = null;
window["onpointerout"]                    = null;
window["onpointerenter"]                  = null;
window["onpointerleave"]                  = null;
window["onselectstart"]                   = null;
window["onselectionchange"]               = null;
window["onanimationend"]                  = null;
window["onanimationiteration"]            = null;
window["onanimationstart"]                = null;
window["ontransitionrun"]                 = null;
window["ontransitionstart"]               = null;
window["ontransitionend"]                 = null;
window["ontransitioncancel"]              = null;
window["onafterprint"]                    = null;
window["onbeforeprint"]                   = null;
window["onbeforeunload"]                  = null;
window["onhashchange"]                    = null;
window["onlanguagechange"]                = null;
window["onmessage"]                       = null;
window["onmessageerror"]                  = null;
window["onoffline"]                       = null;
window["ononline"]                        = null;
window["onpagehide"]                      = null;
window["onpageshow"]                      = null;
window["onpopstate"]                      = null;
window["onrejectionhandled"]              = null;
window["onstorage"]                       = null;
window["onunhandledrejection"]            = null;
window["onunload"]                        = null;
window["alert"]                           = function alert(){debugger;};                           safefunction(window["alert"]);
window["atob"]                            = function atob(){debugger;};                            safefunction(window["atob"]);
window["blur"]                            = function blur(){debugger;};                            safefunction(window["blur"]);
window["btoa"]                            = function btoa(){debugger;};                            safefunction(window["btoa"]);
window["cancelAnimationFrame"]            = function cancelAnimationFrame(){debugger;};            safefunction(window["cancelAnimationFrame"]);
window["cancelIdleCallback"]              = function cancelIdleCallback(){debugger;};              safefunction(window["cancelIdleCallback"]);
window["captureEvents"]                   = function captureEvents(){debugger;};                   safefunction(window["captureEvents"]);
window["clearInterval"]                   = function clearInterval(){debugger;};                   safefunction(window["clearInterval"]);
window["clearTimeout"]                    = function clearTimeout(){debugger;};                    safefunction(window["clearTimeout"]);
window["close"]                           = function close(){debugger;};                           safefunction(window["close"]);
window["confirm"]                         = function confirm(){debugger;};                         safefunction(window["confirm"]);
window["createImageBitmap"]               = function createImageBitmap(){debugger;};               safefunction(window["createImageBitmap"]);
window["fetch"]                           = function fetch(){debugger;};                           safefunction(window["fetch"]);
window["find"]                            = function find(){debugger;};                            safefunction(window["find"]);
window["focus"]                           = function focus(){debugger;};                           safefunction(window["focus"]);
window["getComputedStyle"]                = function getComputedStyle(){debugger;};                safefunction(window["getComputedStyle"]);
window["getSelection"]                    = function getSelection(){debugger;};                    safefunction(window["getSelection"]);
window["matchMedia"]                      = function matchMedia(){debugger;};                      safefunction(window["matchMedia"]);
window["moveBy"]                          = function moveBy(){debugger;};                          safefunction(window["moveBy"]);
window["moveTo"]                          = function moveTo(){debugger;};                          safefunction(window["moveTo"]);
window["open"]                            = function open(){debugger;};                            safefunction(window["open"]);
window["postMessage"]                     = function postMessage(){debugger;};                     safefunction(window["postMessage"]);
window["print"]                           = function print(){debugger;};                           safefunction(window["print"]);
window["prompt"]                          = function prompt(){debugger;};                          safefunction(window["prompt"]);
window["queueMicrotask"]                  = function queueMicrotask(){debugger;};                  safefunction(window["queueMicrotask"]);
window["releaseEvents"]                   = function releaseEvents(){debugger;};                   safefunction(window["releaseEvents"]);
window["requestAnimationFrame"]           = function requestAnimationFrame(){debugger;};           safefunction(window["requestAnimationFrame"]);
window["requestIdleCallback"]             = function requestIdleCallback(){debugger;};             safefunction(window["requestIdleCallback"]);
window["resizeBy"]                        = function resizeBy(){debugger;};                        safefunction(window["resizeBy"]);
window["resizeTo"]                        = function resizeTo(){debugger;};                        safefunction(window["resizeTo"]);
window["scroll"]                          = function scroll(){debugger;};                          safefunction(window["scroll"]);
window["scrollBy"]                        = function scrollBy(){debugger;};                        safefunction(window["scrollBy"]);
window["scrollTo"]                        = function scrollTo(){debugger;};                        safefunction(window["scrollTo"]);
window["setInterval"]                     = function setInterval(){debugger;};                     safefunction(window["setInterval"]);
window["setTimeout"]                      = function setTimeout(){debugger;};                      safefunction(window["setTimeout"]);
window["stop"]                            = function stop(){debugger;};                            safefunction(window["stop"]);
window["webkitCancelAnimationFrame"]      = function webkitCancelAnimationFrame(){debugger;};      safefunction(window["webkitCancelAnimationFrame"]);
window["webkitRequestAnimationFrame"]     = function webkitRequestAnimationFrame(){debugger;};     safefunction(window["webkitRequestAnimationFrame"]);
window["chrome"]                          = new (class Object {});
window["speechSynthesis"]                 = new (class EventTarget {});
window["originAgentCluster"]              = false;
window["onpointerrawupdate"]              = null;
window["trustedTypes"]                    = new (class TrustedTypePolicyFactory {});
window["crossOriginIsolated"]             = false;
window["openDatabase"]                    = function openDatabase(){debugger;};                    safefunction(window["openDatabase"]);
window["webkitRequestFileSystem"]         = function webkitRequestFileSystem(){debugger;};         safefunction(window["webkitRequestFileSystem"]);
window["webkitResolveLocalFileSystemURL"] = function webkitResolveLocalFileSystemURL(){debugger;}; safefunction(window["webkitResolveLocalFileSystemURL"]);
window["generatecode4v"]                  = function generatecode4v(){debugger;};                  safefunction(window["generatecode4v"]);
window["generatecode4v1"]                 = function generatecode4v1(){debugger;};                 safefunction(window["generatecode4v1"]);
window["generate4example"]                = function generate4example(){debugger;};                safefunction(window["generate4example"]);
window["generate4Prototype"]              = function generate4Prototype(){debugger;};              safefunction(window["generate4Prototype"]);
window["alignment"]                       = function alignment(){debugger;};                       safefunction(window["alignment"]);
window["alignment_safefunction"]          = function alignment_safefunction(){debugger;};          safefunction(window["alignment_safefunction"]);
window["vall"]                            = function vall(){debugger;};                            safefunction(window["vall"]);
document.__proto__["implementation"]                            = new (class DOMImplementation {});
document.__proto__["URL"]                                       = "http://app1.nmpa.gov.cn/data_nmpa/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=152904713761213296322795806604&CbSlDlH0=qGc5kacU2y8U2y8U2enJaDCR.TmXaHUY4V.RdcrvZCQqqxQ";
document.__proto__["documentURI"]                               = "http://app1.nmpa.gov.cn/data_nmpa/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=152904713761213296322795806604&CbSlDlH0=qGc5kacU2y8U2y8U2enJaDCR.TmXaHUY4V.RdcrvZCQqqxQ";
document.__proto__["compatMode"]                                = "CSS1Compat";
document.__proto__["characterSet"]                              = "GBK";
document.__proto__["charset"]                                   = "GBK";
document.__proto__["inputEncoding"]                             = "GBK";
document.__proto__["contentType"]                               = "text/html";
document.__proto__["doctype"]                                   = new (class DocumentType {});
document.__proto__["documentElement"]                           = new (class HTMLHtmlElement {});
document.__proto__["xmlEncoding"]                               = null;
document.__proto__["xmlVersion"]                                = null;
document.__proto__["xmlStandalone"]                             = false;
document.__proto__["domain"]                                    = "app1.nmpa.gov.cn";
document.__proto__["referrer"]                                  = "http://app1.nmpa.gov.cn/data_nmpa/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=152904713761213296322795806604";
document.__proto__["lastModified"]                              = "04/22/2021 22:43:06";
document.__proto__["readyState"]                                = "loading";
document.__proto__["title"]                                     = "国家药品监督管理局--数据查询";
document.__proto__["dir"]                                       = "";
document.__proto__["body"]                                      = null;
document.__proto__["head"]                                      = new (class HTMLHeadElement {});
document.__proto__["images"]                                    = new (class HTMLCollection {});
document.__proto__["embeds"]                                    = new (class HTMLCollection {});
document.__proto__["plugins"]                                   = new (class HTMLCollection {});
document.__proto__["links"]                                     = new (class HTMLCollection {});
document.__proto__["forms"]                                     = new (class HTMLCollection {});
document.__proto__["scripts"]                                   = new (class HTMLCollection {});
document.__proto__["currentScript"]                             = null;
document.__proto__["defaultView"]                               = new (class Window {});
document.__proto__["designMode"]                                = "off";
document.__proto__["onreadystatechange"]                        = null;
document.__proto__["anchors"]                                   = new (class HTMLCollection {});
document.__proto__["applets"]                                   = new (class HTMLCollection {});
document.__proto__["fgColor"]                                   = "";
document.__proto__["linkColor"]                                 = "";
document.__proto__["vlinkColor"]                                = "";
document.__proto__["alinkColor"]                                = "";
document.__proto__["bgColor"]                                   = "";
document.__proto__["all"]                                       = undefined;
document.__proto__["scrollingElement"]                          = new (class HTMLHtmlElement {});
document.__proto__["onpointerlockchange"]                       = null;
document.__proto__["onpointerlockerror"]                        = null;
document.__proto__["hidden"]                                    = true;
document.__proto__["visibilityState"]                           = "hidden";
document.__proto__["wasDiscarded"]                              = false;
document.__proto__["featurePolicy"]                             = new (class FeaturePolicy {});
document.__proto__["webkitVisibilityState"]                     = "hidden";
document.__proto__["webkitHidden"]                              = true;
document.__proto__["onbeforecopy"]                              = null;
document.__proto__["onbeforecut"]                               = null;
document.__proto__["onbeforepaste"]                             = null;
document.__proto__["onfreeze"]                                  = null;
document.__proto__["onresume"]                                  = null;
document.__proto__["onsearch"]                                  = null;
document.__proto__["onsecuritypolicyviolation"]                 = null;
document.__proto__["onvisibilitychange"]                        = null;
document.__proto__["fullscreenEnabled"]                         = true;
document.__proto__["fullscreen"]                                = false;
document.__proto__["onfullscreenchange"]                        = null;
document.__proto__["onfullscreenerror"]                         = null;
document.__proto__["webkitIsFullScreen"]                        = false;
document.__proto__["webkitCurrentFullScreenElement"]            = null;
document.__proto__["webkitFullscreenEnabled"]                   = true;
document.__proto__["webkitFullscreenElement"]                   = null;
document.__proto__["onwebkitfullscreenchange"]                  = null;
document.__proto__["onwebkitfullscreenerror"]                   = null;
document.__proto__["rootElement"]                               = null;
document.__proto__["onabort"]                                   = null;
document.__proto__["onblur"]                                    = null;
document.__proto__["oncancel"]                                  = null;
document.__proto__["oncanplay"]                                 = null;
document.__proto__["oncanplaythrough"]                          = null;
document.__proto__["onchange"]                                  = null;
document.__proto__["onclick"]                                   = null;
document.__proto__["onclose"]                                   = null;
document.__proto__["oncontextmenu"]                             = null;
document.__proto__["oncuechange"]                               = null;
document.__proto__["ondblclick"]                                = null;
document.__proto__["ondrag"]                                    = null;
document.__proto__["ondragend"]                                 = null;
document.__proto__["ondragenter"]                               = null;
document.__proto__["ondragleave"]                               = null;
document.__proto__["ondragover"]                                = null;
document.__proto__["ondragstart"]                               = null;
document.__proto__["ondrop"]                                    = null;
document.__proto__["ondurationchange"]                          = null;
document.__proto__["onemptied"]                                 = null;
document.__proto__["onended"]                                   = null;
document.__proto__["onerror"]                                   = null;
document.__proto__["onfocus"]                                   = null;
document.__proto__["onformdata"]                                = null;
document.__proto__["oninput"]                                   = null;
document.__proto__["oninvalid"]                                 = null;
document.__proto__["onkeydown"]                                 = null;
document.__proto__["onkeypress"]                                = null;
document.__proto__["onkeyup"]                                   = null;
document.__proto__["onload"]                                    = null;
document.__proto__["onloadeddata"]                              = null;
document.__proto__["onloadedmetadata"]                          = null;
document.__proto__["onloadstart"]                               = null;
document.__proto__["onmousedown"]                               = null;
document.__proto__["onmouseenter"]                              = null;
document.__proto__["onmouseleave"]                              = null;
document.__proto__["onmousemove"]                               = null;
document.__proto__["onmouseout"]                                = null;
document.__proto__["onmouseover"]                               = null;
document.__proto__["onmouseup"]                                 = null;
document.__proto__["onmousewheel"]                              = null;
document.__proto__["onpause"]                                   = null;
document.__proto__["onplay"]                                    = null;
document.__proto__["onplaying"]                                 = null;
document.__proto__["onprogress"]                                = null;
document.__proto__["onratechange"]                              = null;
document.__proto__["onreset"]                                   = null;
document.__proto__["onresize"]                                  = null;
document.__proto__["onscroll"]                                  = null;
document.__proto__["onseeked"]                                  = null;
document.__proto__["onseeking"]                                 = null;
document.__proto__["onselect"]                                  = null;
document.__proto__["onstalled"]                                 = null;
document.__proto__["onsubmit"]                                  = null;
document.__proto__["onsuspend"]                                 = null;
document.__proto__["ontimeupdate"]                              = null;
document.__proto__["ontoggle"]                                  = null;
document.__proto__["onvolumechange"]                            = null;
document.__proto__["onwaiting"]                                 = null;
document.__proto__["onwebkitanimationend"]                      = null;
document.__proto__["onwebkitanimationiteration"]                = null;
document.__proto__["onwebkitanimationstart"]                    = null;
document.__proto__["onwebkittransitionend"]                     = null;
document.__proto__["onwheel"]                                   = null;
document.__proto__["onauxclick"]                                = null;
document.__proto__["ongotpointercapture"]                       = null;
document.__proto__["onlostpointercapture"]                      = null;
document.__proto__["onpointerdown"]                             = null;
document.__proto__["onpointermove"]                             = null;
document.__proto__["onpointerup"]                               = null;
document.__proto__["onpointercancel"]                           = null;
document.__proto__["onpointerover"]                             = null;
document.__proto__["onpointerout"]                              = null;
document.__proto__["onpointerenter"]                            = null;
document.__proto__["onpointerleave"]                            = null;
document.__proto__["onselectstart"]                             = null;
document.__proto__["onselectionchange"]                         = null;
document.__proto__["onanimationend"]                            = null;
document.__proto__["onanimationiteration"]                      = null;
document.__proto__["onanimationstart"]                          = null;
document.__proto__["ontransitionrun"]                           = null;
document.__proto__["ontransitionstart"]                         = null;
document.__proto__["ontransitionend"]                           = null;
document.__proto__["ontransitioncancel"]                        = null;
document.__proto__["oncopy"]                                    = null;
document.__proto__["oncut"]                                     = null;
document.__proto__["onpaste"]                                   = null;
document.__proto__["children"]                                  = new (class HTMLCollection {});
document.__proto__["firstElementChild"]                         = new (class HTMLHtmlElement {});
document.__proto__["lastElementChild"]                          = new (class HTMLHtmlElement {});
document.__proto__["childElementCount"]                         = 1;
document.__proto__["activeElement"]                             = null;
document.__proto__["styleSheets"]                               = new (class StyleSheetList {});
document.__proto__["pointerLockElement"]                        = null;
document.__proto__["fullscreenElement"]                         = null;
document.__proto__["adoptedStyleSheets"]                        = new (class Array {});
document.__proto__["fonts"]                                     = new (class EventTarget {});
document.__proto__["adoptNode"]                                 = function adoptNode(){debugger;};                   safefunction(document["adoptNode"]);
document.__proto__["append"]                                    = function append(){debugger;};                      safefunction(document["append"]);
document.__proto__["captureEvents"]                             = function captureEvents(){debugger;};               safefunction(document["captureEvents"]);
document.__proto__["caretRangeFromPoint"]                       = function caretRangeFromPoint(){debugger;};         safefunction(document["caretRangeFromPoint"]);
document.__proto__["clear"]                                     = function clear(){debugger;};                       safefunction(document["clear"]);
document.__proto__["close"]                                     = function close(){debugger;};                       safefunction(document["close"]);
document.__proto__["createAttribute"]                           = function createAttribute(){debugger;};             safefunction(document["createAttribute"]);
document.__proto__["createAttributeNS"]                         = function createAttributeNS(){debugger;};           safefunction(document["createAttributeNS"]);
document.__proto__["createCDATASection"]                        = function createCDATASection(){debugger;};          safefunction(document["createCDATASection"]);
document.__proto__["createComment"]                             = function createComment(){debugger;};               safefunction(document["createComment"]);
document.__proto__["createDocumentFragment"]                    = function createDocumentFragment(){debugger;};      safefunction(document["createDocumentFragment"]);
document.__proto__["createElement"]                             = function createElement(){debugger;};               safefunction(document["createElement"]);
document.__proto__["createElementNS"]                           = function createElementNS(){debugger;};             safefunction(document["createElementNS"]);
document.__proto__["createEvent"]                               = function createEvent(){debugger;};                 safefunction(document["createEvent"]);
document.__proto__["createExpression"]                          = function createExpression(){debugger;};            safefunction(document["createExpression"]);
document.__proto__["createNSResolver"]                          = function createNSResolver(){debugger;};            safefunction(document["createNSResolver"]);
document.__proto__["createNodeIterator"]                        = function createNodeIterator(){debugger;};          safefunction(document["createNodeIterator"]);
document.__proto__["createProcessingInstruction"]               = function createProcessingInstruction(){debugger;}; safefunction(document["createProcessingInstruction"]);
document.__proto__["createRange"]                               = function createRange(){debugger;};                 safefunction(document["createRange"]);
document.__proto__["createTextNode"]                            = function createTextNode(){debugger;};              safefunction(document["createTextNode"]);
document.__proto__["createTreeWalker"]                          = function createTreeWalker(){debugger;};            safefunction(document["createTreeWalker"]);
document.__proto__["elementFromPoint"]                          = function elementFromPoint(){debugger;};            safefunction(document["elementFromPoint"]);
document.__proto__["elementsFromPoint"]                         = function elementsFromPoint(){debugger;};           safefunction(document["elementsFromPoint"]);
document.__proto__["evaluate"]                                  = function evaluate(){debugger;};                    safefunction(document["evaluate"]);
document.__proto__["execCommand"]                               = function execCommand(){debugger;};                 safefunction(document["execCommand"]);
document.__proto__["exitFullscreen"]                            = function exitFullscreen(){debugger;};              safefunction(document["exitFullscreen"]);
document.__proto__["exitPointerLock"]                           = function exitPointerLock(){debugger;};             safefunction(document["exitPointerLock"]);
document.__proto__["getElementById"]                            = function getElementById(){debugger;};              safefunction(document["getElementById"]);
document.__proto__["getElementsByClassName"]                    = function getElementsByClassName(){debugger;};      safefunction(document["getElementsByClassName"]);
document.__proto__["getElementsByName"]                         = function getElementsByName(){debugger;};           safefunction(document["getElementsByName"]);
document.__proto__["getElementsByTagName"]                      = function getElementsByTagName(){debugger;};        safefunction(document["getElementsByTagName"]);
document.__proto__["getElementsByTagNameNS"]                    = function getElementsByTagNameNS(){debugger;};      safefunction(document["getElementsByTagNameNS"]);
document.__proto__["getSelection"]                              = function getSelection(){debugger;};                safefunction(document["getSelection"]);
document.__proto__["hasFocus"]                                  = function hasFocus(){debugger;};                    safefunction(document["hasFocus"]);
document.__proto__["importNode"]                                = function importNode(){debugger;};                  safefunction(document["importNode"]);
document.__proto__["open"]                                      = function open(){debugger;};                        safefunction(document["open"]);
document.__proto__["prepend"]                                   = function prepend(){debugger;};                     safefunction(document["prepend"]);
document.__proto__["queryCommandEnabled"]                       = function queryCommandEnabled(){debugger;};         safefunction(document["queryCommandEnabled"]);
document.__proto__["queryCommandIndeterm"]                      = function queryCommandIndeterm(){debugger;};        safefunction(document["queryCommandIndeterm"]);
document.__proto__["queryCommandState"]                         = function queryCommandState(){debugger;};           safefunction(document["queryCommandState"]);
document.__proto__["queryCommandSupported"]                     = function queryCommandSupported(){debugger;};       safefunction(document["queryCommandSupported"]);
document.__proto__["queryCommandValue"]                         = function queryCommandValue(){debugger;};           safefunction(document["queryCommandValue"]);
document.__proto__["querySelector"]                             = function querySelector(){debugger;};               safefunction(document["querySelector"]);
document.__proto__["querySelectorAll"]                          = function querySelectorAll(){debugger;};            safefunction(document["querySelectorAll"]);
document.__proto__["releaseEvents"]                             = function releaseEvents(){debugger;};               safefunction(document["releaseEvents"]);
document.__proto__["webkitCancelFullScreen"]                    = function webkitCancelFullScreen(){debugger;};      safefunction(document["webkitCancelFullScreen"]);
document.__proto__["webkitExitFullscreen"]                      = function webkitExitFullscreen(){debugger;};        safefunction(document["webkitExitFullscreen"]);
document.__proto__["write"]                                     = function write(){debugger;};                       safefunction(document["write"]);
document.__proto__["writeln"]                                   = function writeln(){debugger;};                     safefunction(document["writeln"]);
document.__proto__["fragmentDirective"]                         = new (class FragmentDirective {});
document.__proto__["onpointerrawupdate"]                        = null;
document.__proto__["timeline"]                                  = new (class DocumentTimeline {});
document.__proto__["pictureInPictureEnabled"]                   = true;
document.__proto__["pictureInPictureElement"]                   = null;
document.__proto__["getAnimations"]                             = function getAnimations(){debugger;};               safefunction(document["getAnimations"]);
document.__proto__["exitPictureInPicture"]                      = function exitPictureInPicture(){debugger;};        safefunction(document["exitPictureInPicture"]);
document.__proto__["replaceChildren"]                           = function replaceChildren(){debugger;};             safefunction(document["replaceChildren"]);
document.__proto__["nodeType"]                                  = 9;
document.__proto__["nodeName"]                                  = "#document";
document.__proto__["baseURI"]                                   = "http://app1.nmpa.gov.cn/data_nmpa/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=152904713761213296322795806604&CbSlDlH0=qGc5kacU2y8U2y8U2enJaDCR.TmXaHUY4V.RdcrvZCQqqxQ";
document.__proto__["isConnected"]                               = true;
document.__proto__["ownerDocument"]                             = null;
document.__proto__["parentNode"]                                = null;
document.__proto__["parentElement"]                             = null;
document.__proto__["childNodes"]                                = new (class NodeList {});
document.__proto__["firstChild"]                                = new (class DocumentType {});
document.__proto__["lastChild"]                                 = new (class HTMLHtmlElement {});
document.__proto__["previousSibling"]                           = null;
document.__proto__["nextSibling"]                               = null;
document.__proto__["nodeValue"]                                 = null;
document.__proto__["textContent"]                               = null;
document.__proto__["ELEMENT_NODE"]                              = 1;
document.__proto__["ATTRIBUTE_NODE"]                            = 2;
document.__proto__["TEXT_NODE"]                                 = 3;
document.__proto__["CDATA_SECTION_NODE"]                        = 4;
document.__proto__["ENTITY_REFERENCE_NODE"]                     = 5;
document.__proto__["ENTITY_NODE"]                               = 6;
document.__proto__["PROCESSING_INSTRUCTION_NODE"]               = 7;
document.__proto__["COMMENT_NODE"]                              = 8;
document.__proto__["DOCUMENT_NODE"]                             = 9;
document.__proto__["DOCUMENT_TYPE_NODE"]                        = 10;
document.__proto__["DOCUMENT_FRAGMENT_NODE"]                    = 11;
document.__proto__["NOTATION_NODE"]                             = 12;
document.__proto__["DOCUMENT_POSITION_DISCONNECTED"]            = 1;
document.__proto__["DOCUMENT_POSITION_PRECEDING"]               = 2;
document.__proto__["DOCUMENT_POSITION_FOLLOWING"]               = 4;
document.__proto__["DOCUMENT_POSITION_CONTAINS"]                = 8;
document.__proto__["DOCUMENT_POSITION_CONTAINED_BY"]            = 16;
document.__proto__["DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC"] = 32;
document.__proto__["appendChild"]                               = function appendChild(){debugger;};                 safefunction(document["appendChild"]);
document.__proto__["cloneNode"]                                 = function cloneNode(){debugger;};                   safefunction(document["cloneNode"]);
document.__proto__["compareDocumentPosition"]                   = function compareDocumentPosition(){debugger;};     safefunction(document["compareDocumentPosition"]);
document.__proto__["contains"]                                  = function contains(){debugger;};                    safefunction(document["contains"]);
document.__proto__["getRootNode"]                               = function getRootNode(){debugger;};                 safefunction(document["getRootNode"]);
document.__proto__["hasChildNodes"]                             = function hasChildNodes(){debugger;};               safefunction(document["hasChildNodes"]);
document.__proto__["insertBefore"]                              = function insertBefore(){debugger;};                safefunction(document["insertBefore"]);
document.__proto__["isDefaultNamespace"]                        = function isDefaultNamespace(){debugger;};          safefunction(document["isDefaultNamespace"]);
document.__proto__["isEqualNode"]                               = function isEqualNode(){debugger;};                 safefunction(document["isEqualNode"]);
document.__proto__["isSameNode"]                                = function isSameNode(){debugger;};                  safefunction(document["isSameNode"]);
document.__proto__["lookupNamespaceURI"]                        = function lookupNamespaceURI(){debugger;};          safefunction(document["lookupNamespaceURI"]);
document.__proto__["lookupPrefix"]                              = function lookupPrefix(){debugger;};                safefunction(document["lookupPrefix"]);
document.__proto__["normalize"]                                 = function normalize(){debugger;};                   safefunction(document["normalize"]);
document.__proto__["removeChild"]                               = function removeChild(){debugger;};                 safefunction(document["removeChild"]);
document.__proto__["replaceChild"]                              = function replaceChild(){debugger;};                safefunction(document["replaceChild"]);
document["location"] = new (class Location {});
Node.prototype["ELEMENT_NODE"]                              = 1;
Node.prototype["ATTRIBUTE_NODE"]                            = 2;
Node.prototype["TEXT_NODE"]                                 = 3;
Node.prototype["CDATA_SECTION_NODE"]                        = 4;
Node.prototype["ENTITY_REFERENCE_NODE"]                     = 5;
Node.prototype["ENTITY_NODE"]                               = 6;
Node.prototype["PROCESSING_INSTRUCTION_NODE"]               = 7;
Node.prototype["COMMENT_NODE"]                              = 8;
Node.prototype["DOCUMENT_NODE"]                             = 9;
Node.prototype["DOCUMENT_TYPE_NODE"]                        = 10;
Node.prototype["DOCUMENT_FRAGMENT_NODE"]                    = 11;
Node.prototype["NOTATION_NODE"]                             = 12;
Node.prototype["DOCUMENT_POSITION_DISCONNECTED"]            = 1;
Node.prototype["DOCUMENT_POSITION_PRECEDING"]               = 2;
Node.prototype["DOCUMENT_POSITION_FOLLOWING"]               = 4;
Node.prototype["DOCUMENT_POSITION_CONTAINS"]                = 8;
Node.prototype["DOCUMENT_POSITION_CONTAINED_BY"]            = 16;
Node.prototype["DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC"] = 32;
Node.prototype["appendChild"]                               = function appendChild(){debugger;};             safefunction(Node.prototype["appendChild"]);
Node.prototype["cloneNode"]                                 = function cloneNode(){debugger;};               safefunction(Node.prototype["cloneNode"]);
Node.prototype["compareDocumentPosition"]                   = function compareDocumentPosition(){debugger;}; safefunction(Node.prototype["compareDocumentPosition"]);
Node.prototype["contains"]                                  = function contains(){debugger;};                safefunction(Node.prototype["contains"]);
Node.prototype["getRootNode"]                               = function getRootNode(){debugger;};             safefunction(Node.prototype["getRootNode"]);
Node.prototype["hasChildNodes"]                             = function hasChildNodes(){debugger;};           safefunction(Node.prototype["hasChildNodes"]);
Node.prototype["insertBefore"]                              = function insertBefore(){debugger;};            safefunction(Node.prototype["insertBefore"]);
Node.prototype["isDefaultNamespace"]                        = function isDefaultNamespace(){debugger;};      safefunction(Node.prototype["isDefaultNamespace"]);
Node.prototype["isEqualNode"]                               = function isEqualNode(){debugger;};             safefunction(Node.prototype["isEqualNode"]);
Node.prototype["isSameNode"]                                = function isSameNode(){debugger;};              safefunction(Node.prototype["isSameNode"]);
Node.prototype["lookupNamespaceURI"]                        = function lookupNamespaceURI(){debugger;};      safefunction(Node.prototype["lookupNamespaceURI"]);
Node.prototype["lookupPrefix"]                              = function lookupPrefix(){debugger;};            safefunction(Node.prototype["lookupPrefix"]);
Node.prototype["normalize"]                                 = function normalize(){debugger;};               safefunction(Node.prototype["normalize"]);
Node.prototype["removeChild"]                               = function removeChild(){debugger;};             safefunction(Node.prototype["removeChild"]);
Node.prototype["replaceChild"]                              = function replaceChild(){debugger;};            safefunction(Node.prototype["replaceChild"]);
navigator.__proto__["vendorSub"]               = "";
navigator.__proto__["productSub"]              = "20030107";
navigator.__proto__["vendor"]                  = "Google Inc.";
navigator.__proto__["maxTouchPoints"]          = 0;
navigator.__proto__["userActivation"]          = new (class UserActivation {});
navigator.__proto__["doNotTrack"]              = null;
navigator.__proto__["geolocation"]             = new (class Geolocation {});
navigator.__proto__["plugins"]                 = new (class PluginArray {});
navigator.__proto__["mimeTypes"]               = new (class MimeTypeArray {});
navigator.__proto__["webkitTemporaryStorage"]  = new (class Object {});
navigator.__proto__["webkitPersistentStorage"] = new (class Object {});
navigator.__proto__["hardwareConcurrency"]     = 8;
navigator.__proto__["cookieEnabled"]           = true;
navigator.__proto__["appCodeName"]             = "Mozilla";
navigator.__proto__["appName"]                 = "Netscape";
navigator.__proto__["appVersion"]              = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36";
navigator.__proto__["platform"]                = "Win32";
navigator.__proto__["product"]                 = "Gecko";
navigator.__proto__["userAgent"]               = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36";
navigator.__proto__["language"]                = "zh-CN";
navigator.__proto__["languages"]               = ["zh-CN","zh"];
navigator.__proto__["onLine"]                  = true;
navigator.__proto__["webdriver"]               = false;
navigator.__proto__["getBattery"]              = function getBattery(){debugger;};  safefunction(navigator["getBattery"]);
navigator.__proto__["getGamepads"]             = function getGamepads(){debugger;}; safefunction(navigator["getGamepads"]);
navigator.__proto__["javaEnabled"]             = function javaEnabled(){debugger;}; safefunction(navigator["javaEnabled"]);
navigator.__proto__["sendBeacon"]              = function sendBeacon(){debugger;};  safefunction(navigator["sendBeacon"]);
navigator.__proto__["vibrate"]                 = function vibrate(){debugger;};     safefunction(navigator["vibrate"]);
navigator.__proto__["scheduling"]              = new (class Scheduling {});
navigator.__proto__["mediaCapabilities"]       = new (class MediaCapabilities {});
navigator.__proto__["permissions"]             = new (class Permissions {});
navigator.__proto__["mediaSession"]            = new (class MediaSession {});
window.location["ancestorOrigins"] = new (class DOMStringList {});
window.location["href"]            = "http://app1.nmpa.gov.cn/data_nmpa/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=152904713761213296322795806604&CbSlDlH0=qGc5kacU2y8U2y8U2enJaDCR.TmXaHUY4V.RdcrvZCQqqxQ";
window.location["origin"]          = "http://app1.nmpa.gov.cn";
window.location["protocol"]        = "http:";
window.location["host"]            = "app1.nmpa.gov.cn";
window.location["hostname"]        = "app1.nmpa.gov.cn";
window.location["port"]            = "";
window.location["pathname"]        = "/data_nmpa/face3/base.jsp";
window.location["search"]          = "?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=152904713761213296322795806604&CbSlDlH0=qGc5kacU2y8U2y8U2enJaDCR.TmXaHUY4V.RdcrvZCQqqxQ";
window.location["hash"]            = "";
window.location["assign"]          = function assign(){debugger;};  safefunction(window.location["assign"]);
window.location["reload"]          = function reload(){debugger;};  safefunction(window.location["reload"]);
window.location["replace"]         = function replace(){debugger;}; safefunction(window.location["replace"]);
window.localStorage["FSSBB16"]      = "449709:j7ph23QYOI92qmRsUj0wta";
window.localStorage["FSSBB3"]       = "449709:bpUrsKE3gKMS9.O6igoafa";
window.localStorage["FSSBB21"]      = "449709:j4lc.Ceen.t6bP2rHXz7TA";
window.localStorage["FSSBB40"]      = "449709:1";
window.localStorage["$_fh0"]        = "t5vkmXwuUtqfnaX42LaFxHN6SJ9";
window.localStorage["$_fb"]         = "J6vyYlSv1XsYgvYwG3aDh_04aQlC53.8l8bYFyUgWyHQuMmRESfyD9LdUWLlK2RE";
window.localStorage["FSSBB17"]      = "449709:3Vm70s24xdXcsSP6wql2MA";
window.localStorage["$_f1"]         = "d24b9D80LxpDy55WxWI8MfvOM6Z";
window.localStorage["$_YWTU"]       = "FEQUsSBVzv0QWk6YXiwmU1rTQu5fgYnAS0QCjp2noTZ";
window.localStorage["$_f0"]         = "B_NtkFSQA4JOlBfLn.K4gILrPFL";
window.localStorage["__#classType"] = "localStorage";
window.localStorage["$_nd"]         = "152516";
window.localStorage["FSSBB47"]      = "449709:1";
window.localStorage["FSSBB2"]       = "449709:jAOI94RObj1ow2EW3kdJqA";
window.localStorage["FSSBB15"]      = "449709:2";
window.localStorage["FSSBB18"]      = "449709:V89Lcdd7icYi26_b9xc3Fa";
window.localStorage["$_cDro"]       = "1";
window.sessionStorage["$_cDro"] = "1";
window.sessionStorage["$_YWTU"] = "FEQUsSBVzv0QWk6YXiwmU1rTQu5fgYnAS0QCjp2noTZ";



























for (let key in navigator.__proto__) {
    navigator[key] = navigator.__proto__[key];
    if (typeof (navigator.__proto__[key]) != "function") {
        navigator.__proto__.__defineGetter__(key, function() {
            debugger ;var e = new Error();
            e.name = "TypeError";
            e.message = "Illegal invocation";
            e.stack = "VM988:1 Uncaught TypeError: Illegal invocation \r\n at <anonymous>:1:19";
            throw e;
        });
    }
}