import os
import sys
import ctypes
import subprocess

def request_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Đang yêu cầu quyền Admin (UAC) để cấu hình Scheduled Task...")
        try:
            # sys.executable is python.exe
            args = " ".join([f'"{arg}"' for arg in sys.argv])
            ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, None, 1)
            if ret <= 32:
                print("Lỗi: Người dùng từ chối cấp quyền Admin.")
                os.system("pause")
            sys.exit()
        except Exception as e:
            print(f"Lỗi xin quyền: {e}")
            sys.exit()

def main():
    request_admin()
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'app.exe')
    if not os.path.exists(app_path):
        print(f"Lỗi: Không tìm thấy {app_path}. Vui lòng chờ quá trình build hoàn tất.")
        os.system("pause")
        return

    task_name = "DemoPersistenceAppTask"
    
    # Lệnh tạo scheduled task chạy ngầm mỗi khi user logon bằng quyền cao nhất (RL HIGHEST = Admin)
    cmd = f'schtasks /Create /TN "{task_name}" /TR "\\"{app_path}\\" --source Scheduled_Task" /SC ONLOGON /F /RL HIGHEST'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("Thành công: Đã tạo và cấu hình Scheduled Task (DemoPersistenceAppTask)!")
    except subprocess.CalledProcessError as e:
        print(f"Thất bại: Lỗi khi tạo scheduled task: {e}")
    
    os.system("pause")

if __name__ == '__main__':
    main()
