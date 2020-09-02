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

// 钩子函数的实现
const handler = {
  apply: function (target, thisArg, args){
    console.log("Intercepted a call tocreateElement with args: " + args);
    return target.apply(thisArg, args)
  }
}
document.createElement = new Proxy(document.createElement, handler);
document.createElement.toString = Function.prototype.toString
