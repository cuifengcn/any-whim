function AddCatchLog(path){
    var err_name = path.node.param.name
    path.node.body.body.unshift({
        "type": "ExpressionStatement",
        "expression": {
            "type": "CallExpression",
            "callee": {
                "type": "MemberExpression",
                "computed": false,
                "object": {
                    "type": "Identifier",
                    "name": "console"
                },
                "property": {
                    "type": "Identifier",
                    "name": "log"
                }
            },
            "arguments": [
                {
                    "type": "Identifier",
                    "name": err_name
                }
            ]
        }
    })
}



function muti_process_defusion(jscode){
    var ast = parser.parse(jscode);
    traverse(ast, {CatchClause: AddCatchLog});
    var { code } = generator(ast, { jsescOption: { minimal: true, } });
    return code;
}
const fs = require('fs');
var jscode = fs.readFileSync("./addlog.js", {
    encoding: "utf-8"
});
code = muti_process_defusion(jscode);
// console.log(code);
fs.writeFileSync('./addloger.js', code, {
    encoding: "utf-8"
})