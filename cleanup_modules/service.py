import os
import subprocess

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
    
    # get app path relative to cleanup.py or cwd
    app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dist', 'app.exe')
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
