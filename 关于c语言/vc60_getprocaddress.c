#include <stdio.h>
#include <windows.h>

__declspec(naked) DWORD getKernel32(){
    __asm{
        mov eax, fs:[30h]
        mov eax, [eax+0ch]
        mov eax, [eax+14h]
        mov eax, [eax]
        mov eax, [eax]
        mov eax, [eax+10h]
        ret
    }
}

FARPROC _GetProcAddress(HMODULE hModuleBase){
    PIMAGE_DOS_HEADER lpDosHeader = (PIMAGE_DOS_HEADER)hModuleBase;
    PIMAGE_NT_HEADERS32 lpNtHeader = (PIMAGE_NT_HEADERS32)((DWORD)lpDosHeader + lpDosHeader->e_lfanew);
    PIMAGE_EXPORT_DIRECTORY lpExports;
    PDWORD  lpdwFunName;
    PWORD   lpwOrd;
    PDWORD  lpdwFunAddr;
    DWORD   dwLoop;
    FARPROC pRet;
    char* pFunName;
    if (!lpNtHeader -> OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].Size){
        return NULL;
    }

    if (!lpNtHeader -> OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress){
        return NULL;
    }
    lpExports   = (PIMAGE_EXPORT_DIRECTORY)((DWORD)hModuleBase + (DWORD)lpNtHeader->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
    lpdwFunName = (PDWORD)((DWORD)hModuleBase + (DWORD)lpExports->AddressOfNames);
    lpwOrd      = (PWORD)((DWORD)hModuleBase  + (DWORD)lpExports->AddressOfNameOrdinals);
    lpdwFunAddr = (PDWORD)((DWORD)hModuleBase + (DWORD)lpExports->AddressOfFunctions);
    dwLoop      = 0;
    pRet        = NULL;
    for (;dwLoop <= lpExports->NumberOfNames - 1; dwLoop++){
        pFunName = (char*)(lpdwFunName[dwLoop] + (DWORD)hModuleBase);
        if (    pFunName[0] == 'G' &&
                pFunName[1] == 'e' &&
                pFunName[2] == 't' &&
                pFunName[3] == 'P' &&
                pFunName[4] == 'r' &&
                pFunName[5] == 'o' &&
                pFunName[6] == 'c' &&
                pFunName[7] == 'A' &&
                pFunName[8] == 'd' &&
                pFunName[9] == 'd' &&
                pFunName[10] == 'r' &&
                pFunName[11] == 'e' &&
                pFunName[12] == 's' &&
                pFunName[13] == 's'     ){
            pRet = (FARPROC)(lpdwFunAddr[lpwOrd[dwLoop]] + (DWORD)hModuleBase);
            break;
        }
    }
    return pRet;
}

int main(){
    HMODULE hLoadLibraryA = (HMODULE)getKernel32();
    typedef FARPROC (WINAPI* FN_GetProcAddress)(
        HMODULE hModule,
        LPCSTR lpProcName
    );
    FN_GetProcAddress fn_GetProcAddress;
    fn_GetProcAddress = (FN_GetProcAddress)_GetProcAddress(hLoadLibraryA);

    printf("0x%08x\n", fn_GetProcAddress);
    printf("0x%08x\n", GetProcAddress);


    /*
    LPVOID lp = GetProcAddress(LoadLibraryA("user32"), "MessageBoxA");
    char * s = "hello world.";
    __asm{
        push 0
        push 0
        push s
        push 0
        call lp
    }
    */  

    /*
    typedef HANDLE (WINAPI* FN_CreateFileA)(
        LPCSTR lpFileName,
        DWORD dwDesiredAccess,
        DWORD dwShareMode,
        LPSECURITY_ATTRIBUTES lpSecurityAttributes,
        DWORD dwCreationDisposition,
        DWORD dwFlagsAndAttributes,
        HANDLE hTemplateFile
        );
    FN_CreateFileA fn_CreateFileA;
    fn_CreateFileA = (FN_CreateFileA)GetProcAddress(LoadLibraryA("kernel32.dll"), "CreateFileA");
    fn_CreateFileA("./hello123123.txt",GENERIC_WRITE,0,NULL,CREATE_ALWAYS,0,NULL);
    */


    return 0;
}