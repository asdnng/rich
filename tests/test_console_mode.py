import unittest
from unittest.mock import MagicMock, patch, ANY
from ctypes import wintypes
from rich._win32_console import GetConsoleMode, LegacyWindowsError

branch_hit = {
    "Branch 1 (success)": False,
    "Branch 2 (failure)": False,
}

class TestGetConsoleMode(unittest.TestCase):

    @patch('rich._win32_console._GetConsoleMode')
    def test_get_console_mode_success(self, mock_get_console_mode):
        print("Testing Branch 1: Successful _GetConsoleMode call")
        mock_get_console_mode.return_value = True
        std_handle = MagicMock(spec=wintypes.HANDLE)

        result = GetConsoleMode(std_handle)
        branch_hit["Branch 1 (success)"] = True
        self.assertIsInstance(result, int)
        mock_get_console_mode.assert_called_once_with(std_handle, ANY)

    @patch('rich._win32_console._GetConsoleMode')
    def test_get_console_mode_failure(self, mock_get_console_mode):
        print("Testing Branch 2: Failed _GetConsoleMode call")
        mock_get_console_mode.return_value = False
        std_handle = MagicMock(spec=wintypes.HANDLE)

        with self.assertRaises(LegacyWindowsError) as context:
            GetConsoleMode(std_handle)
        branch_hit["Branch 2 (failure)"] = True
        self.assertEqual(str(context.exception), "Unable to get legacy Windows Console Mode")
        mock_get_console_mode.assert_called_once_with(std_handle, ANY)

    @classmethod
    def tearDownClass(cls):
        hits = sum(hit for hit in branch_hit.values())
        total_branches = len(branch_hit)
        coverage_percent = (hits / total_branches) * 100
        print(f"\nCoverage: {coverage_percent:.2f}%")
        for branch, hit in branch_hit.items():
            print(f"{branch} was {'hit' if hit else 'not hit'}")

if __name__ == "__main__":
    unittest.main()