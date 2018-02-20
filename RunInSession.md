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
	char* sessionId = getenv("SID");
	if(sessionId==NULL){sessionId="1";}
	if(argc<2){printf("SYNOPSIS : %s [cmd]", argv[0]);exit(0);}
	HANDLE t = NULL;
	LPVOID eb = NULL; 
	PROCESS_INFORMATION pi = {0};
	STARTUPINFO si = {0};
	char cmd[512];
	strncpy (cmd, GetCommandLine()+strlen(argv[0])+2, sizeof(cmd));
	if(!WTSQueryUserToken(atoi(sessionId), &t)){
		printf("WTSQueryUserToken failed!");exit(1);
	}
	if(!CreateEnvironmentBlock(&eb, t, FALSE)){
		printf("CreateEnvironmentBlock failed!");exit(1);
	}
	if (!CreateProcessAsUser(t, NULL, cmd, NULL, NULL, FALSE, CREATE_UNICODE_ENVIRONMENT, eb, NULL, &si, &pi))
	{
		printf("CreateProcessAsUser failed!");exit(1);
	}
	printf("PID : %d", pi.dwProcessId);
}
```
##### Notice

- `nt authority\system` **required**
- You can change session id by set `SID` environment variable, default is 1 (`console session`)

##### Credit 
[Grawity](https://gist.github.com/grawity/871048)
