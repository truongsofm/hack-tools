Run program in other Windows Terminal Session 
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

	[Flags]
	enum CreateProcessFlags : uint
	{
		CREATE_BREAKAWAY_FROM_JOB			= 0x01000000,
		CREATE_DEFAULT_ERROR_MODE			= 0x04000000,
		CREATE_NEW_CONSOLE					= 0x00000010,
		CREATE_NEW_PROCESS_GROUP				= 0x00000200,
		CREATE_NO_WINDOW						= 0x08000000,
		CREATE_PROTECTED_PROCESS				= 0x00040000,
		CREATE_PRESERVE_CODE_AUTHZ_LEVEL	= 0x02000000,
		CREATE_SEPARATE_WOW_VDM			= 0x00000800,
		CREATE_SHARED_WOW_VDM				= 0x00001000,
		CREATE_SUSPENDED						= 0x00000004,
		CREATE_UNICODE_ENVIRONMENT			= 0x00000400,
		DEBUG_ONLY_THIS_PROCESS				= 0x00000002,
		DEBUG_PROCESS							= 0x00000001,
		DETACHED_PROCESS						= 0x00000008,
		EXTENDED_STARTUPINFO_PRESENT		= 0x00080000,
		INHERIT_PARENT_AFFINITY				= 0x00010000,
	}
	
	static int Main()
	{
	string Args0 = Environment.GetCommandLineArgs()[0];
	try {
		uint ConsoleSessionId = WTSGetActiveConsoleSessionId();// 1 by default
		uint SessionId = 1;
		IntPtr hToken; WTSQueryUserToken(SessionId, out hToken);
		IntPtr lpEnvironment; CreateEnvironmentBlock(out lpEnvironment, hToken, false);
		SECURITY_ATTRIBUTES saProcessAttributes = new SECURITY_ATTRIBUTES();
		SECURITY_ATTRIBUTES saThreadAttributes = new SECURITY_ATTRIBUTES();
		STARTUPINFO startupInfo = new STARTUPINFO();
		PROCESS_INFORMATION processInfo;
		CreateProcessFlags flags = 0;
		flags |= CreateProcessFlags.CREATE_UNICODE_ENVIRONMENT;//!importaint
		String cmd = Environment.CommandLine.Substring(Args0.Length).Trim();//work with quoted parameter
		if(cmd.Length==0){
			Console.WriteLine("Usage : <{0}> <cmd>", Args0);
			return 0;
		}
		if (CreateProcessAsUser(hToken, null, cmd, ref saProcessAttributes, ref saThreadAttributes, false, (uint)flags, lpEnvironment, null, ref startupInfo, out processInfo))
		{
			Console.WriteLine("PID = "+processInfo.dwProcessId);
		}
		else {
			Console.WriteLine("`nt authority\\system` required");
		}
	}
	catch(Exception e){
		Console.WriteLine("Got Exception "+e.GetType().Name);
	}
	return 0;
	}
}
```

Credit : [Grawity](https://gist.github.com/grawity/871048)