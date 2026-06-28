import winreg
import os
import sys
import ctypes

def request_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Đang yêu cầu quyền Admin (UAC) để thiết lập HKLM Registry Run Key...")
        try:
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

    command = f'"{app_path}" --source Registry_Run_Key_HKLM'
    
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_name = "DemoPersistenceApp_HKLM"

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        print(f"Thành công: Đã thêm Registry Run Key vào HKLM (All Users)!\nĐường dẫn: HKEY_LOCAL_MACHINE\\{key_path}\nKhóa: {key_name}")
    except Exception as e:
        print(f"Thất bại: Lỗi thiết lập registry: {e}")
        
    os.system("pause")

if __name__ == '__main__':
    main()
