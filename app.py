import os
import sys
import ctypes
import datetime
import argparse
import getpass
import time
import win32serviceutil
import win32service
import win32event
import servicemanager

def is_session_0():
    try:
        session_id = ctypes.c_uint32()
        process_id = ctypes.windll.kernel32.GetCurrentProcessId()
        if ctypes.windll.kernel32.ProcessIdToSessionId(process_id, ctypes.byref(session_id)):
            return session_id.value == 0
    except Exception:
        pass
    return os.environ.get('USERNAME', '').upper() == 'SYSTEM'

def write_log(source):
    try:
        log_path = r"C:\Users\hehe123\Desktop\run_log.txt"
        fallback_path = r"C:\Users\Public\Desktop\run_log.txt"
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = os.environ.get('USERNAME', 'SYSTEM')
        
        log_msg = f"{now_str} | Phương thức: {source} | User: {username}\n"
        
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(log_msg)
        except:
            with open(fallback_path, "a", encoding="utf-8") as f:
                f.write(log_msg)
    except Exception as e:
        pass

def launch_in_active_session():
    """Re-launch app.exe vào session của user đang đăng nhập (Session 1/2) từ Session 0"""
    try:
        import ctypes.wintypes

        STARTF_USESHOWWINDOW = 0x00000001
        CREATE_UNICODE_ENVIRONMENT = 0x00000400
        SW_SHOW = 5
        TOKEN_ALL_ACCESS = 0xF01FF
        SecurityImpersonation = 2
        TokenPrimary = 1

        class STARTUPINFO(ctypes.Structure):
            _fields_ = [
                ('cb', ctypes.wintypes.DWORD), ('lpReserved', ctypes.wintypes.LPWSTR),
                ('lpDesktop', ctypes.wintypes.LPWSTR), ('lpTitle', ctypes.wintypes.LPWSTR),
                ('dwX', ctypes.wintypes.DWORD), ('dwY', ctypes.wintypes.DWORD),
                ('dwXSize', ctypes.wintypes.DWORD), ('dwYSize', ctypes.wintypes.DWORD),
                ('dwXCountChars', ctypes.wintypes.DWORD), ('dwYCountChars', ctypes.wintypes.DWORD),
                ('dwFillAttribute', ctypes.wintypes.DWORD), ('dwFlags', ctypes.wintypes.DWORD),
                ('wShowWindow', ctypes.wintypes.WORD), ('cbReserved2', ctypes.wintypes.WORD),
                ('lpReserved2', ctypes.wintypes.LPBYTE),
                ('hStdInput', ctypes.wintypes.HANDLE), ('hStdOutput', ctypes.wintypes.HANDLE),
                ('hStdError', ctypes.wintypes.HANDLE),
            ]

        class PROCESS_INFORMATION(ctypes.Structure):
            _fields_ = [
                ('hProcess', ctypes.wintypes.HANDLE), ('hThread', ctypes.wintypes.HANDLE),
                ('dwProcessId', ctypes.wintypes.DWORD), ('dwThreadId', ctypes.wintypes.DWORD),
            ]

        # Lấy session ID của console user đang đăng nhập (Session 1 hoặc 2)
        active_session = ctypes.windll.kernel32.WTSGetActiveConsoleSessionId()

        # Lấy token của user trong session đó
        h_token = ctypes.wintypes.HANDLE()
        ctypes.windll.wtsapi32.WTSQueryUserToken(active_session, ctypes.byref(h_token))

        # Duplicate token thành Primary token
        h_dup = ctypes.wintypes.HANDLE()
        ctypes.windll.advapi32.DuplicateTokenEx(
            h_token, TOKEN_ALL_ACCESS, None,
            SecurityImpersonation, TokenPrimary, ctypes.byref(h_dup)
        )

        # Tạo environment block cho user
        lp_env = ctypes.c_void_p()
        ctypes.windll.userenv.CreateEnvironmentBlock(ctypes.byref(lp_env), h_dup, False)

        # Đường dẫn exe hiện tại
        exe_path = sys.argv[0]
        cmd = f'"{exe_path}" --source WMI'

        si = STARTUPINFO()
        si.cb = ctypes.sizeof(si)
        si.lpDesktop = "winsta0\\default"
        si.dwFlags = STARTF_USESHOWWINDOW
        si.wShowWindow = SW_SHOW
        pi = PROCESS_INFORMATION()

        ctypes.windll.advapi32.CreateProcessAsUserW(
            h_dup, None, cmd, None, None, False,
            CREATE_UNICODE_ENVIRONMENT, lp_env, None,
            ctypes.byref(si), ctypes.byref(pi)
        )

        ctypes.windll.userenv.DestroyEnvironmentBlock(lp_env)
        ctypes.windll.kernel32.CloseHandle(h_token)
        ctypes.windll.kernel32.CloseHandle(h_dup)
        if pi.hProcess: ctypes.windll.kernel32.CloseHandle(pi.hProcess)
        if pi.hThread:  ctypes.windll.kernel32.CloseHandle(pi.hThread)
    except Exception:
        pass


def show_gui():
    import tkinter as tk

    
    root = tk.Tk()
    root.title("Thông báo")
    root.attributes('-topmost', True)
    
    window_width = 300
    window_height = 80
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Màn hình ở góc phải dưới (trên taskbar một chút)
    x = screen_width - window_width - 20
    y = screen_height - window_height - 60 
    
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    root.configure(bg='#2b2b2b')
    
    lbl = tk.Label(root, text="thử nghiệm chương trình", fg='white', bg='#2b2b2b', font=('Arial', 14))
    lbl.pack(expand=True)
    
    # Đóng sau 10 giây (10000 ms)
    root.after(10000, root.destroy)
    root.mainloop()

class AppService(win32serviceutil.ServiceFramework):
    _svc_name_ = "DemoPersistenceApp"
    _svc_display_name_ = "Demo Persistence Service"
    _svc_description_ = "Service demo persistence"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        write_log("Windows Service")
        while self.is_running:
            rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
            if rc == win32event.WAIT_OBJECT_0:
                break

def run_app(source):
    write_log(source)
    if is_session_0():
        # Đang ở Session 0 (WMI/Service) → re-launch vào session của user để hiện GUI
        launch_in_active_session()
    else:
        # Đang ở Session 1/2 (user session) → hiện GUI bình thường
        show_gui()

def main():
    # If run without arguments, try to see if it's started by Service Control Manager
    if len(sys.argv) == 1:
        try:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(AppService)
            servicemanager.StartServiceCtrlDispatcher()
            return
        except Exception as e:
            # Error 1063 means not started by SCM
            pass

    # Manually parse --source
    source = "Direct Run"
    for i in range(len(sys.argv)):
        if sys.argv[i] == "--source" and i + 1 < len(sys.argv):
            source = sys.argv[i+1]
            break

    # If it's pywin32 standard args for service install/start/stop/remove
    if len(sys.argv) > 1 and sys.argv[1] in ['install', 'update', 'remove', 'start', 'stop', 'restart', 'debug']:
        win32serviceutil.HandleCommandLine(AppService)
        return

    # Normal execution
    run_app(source)

if __name__ == '__main__':
    main()
