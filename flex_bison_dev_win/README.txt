windows 下的 bison/flex 开发模板

个人开发环境为 windows64 位系统
flex 和 bison 的windows版本的工具已经集成在此处，只需要安装编译器即可。
在该 README.txt 目录路径下的 cmd 内执行 run.bat 即可在当前路径下生成一个exe文件。
默认模板清理中间文件，若你需要请在 .bat 文件中修改。

建议安装 tcc 编译器，也是个人建议的编译器工具，编译快且编译出的体积小很多
如果想换编译器，换成 gcc，在 run.bat 里面将 tcc 修改成 gcc 即可
（tcc 和 gcc 都需要处理环境变量的问题）