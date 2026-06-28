import os
import sys
import ctypes
import subprocess

def request_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Đang yêu cầu quyền Admin (UAC) để đăng ký Windows Service...")
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

    try:
        # Sử dụng pywin32 module tích hợp trong app.exe để cài đặt service
        print("Đang cài đặt service...")
        subprocess.run([app_path, "install", "--startup=auto"], check=True)
        
        print("Đang khởi động service...")
        subprocess.run([app_path, "start"], check=True)
        
        print("Thành công: Windows Service đã được cài đặt và khởi động (tự chạy ngầm).")
    except subprocess.CalledProcessError as e:
        print(f"Thất bại: Có lỗi xảy ra trong quá trình cấu hình service: {e}")

    os.system("pause")

if __name__ == '__main__':
    main()
