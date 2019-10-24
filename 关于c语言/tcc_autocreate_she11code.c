// 32位与64位 通用的 windows she11code 生成工具。 语法依 at&t 语法，
// tcc 与 gcc 均能编译并且成功执行，值得注意的是，tcc 与 gcc 编译函数的方式稍微有点不太一样。所以下面有部分使用了宏定义处理
// 为了更强的兼容性，这里将不使用 naked 的函数处理方式，防止部分 gcc 无法编译通过的情况。
// （注意，这里使用的 gcc 是旧版本的 gcc，也就是那个安装 devcpp 时附带会安装的那个旧版本。 貌似是 4.9）
// （如果是高版本的 gcc 请留意一下在 gcc_autocreate_she11code.c 的不同实现，那里兼容 naked 的函数语法）
// （不得不说我一个c语言萌新TM也没想到不同版本竟然TMD不兼容）
// gcc 不同版本造成的影响只会影响到汇编的函数跳转部分，所以正常开发即可，遇到错误需要考虑是否会是汇编的问题。
// 这里的代码支持低版本的 gcc，并且这里支持64，32位的交叉编译。

// 编写 she11code 的代码需要注意的是
// 1) 不能直接使用函数获取函数的地址，需要通过一定的汇编获取 Kernel32 的地址
// 2) 后续找到 GetProcAddress LoadLibraryA 这两个函数的地址后续基本就需要这两个函数进行处理必要函数的获取
// 3) 使用那些函数的时候也需要注意，需要从函数声明的地方获取结构声明，所有“函数声明”不会影响生成的代码的顺序和 she11code 体积。
// 4) 另外 she11code 的编写中注意不能使用任何全局变量，并且函数内“字符串声明”的方式只能使用 char[] 来实现，
//    这是为了避免字符串由于编译器优化被放到其他地方从而 she11code 不完整。
// cmd> tcc tcc_autocreate_she11code.c
// 需要生成32位则在 tcc 命令行加上 -m32 。 生成的工具 tcc_autocreate_she11code.exe 执行后会生成 sh.bin 的文件(she11code)。

#include <stdio.h>
#include <windows.h>

HMODULE getKernel32();
FARPROC getProcAddress(HMODULE hModuleBase);
void ShellcodeStart();
void ShellcodeEntry();
void ShellcodeEnd();
void CreateShellcode();
char* ShellcodeEncode(int size);
void ShellcodeDecode();

