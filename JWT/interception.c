// 暂时不清楚这个代码是否有用。

#include <stdio.h>
#include <windows.h>
#include "interception.h"
#pragma comment(lib, "interception")

int MAPVK_VK_TO_VSC = 0;

int main(){

    Sleep(3000);

    InterceptionContext context = interception_create_context();
    InterceptionKeyStroke keyStroke[2];
    ZeroMemory(keyStroke, sizeof(keyStroke));
    // keyStroke[0].code = MapVirtualKey('A', MAPVK_VK_TO_VSC);
    keyStroke[0].code = 'a';
    keyStroke[0].state = INTERCEPTION_KEY_DOWN;
    keyStroke[1].code = keyStroke[0].code;
    keyStroke[1].state = INTERCEPTION_KEY_UP;
    interception_send(context, INTERCEPTION_KEYBOARD(0), (InterceptionStroke*)keyStroke, _countof(keyStroke));
    interception_destroy_context(context);
}