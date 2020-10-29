#include <ntddk.h>
#pragma pack(1)
typedef struct ServiceDescriptorEntry {
    unsigned int *ServiceTableBase;
    unsigned int *ServiceCounterTableBase;
    unsigned int NumberOfServices;
    unsigned char *ParamTableBase;
} ServiceDescriptorTableEntry_t, *PServiceDescriptorTableEntry_t;
#pragma pack()
__declspec(dllimport) ServiceDescriptorTableEntry_t KeServiceDescriptorTable;
ULONG Old_NtCreateFile = 0;
ULONG Address1 = 0;
ULONG Address2 = 0;
typedef NTSTATUS  (*PNEWNTCREATEFILE)(
    OUT PHANDLE  FileHandle,
    IN ACCESS_MASK  DesiredAccess,
    IN POBJECT_ATTRIBUTES  ObjectAttributes,
    OUT PIO_STATUS_BLOCK  IoStatusBlock,
    IN PLARGE_INTEGER  AllocationSize  OPTIONAL,
    IN ULONG  FileAttributes,
    IN ULONG  ShareAccess,
    IN ULONG  CreateDisposition,
    IN ULONG  CreateOptions,
    IN PVOID  EaBuffer  OPTIONAL,
    IN ULONG  EaLength
    );
void PageProtectOn() {
    __asm {
        mov  eax, cr0
        or   eax, 10000h
        mov  cr0, eax
        sti
    }
}
void PageProtectOff() {
    __asm {
        cli
        mov  eax, cr0
        and  eax, not 10000h
        mov  cr0, eax
    }
}
ULONG SearchAddress() {
    int i = 0;
    UCHAR *p = (UCHAR *)Address1;
    for (i = 0; i < 100; i++) {
        if (*p == 0x2b && 
            *(p + 1) == 0xe1 && 
            *(p + 2) == 0xc1 && 
            *(p + 3) == 0xe9 && 
            *(p + 4) == 0x02) {
            Address2 = (ULONG)p;
            return (ULONG)p;
        }
        p--;
    }
    return 0;
}
VOID File_HOOKAPI(ULONG ServiceTableBase, ULONG NumberOfServices) {
    if (ServiceTableBase == (ULONG)KeServiceDescriptorTable.ServiceTableBase) {
        if (NumberOfServices == 119) {
            KdPrint(("看那些进入KiFasetCallEntry调用ntopenkey进程名是%s\n", (char*)PsGetCurrentProcess() + 0x174));
        }
    }
}
__declspec(naked)
VOID NewKiFastCallEntry() {
    __asm{
        pushad
        pushfd
        push eax
        push edi
        call File_HOOKAPI
        popfd
        popad
        pop eax
        sub esp, ecx
        shr ecx, 2
        jmp eax
    }
}
VOID Hook_KiFastCallEntry() {
    ULONG AwayAddress = 0;
    UCHAR TraitCode[5];
    TraitCode[0] = 0xE8;
    AwayAddress = (ULONG)NewKiFastCallEntry - 5 - Address2;
    *(ULONG*)&TraitCode[1] = AwayAddress;
    PageProtectOff();
    RtlCopyMemory((PVOID)Address2, TraitCode, 5);
    PageProtectOn();
}
NTSTATUS  NewCreateFile(
    OUT PHANDLE  FileHandle,
    IN ACCESS_MASK  DesiredAccess,
    IN POBJECT_ATTRIBUTES  ObjectAttributes,
    OUT PIO_STATUS_BLOCK  IoStatusBlock,
    IN PLARGE_INTEGER  AllocationSize  OPTIONAL,
    IN ULONG  FileAttributes,
    IN ULONG  ShareAccess,
    IN ULONG  CreateDisposition,
    IN ULONG  CreateOptions,
    IN PVOID  EaBuffer  OPTIONAL,
    IN ULONG  EaLength
    ) {
    __asm{
        pushad
        mov eax, [ebp + 0x4]
        mov Address1, eax
        popad
    }
    SearchAddress();
    Hook_KiFastCallEntry();
    return (((PNEWNTCREATEFILE)Old_NtCreateFile)(FileHandle, DesiredAccess, ObjectAttributes,
        IoStatusBlock, AllocationSize, FileAttributes, ShareAccess, CreateDisposition, CreateOptions,
        EaBuffer, EaLength));
}
VOID DriverUnload(IN PDRIVER_OBJECT pDriverObject) {
    UCHAR tezhengma[5] = { 0x2b, 0xe1, 0xc1, 0xe9, 0x02 };
    PageProtectOff();
    KeServiceDescriptorTable.ServiceTableBase[37] = (unsigned int)Old_NtCreateFile;
    PageProtectOn();
    PageProtectOff();
    RtlCopyMemory((PVOID)Address2, tezhengma, 5);
    PageProtectOn();
    KdPrint(("已经执行到驱动卸载历程\n"));
}
NTSTATUS DriverEntry(IN PDRIVER_OBJECT pDriverObject, IN PUNICODE_STRING RegistryPath) {
    Old_NtCreateFile = KeServiceDescriptorTable.ServiceTableBase[37];
    PageProtectOff();
    KeServiceDescriptorTable.ServiceTableBase[37] = (unsigned int)NewCreateFile;
    PageProtectOn();
    pDriverObject->DriverUnload = DriverUnload;
    DbgPrint("DriverEntry");
    return STATUS_SUCCESS;
}