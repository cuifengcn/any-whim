// 32位与64位 通用的 windows she11code 生成工具。 语法依 at&t 语法，
// 目前只能 tcc 编译，gcc 生成的exe文件执行生成的 sh.bin 文件(she11code)无法使用。
// 编写 she11code 的代码需要注意的是
// 1) 不能直接使用函数获取函数的地址，需要通过一定的汇编获取 Kernel32 的地址
// 2) 后续找到 GetProcAddress LoadLibraryA 这两个函数的地址后续基本就需要这两个函数进行处理必要函数的获取
// 3) 使用那些函数的时候也需要注意，需要从函数声明的地方获取结构声明，所有“函数声明”不会影响生成的代码的顺序和 she11code 体积。
// 4) 另外 she11code 的编写中注意不能使用任何全局变量，并且函数内“字符串声明”的方式只能使用 char[] 来实现，
//    这是为了避免字符串由于编译器优化被放到其他地方从而 she11code 不完整。
// cmd> tcc tcc_autocreate_she11code.c
// 需要生成32位则在 tcc 命令行加上 -m 。 生成的工具 tcc_autocreate_she11code.exe 执行后会生成 sh.bin 的文件(she11code)。

#include <stdio.h>
#include <windows.h>

HMODULE getKernel32();
FARPROC getProcAddress(HMODULE hModuleBase);
void ShellcodeStart();
void ShellcodeEntry();
void ShellcodeEnd();
void CreateShellcode();

// create shellcode bin.
// int WINAPI WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
int main(int argc, char const *argv[]) {
    printf("kernel32:       %016llx\n", getKernel32());
    printf("GetProcAddress: %016llx\n", getProcAddress((HMODULE)getKernel32()));
    CreateShellcode();
}
void CreateShellcode(){
    HANDLE hBin = CreateFileA("sh.bin", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
    DWORD dwSize;
    DWORD dwWrite;
    if (hBin == INVALID_HANDLE_VALUE){
        printf("%s error:%d\n", "create sh.bin fail.", GetLastError());
        return;
    }
    dwSize = ShellcodeEnd - ShellcodeStart;
    WriteFile(hBin, ShellcodeStart, dwSize, &dwWrite, NULL);
}







// shellcode
__declspec(naked) void ShellcodeStart(){
    asm("call ShellcodeEntry");
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
    UINT uType);
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
__declspec(naked) HMODULE getKernel32(){
    asm("mov %gs:(0x60), %rax");
    asm("mov 0x18(%rax), %rax");
    asm("mov 0x20(%rax), %rax");
    asm("mov (%rax), %rax");
    asm("mov (%rax), %rax");
    asm("mov 0x20(%rax), %rax");
}
#else
__declspec(naked) HMODULE getKernel32(){
    asm("mov %fs:(0x30), %eax");
    asm("mov 0x0c(%eax), %eax");
    asm("mov 0x14(%eax), %eax");
    asm("mov (%eax), %eax");
    asm("mov (%eax), %eax");
    asm("mov 0x10(%eax), %eax");
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
    for (UINT i = 0; i < pExportDir->NumberOfNames; i++){
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