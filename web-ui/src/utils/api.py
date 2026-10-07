import aiohttp
from typing import Dict, List
from datetime import datetime
import asyncio
from utils.state import update_state, get_state

CPU_HISTORY = []
MEMORY_HISTORY = {
    'free': [],
    'used': []
}
CPU_FREQUENCY_HISTORY = []
MAX_HISTORY_SIZE = 40


def update_history(history_list, new_data):
    history_list.append(new_data)
    if len(history_list) > MAX_HISTORY_SIZE:
        history_list.pop(0)
    return history_list

def update_memory_history(type_key, data):
    """Helper function to update memory history"""
    timestamp = data.get('timestamp')
    value = float(data.get('value', 0))
    
    MEMORY_HISTORY[type_key].append({
        'timestamp': timestamp,
        'value': value
    })
    
    if len(MEMORY_HISTORY[type_key]) > MAX_HISTORY_SIZE:
        MEMORY_HISTORY[type_key].pop(0)

def clear_history():
    CPU_HISTORY.clear()
    MEMORY_HISTORY['free'].clear()
    MEMORY_HISTORY['used'].clear()
    CPU_FREQUENCY_HISTORY.clear()

DEFAULT_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 1

async def fetch_data(session, url, timeout=DEFAULT_TIMEOUT, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            timeout_config = aiohttp.ClientTimeout(
                total=timeout,
                connect=timeout/2,
                sock_read=timeout
            )
            
            async with session.get(url, timeout=timeout_config) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Attempt {attempt + 1}/{max_retries}: Failed to fetch data from {url}: Status {response.status}")
                    
        except asyncio.TimeoutError:
            print(f"Attempt {attempt + 1}/{max_retries}: Timeout when fetching data from {url}")
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Error fetching data from {url}: {str(e)}")
            
        if attempt < max_retries - 1:
            await asyncio.sleep(RETRY_DELAY)
            
    return None

async def get_cpu_data(IP_ADDRESS: str) -> List[Dict]:
    if "http" not in IP_ADDRESS:
        IP_ADDRESS = "http://" + IP_ADDRESS
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, f"{IP_ADDRESS}/metrics/v1/cpu/usage")
        if data:
            usages = [float(cpu['usage']) for cpu in data]
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            history_data = {
                'timestamp': timestamp,
                'usages': usages 
            }
            if update_state('cpu_usage', data):
                update_history(CPU_HISTORY, history_data)
            return get_state('cpu_usage')
        return None

async def get_memory_data(IP_ADDRESS: str) -> Dict:
    if "http" not in IP_ADDRESS:
        IP_ADDRESS = "http://" + IP_ADDRESS
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, f"{IP_ADDRESS}/metrics/v1/ram/percent")
        if data:
            update_state('memory_percent', data)
            return data
        else:
            default_data = {'value': 0}
            update_state('memory_percent', default_data)
            return default_data

async def get_memory_data_free(IP_ADDRESS: str) -> Dict:
    if "http" not in IP_ADDRESS:
        IP_ADDRESS = "http://" + IP_ADDRESS
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, f"{IP_ADDRESS}/metrics/v1/ram/free")
        if data:
            data['timestamp'] = datetime.now().strftime('%H:%M:%S')
            if update_state('memory_free', data):
                update_memory_history('free', data)
            return get_state('memory_free')
        return None

async def get_memory_data_used(IP_ADDRESS: str) -> Dict:
    if "http" not in IP_ADDRESS:
        IP_ADDRESS = "http://" + IP_ADDRESS
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, f"{IP_ADDRESS}/metrics/v1/ram/used")
        if data:
            data['timestamp'] = datetime.now().strftime('%H:%M:%S')
            if update_state('memory_used', data):
                update_memory_history('used', data)
            return get_state('memory_used')
        return None

