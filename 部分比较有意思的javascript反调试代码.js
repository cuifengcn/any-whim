// 某些 dev-tools(F12) 的反调试代码
setTimeout(function adbg() {
  var d = new Image;
  Object.defineProperty(d, "id", {get: function() {
      alert(123);
  }})
  console.log(d);
  console.clear();
  setTimeout(adbg, 200);
}, 200)

// 挂钩内置函数 window.eval
// 如果想挂钩别的，可以将 window.eval 直接替换成别的即可，例如 document.createElement
(function(){
  eval_string = window.eval.toString()
  const handler = {
    apply: function (target, thisArg, args){
      console.log("Intercepted a call eval with args: " + args);
      return target.apply(thisArg, args)
    }
  }
  const handler_tostring = {
    apply: function (target, thisArg, args){
      return eval_string;
    }
  }
  window.eval = new Proxy(window.eval, handler);
  window.eval.toString = new Proxy(window.eval.toString, handler_tostring);
})();

// 挂钩 cookie 生成的时机。
(function(){
  'use strict';
  Object.defineProperty(
    document, 'cookie', {
      set: function(cookie){
        // if (cookie.indexOf('RM4hZBv0dDon443M') != -1){ debugger; }
        debugger;
        return cookie;
      }
    }
  )
})();

// 挂钩一些 constructor 形式的调用
Function.prototype.__defineGetter__('constructor', function() {
  return function(...args) {
    console.log('code:', ...args);
    return Function(...args);
  };
});


window.btoa = function btoa(str) {
  var buffer;
  if (str instanceof Buffer) {
    buffer = str;
  } else {
    buffer = Buffer.from(str.toString(), 'binary');
  }
  return buffer.toString('base64');
}







// 挂钩 XMLHttpRequest. 设置请求头和发起请求的时机
(function(){
  XMLHttpRequest_prototype_open_str = XMLHttpRequest.prototype.open.toString()
  const handler = { apply: function (target, thisArg, args){
      // debugger;
      console.log("----- XMLHttpRequest_open -----\n", args)
      return target.apply(thisArg, args) } }
  const handler_tostring = { apply: function (target, thisArg, args){ return XMLHttpRequest_prototype_open_str; } }
  XMLHttpRequest.prototype.open = new Proxy(XMLHttpRequest.prototype.open, handler);
  XMLHttpRequest.prototype.open.toString = new Proxy(XMLHttpRequest.prototype.open.toString, handler_tostring);
})();
(function(){
  XMLHttpRequest_prototype_setRequestHeader_str = XMLHttpRequest.prototype.setRequestHeader.toString()
  const handler = { apply: function (target, thisArg, args){
      // debugger;
      console.log("----- XMLHttpRequest_setRequestHeader -----\n", args)
      return target.apply(thisArg, args) } }
  const handler_tostring = { apply: function (target, thisArg, args){ return XMLHttpRequest_prototype_setRequestHeader_str; } }
  XMLHttpRequest.prototype.setRequestHeader = new Proxy(XMLHttpRequest.prototype.setRequestHeader, handler);
  XMLHttpRequest.prototype.setRequestHeader.toString = new Proxy(XMLHttpRequest.prototype.setRequestHeader.toString, handler_tostring);
})();

// 挂钩生成cookie设置时机
(function(){
  var _cookie = document.__lookupSetter__('cookie');
  var _cookie_set = function(c) {
    if (/RM4hZBv0dDon443M/.test(c)){
      // debugger;
    }
    console.log('----- cookie.set -----\n', c);
    _cookie = c;
    return _cookie;
  }
  var mycookie = document.cookie;
  document.__defineSetter__("cookie", _cookie_set);
  document.__defineGetter__("cookie", function() {return _cookie;} );
  Object.getOwnPropertyNames(String.prototype).filter(k => !!String.prototype[k].call).map(function(a){
    if (!/^caller$|^callee$|^arguments$/.test(a)){
      document.cookie[a] = mycookie[a];
    }
  });
  document.cookie.toString = function (){ return mycookie.toString() };
})();

// 挂钩一些对象的参数，可以快速定位参数赋值点，快速调试
(function(){
  var pname = '_$ss';
  var pobject = window;
  var win_param = pobject.__lookupSetter__(pname);
  var win_param_set = function(c) {
    console.log('----- ' + pname + '.set -----\n', c);
    win_param = c;
    return win_param;
  }
  pobject.__defineSetter__(pname, win_param_set);
  pobject.__defineGetter__(pname, function() {return win_param;} );
})();

// 挂钩打印函数
_console_log = console.log;
console.log = function(...args){
  if (args && args[0] == '有时候控制台输出太多无意义内容会影响性能，可以hook对部分字符串进行不打印'){
    return 
  }
  _console_log(...args);
}


// 挂钩一些对象的参数，特别是该值为列表，也会挂钩该列表对象的push函数
var hook_set = (function(pname, pobject){
  var pname = '_$pr';
  var pobject = window;
  var win_param = pobject.__lookupSetter__(pname);
  var hookpush = false;
  var win_param_set = function(c) {
    console.log('----- ' + pname + '.set -----\n', c);
    win_param = c;
    if (!hookpush && win_param instanceof Array){
      (function(){
        pobject_push_str = win_param.push.toString()
        const handler = { apply: function (target, thisArg, args){
            debugger;
            console.log("----- Array.push -----\n", args)
            return target.apply(thisArg, args) } }
        const handler_tostring = { apply: function (target, thisArg, args){ return pobject_push_str; } }
        win_param.push = new Proxy(win_param.push, handler);
        win_param.push.toString = new Proxy(win_param.push.toString, handler_tostring);
      })();
      hookpush=true;
    }
    return win_param;
  }
  pobject.__defineSetter__(pname, win_param_set);
  pobject.__defineGetter__(pname, function() {return win_param;} );
});
// hook_set('_$ss', window)