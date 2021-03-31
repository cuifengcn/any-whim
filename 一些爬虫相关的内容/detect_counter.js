// 计数器反调试代码

function make_detect_counter(){
    // 这种主动混淆的方式比较适合将字符串集中优化处理
    // 并且这样得函数经过 ugliy-es 优化后混淆程度会提升很多。
    var _str_defineProperty = "defineProperty"
    var _str_prototype = "prototype"
    var _str_undefined = "undefined"
    var _str_Function = "Function"
    var _str_toString = "toString"
    var _str_replace = "replace"
    var _str_String = "String"
    var _str_Object = "Object"
    var _str_concat = "concat"
    var _str_Number = "Number"
    var _str_RegExp = "RegExp"
    var _str_Array = "Array"
    var _str_test = "test"
    var _str_push = "push"
    var _str_bind = "bind"
    var _str_join = "join"
    var _str_Date = "Date"
    var _str_call = "call"
    var _str_pop = "pop"
    var _str_now = "now"
    var _str_get = "get"
    var _str__ = "_"
    var _window = typeof global==_str_undefined?window:global
    function make_counter(){
        var hide_stack_call_bind_func = function(func){
            return _window[_str_Date][_str_call][_str_bind](_window[_str_Date][_str_call], func)
        }
        var hidden_Object_defineProperty = hide_stack_call_bind_func(_window[_str_Object][_str_defineProperty])
        var make_obj_string = function (str){
            var s = {}
            s[_str_get] = function(){
                return hide_stack_call_bind_func(function(){
                    return _window[_str_String][_str_prototype][_str_toString][_str_call](str)
                })
            }
            s[_str_get] = hide_stack_call_bind_func(s[_str_get])
            hidden_Object_defineProperty(_window[_str_Object], s, _str_toString, s)
            return s
        }
        var make_function_getobj = function(func){
            var temp = {}
            temp[_str_get] = function(){ ckn[_str__]++ ; return func }
            temp[_str_get] = hide_stack_call_bind_func(temp[_str_get])
            return temp
        }
        var Object_defineProperty;
        var String_prototype_toString;
        var Number_prototype_toString;
        var Array_prototype_toString;
        var Function_prototype_toString;
        var RegExp_prototype_toString;
        var push;
        var pop;
        var join;
        var concat;
        var replace;
        var test;
        var now;
        var ckn;

        (Object_defineProperty       = _window[_str_Object][_str_defineProperty])
        &&(String_prototype_toString   = _window[_str_String][_str_prototype][_str_toString])
        &&(Number_prototype_toString   = _window[_str_Number][_str_prototype][_str_toString])
        &&(Array_prototype_toString    = _window[_str_Array][_str_prototype][_str_toString])
        &&(Function_prototype_toString = _window[_str_Function][_str_prototype][_str_toString])
        &&(RegExp_prototype_toString   = _window[_str_RegExp][_str_prototype][_str_toString])
        &&(push                        = [].push)
        &&(pop                         = [].pop)
        &&(join                        = [].join)
        &&(concat                      = [].concat)
        &&(replace                     = ''.replace)
        &&(test                        = _window[_str_RegExp][_str_prototype][_str_test])
        &&(now                         = _window[_str_Date][_str_now])
        &&(ckn = {})
        &&(ckn[_str__] = 0)
        hidden_Object_defineProperty(_window[_str_Object],    _window[_str_Object],                   make_obj_string(_str_defineProperty),    make_function_getobj(Object_defineProperty))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_String][_str_prototype],   make_obj_string(_str_toString),          make_function_getobj(String_prototype_toString))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_Number][_str_prototype],   make_obj_string(_str_toString),          make_function_getobj(Number_prototype_toString))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_Array][_str_prototype],    make_obj_string(_str_toString),          make_function_getobj(Array_prototype_toString))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_Function][_str_prototype], make_obj_string(_str_toString),          make_function_getobj(Function_prototype_toString))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_RegExp][_str_prototype],   make_obj_string(_str_toString),          make_function_getobj(RegExp_prototype_toString))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_Array][_str_prototype],    make_obj_string(_str_push),              make_function_getobj(push))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_Array][_str_prototype],    make_obj_string(_str_pop),               make_function_getobj(pop))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_Array][_str_prototype],    make_obj_string(_str_join),              make_function_getobj(join))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_Array][_str_prototype],    make_obj_string(_str_concat),            make_function_getobj(concat))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_String][_str_prototype],   make_obj_string(_str_replace),           make_function_getobj(replace))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_RegExp][_str_prototype],   make_obj_string(_str_test),              make_function_getobj(test))
        &&hidden_Object_defineProperty(_window[_str_Object],    _window[_str_Date],                     make_obj_string(_str_now),               make_function_getobj(now))
        function get_ckn(order){
            if (order == 1){
                return make_obj_string // 获取string保护函数
            }
            return ckn[_str__]
        }
        get_ckn = hide_stack_call_bind_func(get_ckn)
        get_ckn.$ = ckn[_str__]
        return get_ckn
    }
    return make_counter()
}

function test_(){
    var inject_func = make_detect_counter()
    console.log(inject_func(), inject_func.$)
    Object.defineProperty({}, '_', {value:123})
    console.log('Object,             defineProperty', inject_func(), inject_func.$)
    ;(1)+''
    console.log('Number.prototype,   toString',       inject_func(), inject_func.$)
    ;[]+''
    console.log('Array.prototype,    toString',       inject_func(), inject_func.$)
    ;inject_func+''
    console.log('Function.prototype, toString',       inject_func(), inject_func.$)
    ;/1/+''
    console.log('RegExp.prototype,   toString',       inject_func(), inject_func.$)
    ;[].push(1)
    console.log('Array.prototype,    push',           inject_func(), inject_func.$)
    ;[1].pop(1)
    console.log('Array.prototype,    pop',            inject_func(), inject_func.$)
    ;[1,2].join(",")
    console.log('Array.prototype,    join',           inject_func(), inject_func.$)
    ;[].concat([1,2,3])
    console.log('Array.prototype,    concat',         inject_func(), inject_func.$)
    ;'abcd'.replace('a', '')
    console.log('String.prototype,   replace',        inject_func(), inject_func.$)
    ;/a/.test('a')
    console.log('RegExp.prototype,   test',           inject_func(), inject_func.$)
    Date.now()
    console.log('Date,               now',            inject_func(), inject_func.$) // 这一行正常执行结果 和 你随便在前面打几个调试断点执行到这里的结果你看看变化就知道这个反调试有多强了.
}

test_()