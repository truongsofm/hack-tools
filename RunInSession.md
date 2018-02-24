Run program in other Windows Terminal Session ~ `runas`

Compiler : [**Visual C++ 2015 Build Tools**](http://landinghub.visualstudio.com/visual-cpp-build-tools) (C)
```C
#include <stdio.h>
#include <string.h>
#include <windows.h>
#include <Wtsapi32.h>
#include <Userenv.h>

#pragma comment(lib, "userenv.lib")
#pragma comment(lib, "user32.lib")
#pragma comment(lib, "wtsapi32.lib")
#pragma comment(lib, "advapi32.lib")

void main(int argc, char* argv[]){
	HANDLE rh, wh, t = NULL;
	char cmd[512],buffer[257]; DWORD n;
	char* sessionId = getenv("SID");
	if(sessionId==NULL){sessionId="1";}
	if(argc<2){printf("SYNOPSIS : %s [cmd]", argv[0]);return;}
	SECURITY_ATTRIBUTES sa = {sizeof(SECURITY_ATTRIBUTES), NULL, TRUE}; 
	STARTUPINFO si = {0};si.cb = sizeof(STARTUPINFO);si.dwFlags = STARTF_USESTDHANDLES;
	PROCESS_INFORMATION pi = {0};
	if(!CreatePipe(&rh,&wh,&sa,0)){printf("CreatePipe failed !\n");return;}
	if(!WTSQueryUserToken(1, &t)){printf("WTSQueryUserToken failed !\n");return;}
	si.hStdOutput = wh;
	si.hStdError = wh;
	strncpy (cmd, GetCommandLine()+strlen(argv[0])+2, sizeof(cmd));
	if(!CreateProcessAsUser(t, NULL, cmd, NULL, NULL, TRUE, CREATE_NO_WINDOW, 0, NULL, &si, &pi)){printf("CreateProcessAsUser failed !");return;}
	printf("ProcessId : %d\n", pi.dwProcessId);
	CloseHandle(wh);
	WaitForSingleObject( pi.hProcess, INFINITE );
	while(TRUE){
        if (!ReadFile(rh, buffer, 256, &n, NULL)){break;}
        if (n>0){buffer[n]='\0';printf("%s", buffer);}
	}
}
```
##### NOTE
- `nt authority\system` **required**
- You can change session id by set `SID` environment variable, default is 1 (`console session`)

##### TODO
- [x] redirect stdout & stderr from child process

##### Credit 
[Grawity](https://gist.github.com/grawity/871048)
