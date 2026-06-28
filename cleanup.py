import os
import sys
import ctypes
import winreg
import subprocess

def request_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Đang yêu cầu quyền Admin (UAC) để thực hiện Cleanup...")
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

def check_registry():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_name = "DemoPersistenceApp"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, key_name)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except Exception:
        return False

def remove_registry():
    if not check_registry():
        print("[Registry Run Key]: Chưa được cài đặt (Không có gì để gỡ).")
        return
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_name = "DemoPersistenceApp"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, key_name)
        winreg.CloseKey(key)
        print("[Registry Run Key]: Đã gỡ bỏ thành công.")
    except Exception as e:
        print(f"[Registry Run Key]: Lỗi khi gỡ - {e}")

def check_startup():
    startup_folder = os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup')
    shortcut_path = os.path.join(startup_folder, 'DemoPersistenceApp.lnk')
    return os.path.exists(shortcut_path)

def remove_startup():
    if not check_startup():
        print("[Startup Folder]: Chưa được cài đặt (Không có gì để gỡ).")
        return
    startup_folder = os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup')
    shortcut_path = os.path.join(startup_folder, 'DemoPersistenceApp.lnk')
    try:
        os.remove(shortcut_path)
        print("[Startup Folder]: Đã gỡ bỏ thành công.")
    except Exception as e:
        print(f"[Startup Folder]: Lỗi khi gỡ - {e}")

def check_schtasks():
    task_name = "DemoPersistenceAppTask"
    cmd = f'schtasks /Query /TN "{task_name}"'
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except:
        return False

def remove_schtasks():
    if not check_schtasks():
        print("[Scheduled Task]: Chưa được cài đặt (Không có gì để gỡ).")
        return
    task_name = "DemoPersistenceAppTask"
    cmd = f'schtasks /Delete /TN "{task_name}" /F'
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[Scheduled Task]: Đã gỡ bỏ thành công.")
    except Exception as e:
        print(f"[Scheduled Task]: Lỗi khi gỡ - {e}")

def check_service():
    service_name = "DemoPersistenceApp"
    cmd = f'sc query "{service_name}"'
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except:
        return False

def remove_service():
    if not check_service():
        print("[Windows Service]: Chưa được cài đặt (Không có gì để gỡ).")
        return
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'app.exe')
    try:
        if os.path.exists(app_path):
            subprocess.run([app_path, "stop"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run([app_path, "remove"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(f'sc stop "DemoPersistenceApp"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(f'sc delete "DemoPersistenceApp"', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[Windows Service]: Đã gỡ bỏ thành công.")
    except Exception as e:
        print(f"[Windows Service]: Lỗi khi gỡ - {e}")

def verify_all():
    print("--- Trạng thái Persistence ---")
    print(f"1. Registry Run Key : {'[CÓ]' if check_registry() else '[TRỐNG]'}")
    print(f"2. Startup Folder   : {'[CÓ]' if check_startup() else '[TRỐNG]'}")
    print(f"3. Scheduled Task   : {'[CÓ]' if check_schtasks() else '[TRỐNG]'}")
    print(f"4. Windows Service  : {'[CÓ]' if check_service() else '[TRỐNG]'}")
    print("------------------------------")

def main():
    request_admin()
    
    while True:
        print("\n=== MENU DỌN DẸP (CLEANUP) ===")
        print("1. Gỡ Registry Run Key")
        print("2. Gỡ Startup Folder")
        print("3. Gỡ Scheduled Task")
        print("4. Gỡ Windows Service")
        print("5. Kiểm tra tất cả (Verify All)")
        print("6. Thoát")
        
        choice = input("Vui lòng chọn (1-6): ")
        
        if choice == '1':
            remove_registry()
        elif choice == '2':
            remove_startup()
        elif choice == '3':
            remove_schtasks()
        elif choice == '4':
            remove_service()
        elif choice == '5':
            verify_all()
        elif choice == '6':
            break
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == '__main__':
    main()
