import winreg

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

def check_registry_hklm():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_name = "DemoPersistenceApp_HKLM"
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        winreg.QueryValueEx(key, key_name)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        try:
            # Fallback 32bit if needed
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
            winreg.QueryValueEx(key, key_name)
            winreg.CloseKey(key)
            return True
        except:
            return False
    except Exception:
        return False

def remove_registry_hklm():
    if not check_registry_hklm():
        print("[Registry Run Key HKLM]: Chưa được cài đặt (Không có gì để gỡ).")
        return
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_name = "DemoPersistenceApp_HKLM"
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.DeleteValue(key, key_name)
        winreg.CloseKey(key)
        print("[Registry Run Key HKLM]: Đã gỡ bỏ thành công.")
    except Exception as e:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_32KEY)
            winreg.DeleteValue(key, key_name)
            winreg.CloseKey(key)
            print("[Registry Run Key HKLM]: Đã gỡ bỏ thành công.")
        except Exception as e2:
            print(f"[Registry Run Key HKLM]: Lỗi khi gỡ - {e2}")
