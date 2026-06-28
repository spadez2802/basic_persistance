import os
import sys
import win32com.client

def main():
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'app.exe')
    if not os.path.exists(app_path):
        print(f"Lỗi: Không tìm thấy {app_path}. Vui lòng chờ quá trình build hoàn tất.")
        return

    startup_folder = os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs\Startup')
    shortcut_path = os.path.join(startup_folder, 'DemoPersistenceApp.lnk')

    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = app_path
        shortcut.Arguments = '--source Startup_Folder'
        shortcut.WorkingDirectory = os.path.dirname(app_path)
        shortcut.save()
        print(f"Thành công: Đã tạo file shortcut trong Startup folder: {shortcut_path}")
    except Exception as e:
        print(f"Thất bại: Lỗi khi tạo shortcut: {e}")

if __name__ == '__main__':
    main()
