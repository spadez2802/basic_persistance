import winreg
import os

def main():
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'app.exe')
    if not os.path.exists(app_path):
        print(f"Lỗi: Không tìm thấy {app_path}. Vui lòng chờ quá trình build hoàn tất.")
        return

    command = f'"{app_path}" --source Registry_Run_Key'
    
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_name = "DemoPersistenceApp"

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        print("Thành công: Đã thêm Registry Run Key!")
    except Exception as e:
        print(f"Thất bại: Lỗi thiết lập registry: {e}")

if __name__ == '__main__':
    main()
