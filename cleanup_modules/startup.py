import os

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
