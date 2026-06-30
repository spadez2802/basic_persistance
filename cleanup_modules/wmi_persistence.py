def check_wmi():
    """Kiểm tra WMI Event Subscription có tồn tại không"""
    try:
        import win32com.client
    except ImportError:
        return False
    
    filter_name = "DemoPersistenceFilter"
    try:
        wmi = win32com.client.GetObject("winmgmts:root\\subscription")
        filters = wmi.ExecQuery(f"Select * from __EventFilter where Name='{filter_name}'")
        return len(list(filters)) > 0
    except:
        return False

def remove_wmi():
    """Gỡ bỏ WMI Event Subscription"""
    if not check_wmi():
        print("[WMI Event Subscription]: Chưa được cài đặt (Không có gì để gỡ).")
        return
    
    try:
        import win32com.client
    except ImportError:
        print("[WMI Event Subscription]: Lỗi - Cần cài pywin32 (pip install pywin32)")
        return
    
    filter_name = "DemoPersistenceFilter"
    consumer_name = "DemoPersistenceConsumer"
    
    try:
        wmi = win32com.client.GetObject("winmgmts:root\\subscription")
        
        # ✅ Bước 1: Xóa Binding trước
        print("[WMI Event Subscription]: Đang xóa Binding...")
        try:
            bindings = wmi.ExecQuery(f"Select * from __FilterToConsumerBinding where Filter like '%{filter_name}%'")
            for binding in bindings:
                binding.Delete_()
        except:
            pass
        
        # ✅ Bước 2: Xóa Consumer
        print("[WMI Event Subscription]: Đang xóa Consumer...")
        try:
            consumers = wmi.ExecQuery(f"Select * from CommandLineEventConsumer where Name='{consumer_name}'")
            for consumer in consumers:
                consumer.Delete_()
        except:
            pass
        
        # ✅ Bước 3: Xóa Filter
        print("[WMI Event Subscription]: Đang xóa Filter...")
        try:
            filters = wmi.ExecQuery(f"Select * from __EventFilter where Name='{filter_name}'")
            for filter_obj in filters:
                filter_obj.Delete_()
        except:
            pass
        
        print("[WMI Event Subscription]: Đã gỡ bỏ thành công.")
    
    except Exception as e:
        print(f"[WMI Event Subscription]: Lỗi khi gỡ - {e}")
