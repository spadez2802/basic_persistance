from .registry import check_registry, remove_registry, check_registry_hklm, remove_registry_hklm
from .startup import check_startup, remove_startup
from .schtasks import check_schtasks, remove_schtasks
from .service import check_service, remove_service
from .wmi_persistence import check_wmi, remove_wmi

__all__ = [
    'check_registry', 'remove_registry',
    'check_registry_hklm', 'remove_registry_hklm',
    'check_startup', 'remove_startup',
    'check_schtasks', 'remove_schtasks',
    'check_service', 'remove_service',
    'check_wmi', 'remove_wmi'
]
