DASHBOARD_STATE = {
    'cpu_usage': [],
    'cpu_name': {'name': 'Unknown'},
    'hostname': {'hostname': 'Unknown'},
    'memory_used': {'timestamp': '00:00:00', 'value': 0},
    'memory_free': {'timestamp': '00:00:00', 'value': 0},
    'memory_percent': {'value': 0},
    'disk_usage': {'percent': 0},
    'top_processes': [],
    'cpu_frequency': {'timestamp': '00:00:00', 'frequency': 0},
    'logs': []
}

def is_different(new_data: any, old_data: any) -> bool:
    """Compare old and new data to detect changes"""
    if isinstance(new_data, (dict, list)) and isinstance(old_data, (dict, list)):
        return str(new_data) != str(old_data)
    return new_data != old_data

def update_state(key: str, new_data: any) -> bool:
    """Update state if data changed"""
    if is_different(new_data, DASHBOARD_STATE[key]):
        DASHBOARD_STATE[key] = new_data
        return True
    return False

def get_state(key: str) -> any:
    """Get current state for key"""
    return DASHBOARD_STATE.get(key)
def clear_state():
    global DASHBOARD_STATE
    DASHBOARD_STATE = {
        'cpu_usage': [],
        'cpu_name': {'name': 'Unknown'},
        'hostname': {'hostname': 'Unknown'},
        'memory_used': {'timestamp': '00:00:00', 'value': 0},
        'memory_free': {'timestamp': '00:00:00', 'value': 0},
        'memory_percent': {'value': 0},
        'disk_usage': {'percent': 0},
        'top_processes': [],
        'cpu_frequency': {'timestamp': '00:00:00', 'frequency': 0},
        'logs': []
    }