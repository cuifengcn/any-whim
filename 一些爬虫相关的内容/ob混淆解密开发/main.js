print = console.log

var esprima = require('esprima');
var estraverse = require('estraverse')
var escodegen = require('escodegen')

// 合并简单的二元运算
function combine_binary(tree) {
    var has_change = false;
    estraverse.replace(tree, {
        enter(node, parent){
            if (node.type === 'BinaryExpression' && node.left.type === 'Literal' && node.right.type === 'Literal') {
                has_change = true;
                return {
                    type: 'Literal',
                    value: eval(JSON.stringify(node.left.value) + node.operator + JSON.stringify(node.right.value))
                };
            }
        }
    });
    if (has_change){
        combine_binary(tree);
    }
};

// 后面的部分是用于 ob混淆的逆向处理
var hook_regexp_test = `// 确保如果出现正则检测代码格式化反调试的时候能始终返回 true;
(function(){
  RegExp_test_string = RegExp.prototype.test.toString();
  const handler = { apply: function (target, thisArg, args){ return true; } }
  const handler_tostring = { apply: function (target, thisArg, args){ return RegExp_test_string; } }
  RegExp.prototype.test = new Proxy(RegExp.prototype.test, handler);
  RegExp.prototype.test.toString = new Proxy(RegExp.prototype.test.toString, handler_tostring);
})();
// 用于 node 环境的处理
window = typeof global == "undefined" ? window : global;
`
// 
function step1(tree){
    var str_func;
    var func_name;
    estraverse.traverse(tree, {
        enter(node, parent) {
            if (parent == null){
                for (var i = 0; i < node.body.length; i++) {
                    if (node.body[i].type == 'VariableDeclaration' && 
                        node.body[i].declarations && 
                        node.body[i].declarations[node.body[i].declarations.length-1].init.type == 'ArrayExpression'){
                        break
                    }
                }
                str_func = hook_regexp_test + [
                        escodegen.generate(node.body[0+i]),
                        escodegen.generate(node.body[1+i]),
                        escodegen.generate(node.body[2+i]),
                    ].join('\n')
                func_name = node.body[2+i].declarations[0].id.name
                node.body = node.body.slice(3+i, node.body.length)
            }
        }
    });
    eval(str_func)
    estraverse.replace(tree, {
        leave(node, parent) {
            if (node.type === 'CallExpression' && node.callee.name === func_name){
                var val = eval(escodegen.generate(node))
                return { type: 'Literal', value: val, raw: val }
            }
        }
    });
}

// 遍历展示
function show(tree) {
    estraverse.traverse(tree, {
        enter(node, parent) {
            if (parent == null){
                print(parent)
                print('---------------')
                print(node)
                print('===============')

            }
        }
    });
}














const fs = require('fs');
var jscode = fs.readFileSync('./test.js', {
    encoding: "utf-8"
});

function muti_process_defusion(code){
    var tree = esprima.parseScript(code)
    combine_binary(tree); // 合并二元运算

    step1(tree)
    combine_binary(tree); // 合并二元运算
    return hook_regexp_test+escodegen.generate(tree);
}

code = muti_process_defusion(jscode)
print(code)