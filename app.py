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
    if not is_session_0():
        show_gui()
    else:
        time.sleep(30)

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
