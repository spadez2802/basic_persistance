import subprocess

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
