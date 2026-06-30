import os
import sys
import ctypes

from cleanup_modules import (
    check_registry, remove_registry,
    check_registry_hklm, remove_registry_hklm,
    check_startup, remove_startup,
    check_schtasks, remove_schtasks,
    check_service, remove_service,
    check_wmi, remove_wmi
)

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

def verify_all():
    print("--- Trạng thái Persistence ---")
    print(f"1. Registry Run Key (HKCU): {'[CÓ]' if check_registry() else '[TRỐNG]'}")
    print(f"   Registry Run Key (HKLM): {'[CÓ]' if check_registry_hklm() else '[TRỐNG]'}")
    print(f"2. Startup Folder         : {'[CÓ]' if check_startup() else '[TRỐNG]'}")
    print(f"3. Scheduled Task   : {'[CÓ]' if check_schtasks() else '[TRỐNG]'}")
    print(f"4. Windows Service  : {'[CÓ]' if check_service() else '[TRỐNG]'}")
    print(f"5. WMI Event Subscription        : {'[CÓ]' if check_wmi() else '[TRỐNG]'}")
    print("------------------------------")

def main():
    request_admin()
    
    while True:
        print("\n=== MENU DỌN DẸP (CLEANUP) ===")
        print("1. Gỡ Registry Run Key (HKCU)")
        print("2. Gỡ Registry Run Key (HKLM)")
        print("3. Gỡ Startup Folder")
        print("4. Gỡ Scheduled Task")
        print("5. Gỡ Windows Service")
        print("6. Gỡ WMI Event Subscription")
        print("7. Kiểm tra tất cả (Verify All)")
        print("8. Thoát")
        
        choice = input("Vui lòng chọn (1-8): ")
        
        if choice == '1':
            remove_registry()
        elif choice == '2':
            remove_registry_hklm()
        elif choice == '3':
            remove_startup()
        elif choice == '4':
            remove_schtasks()
        elif choice == '5':
            remove_service()
        elif choice == '6':
            remove_wmi()
        elif choice == '7':
            verify_all()
        elif choice == '8':
            break
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == '__main__':
    main()