import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from schedule_automation import schedule

class TestExtractShifts(unittest.TestCase):
    def setUp(self):
        self.no_shifts = {
                'Friday': [],
                'Sunday': [],
                'Monday': [],
                'Saturday': [],
                'Thursday': [],
                'Wednesday': [],
                'Tuesday': []
                }
        self.one_shift = {
                'Friday': [],
                'Sunday': [],
                'Monday': ["9am - 1pm Pre Game Set-Up"],
                'Saturday': [],
                'Thursday': [],
                'Wednesday': [],
                'Tuesday': []
                }
    def test_extract_shifts(self):
        pass

if __name__ == "__main__":
    unittest.main()