// create shellcode bin.
// int WINAPI WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
#ifdef _WIN64
int main(int argc, char const *argv[]) {
    printf("kernel32:       %016llx\n", getKernel32());
    printf("GetProcAddress: %016llx\n", getProcAddress((HMODULE)getKernel32()));
    CreateShellcode();
}
#else
int main(int argc, char const *argv[]) {
    printf("kernel32:       %016lx\n", getKernel32());
    printf("GetProcAddress: %016lx\n", getProcAddress((HMODULE)getKernel32()));
    CreateShellcode();
}
#endif
void CreateShellcode(){
    HANDLE hBin = CreateFileA("sh.bin", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
    DWORD dwSize;
    DWORD dwWrite;
    if (hBin == INVALID_HANDLE_VALUE){
        printf("%s error:%d\n", "create sh.bin fail.", GetLastError());
        return;
    }

    // 想实现自动 shellcode 加解密的功能，不过目前在编译 32位的 shellcode 程序会有异常。
    // 另外这种实现方式可以处理预加密，但是解密的头最好还是不要在这里就直接以函数方式实现。
    // 对于 shellcode 来说，需要更加精致的实现手段。
    // WriteFile(hBin, ShellcodeDecode, ShellcodeStart - ShellcodeDecode, &dwWrite, NULL);
    // printf("ShellcodeSize:  %16d\n", dwWrite);
    // char* newShellcode = ShellcodeEncode(ShellcodeEnd - ShellcodeStart);
    // WriteFile(hBin, newShellcode, ShellcodeEnd - ShellcodeStart, &dwWrite, NULL);
    // printf("ShellcodeSize:  %16d\n", dwWrite);
    
    dwSize = ShellcodeEnd - ShellcodeStart;
    WriteFile(hBin, ShellcodeStart, dwSize, &dwWrite, NULL);
    printf("ShellcodeSize:  %16d\n", dwWrite);
}


// 64位编译，64位系统测试下，这里是可以成功跑通，而32位则不行，暂时未知。
// 加密可以实现，但是解密却只能在 64 位上复现有点奇怪。
// char* ShellcodeEncode(int size){
    // char* temp = (char *)malloc(size* sizeof(char));
    // int i = 0;
    // for(;i < size; i++){
        // temp[i] = ((char*)ShellcodeStart)[i] ^ 233;
    // }
    // return temp;
// }
// void ShellcodeDecode(){
    // DWORD dwSize = ShellcodeEnd - ShellcodeStart;
    // int i = 0;
    // for(;i < dwSize; i++){
        // ((char*)ShellcodeStart)[i] ^= 233;
    // }
    // ShellcodeStart(); // TINYC use this
// }
// shellcode
void ShellcodeStart(){
    #ifdef __MINGW32__
        #ifdef _WIN64
        asm("pop %rbp"); 
        asm("jmp ShellcodeEntry");
        #else
        asm("pop %ebp"); 
        asm("jmp _ShellcodeEntry"); // old style. fuck!
        #endif
    #else
    ShellcodeEntry(); // TINYC use this
    #endif
}
// init function struct.
typedef FARPROC (WINAPI* FN_GetProcAddress)(
    HMODULE hModule,
    LPCSTR lpProcName
);
typedef HMODULE (WINAPI* FN_LoadLibraryA)(
    LPCSTR lpLibFileName
);
typedef int (WINAPI* FN_MessageBoxA)(
    HWND hWnd ,
    LPCSTR lpText,
    LPCSTR lpCaption,
    UINT uType
);
typedef HANDLE (WINAPI* FN_CreateFileA)(
    LPCSTR lpFileName,
    DWORD dwDesiredAccess,
    DWORD dwShareMode,
    LPSECURITY_ATTRIBUTES lpSecurityAttributes,
    DWORD dwCreationDisposition,
    DWORD dwFlagsAndAttributes,
    HANDLE hTemplateFile
);
typedef struct _FUNCTION {
    FN_GetProcAddress   fn_GetProcAddress;
    FN_LoadLibraryA     fn_LoadLibraryA;
    FN_CreateFileA      fn_CreateFileA;
    FN_MessageBoxA      fn_MessageBoxA;
}FUNCTION, *PFUNCTION;
void InitFunctions(PFUNCTION pFn){
    char szLoadLibraryA[] = {'L','o','a','d','L','i','b','r','a','r','y','A','\0'};
    char szUser32[] = {'u','s','e','r','3','2','\0'};
    char szMessageBoxA[] = {'M','e','s','s','a','g','e','B','o','x','A','\0'};
    char szKernel32[] = {'k','e','r','n','e','l','3','2','\0'};
    char szCreateFileA[] = {'C','r','e','a','t','e','F','i','l','e','A','\0'};
    pFn->fn_GetProcAddress  = (FN_GetProcAddress)getProcAddress((HMODULE)getKernel32());
    pFn->fn_LoadLibraryA    = (FN_LoadLibraryA)pFn->fn_GetProcAddress((HMODULE)getKernel32(), szLoadLibraryA);
    pFn->fn_MessageBoxA     = (FN_MessageBoxA)pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szUser32), szMessageBoxA);
    pFn->fn_CreateFileA     = (FN_CreateFileA)pFn->fn_GetProcAddress(pFn->fn_LoadLibraryA(szKernel32), szCreateFileA);
}
// work funciton
void WKCreateFile(PFUNCTION pFn){
    char szFileName[] = {'.','/','1','.','t','x','t','\0'};
    pFn->fn_CreateFileA(szFileName,GENERIC_WRITE,0,NULL,CREATE_ALWAYS,0,NULL);
}
void WKMessageBox(PFUNCTION pFn){
    pFn->fn_MessageBoxA(NULL,NULL,NULL,0);
}
// shellcode main
void ShellcodeEntry(){
    FUNCTION fn;
    InitFunctions(&fn);
    WKCreateFile(&fn);
    WKMessageBox(&fn);
}
// get kernel32 and get GetProcAddress.
#ifdef _WIN64
HMODULE getKernel32(){
    asm("mov %gs:(0x60), %rax");
    asm("mov 0x18(%rax), %rax");
    asm("mov 0x20(%rax), %rax");
    asm("mov (%rax), %rax");
    asm("mov (%rax), %rax");
    asm("mov 0x20(%rax), %rax");
    #ifdef __MINGW32__
    asm("pop %rbp"); // sometime you cannot use naked func, this is for more compatibility.
    asm("ret"); // TINYC dnot need this
    #endif
}
#else
HMODULE getKernel32(){
    asm("mov %fs:(0x30), %eax");
    asm("mov 0x0c(%eax), %eax");
    asm("mov 0x14(%eax), %eax");
    asm("mov (%eax), %eax");
    asm("mov (%eax), %eax");
    asm("mov 0x10(%eax), %eax");
    #ifdef __MINGW32__
    asm("pop %ebp"); // sometime you cannot complier naked func, this is for more compatibility.
    asm("ret"); // TINYC dnot need this
    #endif
}
#endif
FARPROC getProcAddress(HMODULE hModuleBase){
    LPBYTE lpBaseAddr = (LPBYTE)hModuleBase;
    PIMAGE_DOS_HEADER lpDosHdr = (PIMAGE_DOS_HEADER)lpBaseAddr;
    PIMAGE_NT_HEADERS pNtHdrs = (PIMAGE_NT_HEADERS)(lpBaseAddr + lpDosHdr->e_lfanew);
    PIMAGE_EXPORT_DIRECTORY pExportDir = (PIMAGE_EXPORT_DIRECTORY)(lpBaseAddr + pNtHdrs->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
    LPDWORD pNameArray = (LPDWORD)(lpBaseAddr + pExportDir->AddressOfNames);
    LPDWORD pAddrArray = (LPDWORD)(lpBaseAddr + pExportDir->AddressOfFunctions);
    LPWORD pOrdArray = (LPWORD)(lpBaseAddr + pExportDir->AddressOfNameOrdinals);
    FARPROC GetProcAddressAPI;
    UINT i = 0;
    for (; i < pExportDir->NumberOfNames; i++){
        LPSTR pFuncName = (LPSTR)(lpBaseAddr + pNameArray[i]);
        if (    pFuncName[0] == 'G' &&
                pFuncName[1] == 'e' &&
                pFuncName[2] == 't' &&
                pFuncName[3] == 'P' &&
                pFuncName[4] == 'r' &&
                pFuncName[5] == 'o' &&
                pFuncName[6] == 'c' &&
                pFuncName[7] == 'A' &&
                pFuncName[8] == 'd' &&
                pFuncName[9] == 'd' &&
                pFuncName[10] == 'r' &&
                pFuncName[11] == 'e' &&
                pFuncName[12] == 's' &&
                pFuncName[13] == 's'     ){
            GetProcAddressAPI = (FARPROC)(lpBaseAddr + pAddrArray[pOrdArray[i]]);
            return GetProcAddressAPI;
        }
    }
    return NULL;
}
void ShellcodeEnd(){
}