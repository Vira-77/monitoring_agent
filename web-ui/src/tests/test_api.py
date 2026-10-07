import unittest 
from unittest.mock import patch
import asyncio
from utils.api import (
    get_cpu_data,
    get_cpu_name,
    get_memory_data,
    get_memory_data_free,
    get_memory_data_used,
    get_disk_data,
    get_log_data,
    get_hostname,
    clear_history,
    get_cpu_frequency,
    get_top_cpu_processes,
    get_cpu_historical,
    get_memory_historical,
    get_cpu_frequency_historical,
    get_total_errors,
    CPU_FREQUENCY_HISTORY,
    CPU_HISTORY,
    MEMORY_HISTORY
)
from utils.state import clear_state

class TestAPI(unittest.TestCase):
    def setUp(self):
        clear_state()
        clear_history()
        self.test_ip = '127.0.0.1'

    @patch('utils.api.fetch_data')
    def test_get_cpu_data_error(self, mock_fetch):
        mock_fetch.return_value = None
        result = asyncio.run(get_cpu_data(self.test_ip))
        self.assertIsNone(result)

    @patch('utils.api.fetch_data')
    def test_get_cpu_data_success(self, mock_fetch):
        mock_data = [{'usage': 50.0}, {'usage': 60.0}]
        mock_fetch.return_value = mock_data
        result = asyncio.run(get_cpu_data(self.test_ip))
        self.assertEqual(result, mock_data)

    @patch('utils.api.fetch_data')
    def test_get_cpu_name_error(self, mock_fetch):
        mock_fetch.return_value = None
        result = asyncio.run(get_cpu_name(self.test_ip))
        self.assertEqual(result, {'name': 'Unknown'})

    @patch('utils.api.fetch_data')
    def test_get_cpu_name_success(self, mock_fetch):
        mock_data = {'average_value': 'Intel i7'}
        mock_fetch.return_value = mock_data
        result = asyncio.run(get_cpu_name(self.test_ip))
        self.assertEqual(result, {'name': 'Intel i7'})

    @patch('utils.api.fetch_data')
    def test_get_memory_data_error(self, mock_fetch):
        mock_fetch.return_value = None
        result = asyncio.run(get_memory_data(self.test_ip))
        self.assertEqual(result, {'value': 0})

    @patch('utils.api.fetch_data')
    def test_get_memory_data_success(self, mock_fetch):
        mock_data = {'value': 75.5}
        mock_fetch.return_value = mock_data
        result = asyncio.run(get_memory_data(self.test_ip))
        self.assertEqual(result, mock_data)

    @patch('utils.api.fetch_data')
    def test_get_memory_data_free_error(self, mock_fetch):
        mock_fetch.return_value = None
        result = asyncio.run(get_memory_data_free(self.test_ip))
        self.assertIsNone(result)

    @patch('utils.api.fetch_data')
    def test_get_memory_data_free_success(self, mock_fetch):
        mock_data = {'value': 4096}
        mock_fetch.return_value = mock_data
        result = asyncio.run(get_memory_data_free(self.test_ip))
        self.assertIn('timestamp', result)
        self.assertEqual(result['value'], 4096)

    @patch('utils.api.fetch_data')
    def test_get_memory_data_used_error(self, mock_fetch):
        mock_fetch.return_value = None
        result = asyncio.run(get_memory_data_used(self.test_ip))
        self.assertIsNone(result)

    @patch('utils.api.fetch_data')
    def test_get_disk_data_error(self, mock_fetch):
        mock_fetch.return_value = None
        result = asyncio.run(get_disk_data(self.test_ip))
        self.assertEqual(result, {'percent': 0})

    @patch('utils.api.fetch_data')
    def test_get_log_data_error(self, mock_fetch):
        mock_fetch.return_value = None
        result = asyncio.run(get_log_data(self.test_ip))
        self.assertEqual(result, [])

    @patch('utils.api.fetch_data')
    def test_get_hostname_error(self, mock_fetch):
        mock_fetch.return_value = None
        result = asyncio.run(get_hostname(self.test_ip))
        self.assertEqual(result, {'hostname': 'Unknown'})

    @patch('utils.api.fetch_data')
    def test_get_cpu_frequency_success(self, mock_fetch):
        mock_data = [{'metric': 'frequency', 'number': 3200.0}]
        mock_fetch.return_value = mock_data
        result = asyncio.run(get_cpu_frequency(self.test_ip))
        self.assertEqual(result['frequency'], 3200.0)

    @patch('utils.api.fetch_data')
    def test_get_top_cpu_processes_success(self, mock_fetch):
        mock_data = [{'name': 'process1', 'cpu': 50}, {'name': 'process2', 'cpu': 30}]
        mock_fetch.return_value = mock_data
        result = asyncio.run(get_top_cpu_processes(self.test_ip))
        self.assertEqual(result, mock_data)

    def test_get_cpu_historical(self):
        test_data = {'timestamp': '12:00:00', 'usages': [50.0, 60.0]}
        CPU_HISTORY.append(test_data)
        result = get_cpu_historical()
        self.assertEqual(result, [test_data])

    def test_get_memory_historical(self):
        test_free = {'timestamp': '12:00:00', 'value': 4096}
        test_used = {'timestamp': '12:00:00', 'value': 4096}
        MEMORY_HISTORY['free'].append(test_free)
        MEMORY_HISTORY['used'].append(test_used)
        result = get_memory_historical()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['value'], 50.0)

    def test_get_cpu_frequency_historical(self):
        test_data = {'timestamp': '12:00:00', 'frequency': 3200.0}
        CPU_FREQUENCY_HISTORY.append(test_data)
        result = get_cpu_frequency_historical()
        self.assertEqual(result, [test_data])

    @patch('aiohttp.ClientSession.get')
    async def test_get_total_errors(self, mock_fetch):
        mock_data = {'value': 42}
        mock_fetch.return_value = mock_data
        result = asyncio.run(get_total_errors(self.test_ip))
        self.assertEqual(result, 42)

        # Test default case
        mock_fetch.return_value = None 
        result = asyncio.run(get_total_errors(self.test_ip))
        self.assertEqual(result, 0)

    def tearDown(self):
        clear_state()
        clear_history()

if __name__ == '__main__':
    unittest.main()