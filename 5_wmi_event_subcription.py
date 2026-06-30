import os
import sys
import ctypes

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
    
    try:
        import win32com.client
    except ImportError:
        print("Lỗi: Cần cài pywin32")
        print("Chạy: pip install pywin32")
        os.system("pause")
        return
    
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'app.exe')
    if not os.path.exists(app_path):
        print(f"Lỗi: Không tìm thấy {app_path}.")
        os.system("pause")
        return

    try:
        # ✅ Kết nối tới WMI
        print("Kết nối tới WMI...")
        wmi = win32com.client.GetObject("winmgmts:root\\subscription")
        
        # ✅ 1. Tạo Event Filter (lắng nghe sự kiện)
        print("\n1️⃣  Tạo Event Filter...")
        filter_name = "DemoPersistenceFilter"
        filter_query = 'SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA "Win32_PerfFormattedData_PerfOS_System"'
        # Mỗi 60 giây, system metrics thay đổi → trigger event
        
        # Xóa filter cũ nếu tồn tại
        wmi.ExecQuery(f"Select * from __EventFilter where Name='{filter_name}'")
        
        filter_class = wmi.Get("__EventFilter")
        filter_instance = filter_class.SpawnInstance_()
        filter_instance.Name = filter_name
        filter_instance.QueryLanguage = "WQL"
        filter_instance.Query = filter_query
        filter_path = filter_instance.Put_()
        print(f"✅ Event Filter tạo thành công: {filter_path}")
        
        # ✅ 2. Tạo Event Consumer (action cần thực hiện)
        print("\n2️⃣  Tạo Event Consumer...")
        consumer_name = "DemoPersistenceConsumer"
        
        consumer_class = wmi.Get("CommandLineEventConsumer")
        consumer_instance = consumer_class.SpawnInstance_()
        consumer_instance.Name = consumer_name
        consumer_instance.CommandLineTemplate = app_path
        consumer_instance.RunInteractively = False
        consumer_path = consumer_instance.Put_()
        print(f"✅ Event Consumer tạo thành công: {consumer_path}")
        
        # ✅ 3. Tạo FilterToConsumerBinding (liên kết Filter + Consumer)
        print("\n3️⃣  Tạo FilterToConsumerBinding...")
        binding_class = wmi.Get("__FilterToConsumerBinding")
        binding_instance = binding_class.SpawnInstance_()
        binding_instance.Filter = filter_path
        binding_instance.Consumer = consumer_path
        binding_path = binding_instance.Put_()
        print(f"✅ Binding tạo thành công: {binding_path}")
        
        # ✅ 4. Kiểm tra
        print("\n4️⃣  Kiểm tra hoạt động...")
        filters = wmi.ExecQuery(f"Select * from __EventFilter where Name='{filter_name}'")
        consumers = wmi.ExecQuery(f"Select * from CommandLineEventConsumer where Name='{consumer_name}'")
        bindings = wmi.ExecQuery(f"Select * from __FilterToConsumerBinding where Filter='{filter_path}'")
        
        print(f"Filters tìm thấy: {len(list(filters))}")
        print(f"Consumers tìm thấy: {len(list(consumers))}")
        print(f"Bindings tìm thấy: {len(list(bindings))}")
        
        print("\n✅ Thành công: WMI Event Subscription đã được cài đặt!")
        print(f"   - Filter: {filter_name}")
        print(f"   - Consumer: {consumer_name}")
        print(f"   - Event sẽ trigger mỗi 60 giây")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

    os.system("pause")

if __name__ == '__main__':
    main()