async def get_disk_data(IP_ADDRESS: str) -> Dict:
    if "http" not in IP_ADDRESS:
        IP_ADDRESS = "http://" + IP_ADDRESS
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, f"{IP_ADDRESS}/metrics/v1/disk/usage")
        if data:
            update_state('disk_usage', data)
            return data
        else:
            default_data = {'percent': 0}
            update_state('disk_usage', default_data)
            return default_data

async def get_log_data(IP_ADDRESS: str) -> List[Dict]:
    if "http" not in IP_ADDRESS:
        IP_ADDRESS = "http://" + IP_ADDRESS
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, f"{IP_ADDRESS}/metrics/v1/logs/last_errors")
        if data:
            update_state('logs', data)
            return data
        else:
            update_state('logs', [])
            return []
        
async def get_cpu_name(IP_ADDRESS: str) -> Dict:
    if "http" not in IP_ADDRESS:
        IP_ADDRESS = "http://" + IP_ADDRESS
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, f"{IP_ADDRESS}/metrics/v1/cpu/name")
        if data:
            processed_data = {'name': data.get('average_value', 'Unknown')}
            update_state('cpu_name', processed_data)
            return processed_data
        else:
            default_data = {'name': 'Unknown'}
            update_state('cpu_name', default_data)
            return default_data

async def get_hostname(IP_ADDRESS: str) -> Dict:
    if "http" not in IP_ADDRESS:
        IP_ADDRESS = "http://" + IP_ADDRESS
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, f"{IP_ADDRESS}/hostname")
        if data:
            update_state('hostname', data)
            return {"hostname": data.get("value", "Unknown")}
        else:
            default_data = {'hostname': "Unknown"}
            update_state('hostname', default_data)
            return default_data
async def get_top_cpu_processes(IP_ADDRESS: str) -> List[Dict]:
    if "http" not in IP_ADDRESS:
        IP_ADDRESS = "http://" + IP_ADDRESS
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, f"{IP_ADDRESS}/metrics/v1/logs/topprocesses")
        if data:
            update_state('top_processes', data)
            return data
        return []
async def get_total_errors(IP_ADDRESS: str) -> Dict:
    if "http" not in IP_ADDRESS:
        IP_ADDRESS = "http://" + IP_ADDRESS
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, f"{IP_ADDRESS}/metrics/v1/logs/error_count")
        if data:
            return data.get('value', 0)
        else:
            default_data = {'value': 0}
            return default_data
        
async def get_cpu_frequency(IP_ADDRESS: str) -> Dict:
    if "http" not in IP_ADDRESS:
        IP_ADDRESS = "http://" + IP_ADDRESS
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, f"{IP_ADDRESS}/metrics/v1/cpu/frequency")
        if data and isinstance(data, list):
            frequency_value = next(
                (item['number'] for item in data if item['metric'] == 'frequency'),
                0
            )
            timestamp = datetime.now().strftime('%H:%M:%S')
            frequency_data = {
                'timestamp': timestamp,
                'frequency': float(frequency_value)
            }
            if update_state('cpu_frequency', frequency_data):
                update_history(CPU_FREQUENCY_HISTORY, frequency_data)
            return get_state('cpu_frequency')
        return None
        
def get_cpu_historical():
    return CPU_HISTORY

def get_memory_historical():
    temp = []
    free_history = MEMORY_HISTORY['free']
    used_history = MEMORY_HISTORY['used']
    
    history_length = min(len(free_history), len(used_history))
    
    for i in range(history_length):
        try:
            timestamp = free_history[i]['timestamp']
            free = float(free_history[i]['value'])
            used = float(used_history[i]['value'])
            total = free + used
            
            memory_percent = (used / total) * 100 if total > 0 else 0
            temp.append({'timestamp': timestamp, 'value': memory_percent})
            
        except (KeyError, TypeError, ValueError) as e:
            print(f"Error processing memory data: {e}")
            continue
            
    return temp

def get_cpu_frequency_historical():
    return CPU_FREQUENCY_HISTORY
