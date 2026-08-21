import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import churn

class TestChurn(unittest.TestCase):
    @patch('churn.subprocess.run')
    def test_get_file_churn(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout="""
            file1.py
            file1.py
            file2.py
            """,
            returncode=0
        )
        
        result = churn.get_file_churn(".", 30)
        self.assertEqual(result["file1.py"], 2)
        self.assertEqual(result["file2.py"], 1)

    def test_identify_hotspots(self):
        counts = {"a.py": 10, "b.py": 2, "c.py": 5}
        hotspots = churn.identify_hotspots(counts, threshold_percentile=50)
        self.assertIn("a.py", hotspots)

if __name__ == '__main__':
    unittest.main()
