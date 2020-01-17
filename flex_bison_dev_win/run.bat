@echo off
SET PATH = %PATH%;".\bin"
@echo on

.\bin\bison.exe -vdty grammar.y
.\bin\flex.exe lex.l
gcc -o fin.exe y.tab.c lex.yy.c

@echo off
del y.tab.c y.tab.h y.output lex.yy.c
@echo on