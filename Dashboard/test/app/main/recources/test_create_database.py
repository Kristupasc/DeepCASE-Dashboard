from unittest import TestCase
from Dashboard.app.main.recources.create_database import *
import base64

class Test(TestCase):
    def test_parse_contents(self):
        file_text = open("create_database.txt", 'rb')
        file_read = file_text.read().decode()

        self.assertAlmostEqual(parse_contents(file_read,"test_123.csv", 0.0), 'File Uploaded Successfully: ' + "test_123.csv"+'' \
                                                     '\n\n\nPress "Start Security Analysis" button to run DeepCASE.')

        self.assertAlmostEqual(parse_contents(file_read,"test_123.csv", 0.0), 'File Uploaded Successfully: ' + "test_123.csv"+'' \
                                                     '\n\n\nPress "Start Security Analysis" button to run DeepCASE.')

