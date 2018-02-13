Run program in other Windows Terminal Session ~ `runas`
```C#
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;

class RunConsole {
	[DllImport("kernel32.dll")]
	static extern uint WTSGetActiveConsoleSessionId();
	[DllImport("wtsapi32.dll", SetLastError=true)]
	static extern bool WTSQueryUserToken(UInt32 sessionId, out IntPtr Token);
	[DllImport("userenv.dll", SetLastError=true)]
	static extern bool CreateEnvironmentBlock(out IntPtr lpEnvironment, IntPtr hToken, bool bInherit);
	[DllImport("advapi32.dll", SetLastError=true, CharSet=CharSet.Unicode)]
	static extern bool CreateProcessAsUser(
		IntPtr hToken,
		string lpApplicationName,
		string lpCommandLine,
		ref SECURITY_ATTRIBUTES lpProcessAttributes,
		ref SECURITY_ATTRIBUTES lpThreadAttributes,
		bool bInheritHandles,
		uint dwCreationFlags,
		IntPtr lpEnvironment,
		string lpCurrentDirectory,
		ref STARTUPINFO lpStartupInfo,
		out PROCESS_INFORMATION lpProcessInformation);
	
	[StructLayout(LayoutKind.Sequential)]
	public struct SECURITY_ATTRIBUTES
	{
		public int nLength;
		public IntPtr lpSecurityDescriptor;
		public int bInheritHandle;
	}
	[StructLayout(LayoutKind.Sequential)]
	internal struct PROCESS_INFORMATION
	{
		public IntPtr hProcess;
		public IntPtr hThread;
		public int dwProcessId;
		public int dwThreadId;
	}
	[StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
	struct STARTUPINFO
	{
		public Int32 cb;
		public string lpReserved;
		public string lpDesktop;
		public string lpTitle;
		public Int32 dwX;
		public Int32 dwY;
		public Int32 dwXSize;
		public Int32 dwYSize;
		public Int32 dwXCountChars;
		public Int32 dwYCountChars;
		public Int32 dwFillAttribute;
		public Int32 dwFlags;
		public Int16 wShowWindow;
		public Int16 cbReserved2;
		public IntPtr lpReserved2;
		public IntPtr hStdInput;
		public IntPtr hStdOutput;
		public IntPtr hStdError;
	}
	
	static int Main()
	{
	string Args0 = Environment.GetCommandLineArgs()[0];
	try {
		uint ConsoleSessionId = WTSGetActiveConsoleSessionId();// default : 1
		uint SessionId = 1;
		IntPtr hToken; WTSQueryUserToken(SessionId, out hToken);
		IntPtr lpEnvironment; CreateEnvironmentBlock(out lpEnvironment, hToken, false);
		SECURITY_ATTRIBUTES saProcessAttributes = new SECURITY_ATTRIBUTES();
		SECURITY_ATTRIBUTES saThreadAttributes = new SECURITY_ATTRIBUTES();
		STARTUPINFO startupInfo = new STARTUPINFO();
		PROCESS_INFORMATION processInfo;
		String cmd = Environment.CommandLine.Substring(Args0.Length).Trim();
		if(cmd.Length==0){
			Console.WriteLine("Usage : <{0}> <cmd>", Args0);
			return 0;
		}
		if (!CreateProcessAsUser(hToken, null, cmd, ref saProcessAttributes, ref saThreadAttributes, false, (uint)0x00000400/*CREATE_UNICODE_ENVIRONMENT*/, lpEnvironment, null, ref startupInfo, out processInfo))
		{
			Console.WriteLine("CreateProcessAsUser failed ! GGWP");
		}
		Console.WriteLine("Pid : "+processInfo.dwProcessId);
	}
	catch(Exception e){
		Console.WriteLine("Exception : "+e.GetType().Name);
	}
	return 0;
	}
}
```
##### Compile
https://www.nuget.org/packages/Microsoft.Net.Compilers

##### Notice

- `nt authority\system` **required**
- You can get Terminal Session ID by using `quser` ,`qwinsta` ,`tasklist`, ... and change `SessionId` accordingly

##### Credit 
[Grawity](https://gist.github.com/grawity/871048)
