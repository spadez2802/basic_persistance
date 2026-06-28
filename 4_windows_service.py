import os
import sys
import ctypes
import subprocess

def request_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Đang yêu cầu quyền Admin (UAC)...")
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
        print(f"Lỗi: Không tìm thấy {app_path}.")
        os.system("pause")
        return

    try:
        service_name = "DemoPersistenceApp"
        
        # ✅ Xóa service cũ nếu tồn tại
        print("Kiểm tra service đã tồn tại...")
        subprocess.run(f'sc delete "{service_name}"', shell=True, capture_output=True)
        
        # ✅ Tạo service mới (cú pháp đúng)
        print("Đang cài đặt service...")
        cmd_create = f'sc create "{service_name}" binPath= "{app_path}" start= auto displayname= "Demo Persistence Service"'
        subprocess.run(cmd_create, shell=True, check=True)
        
        # ✅ Cấu hình mô tả (có check=True)
        print("Đang cấu hình mô tả...")
        subprocess.run(f'sc description "{service_name}" "Service demo persistence"', shell=True, check=True)
        
        # ✅ Khởi động service
        print("Đang khởi động service...")
        subprocess.run(f'sc start "{service_name}"', shell=True, check=True)
        
        print("✅ Thành công: Service đã cài đặt và khởi động!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi: {e}")

    os.system("pause")

if __name__ == '__main__':
    main()