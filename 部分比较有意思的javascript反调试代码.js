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
