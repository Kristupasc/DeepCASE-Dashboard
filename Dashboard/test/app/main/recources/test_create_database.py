from unittest import TestCase
from Dashboard.app.main.recources.create_database import *
import base64

class Test(TestCase):
    def test_parse_contents(self):
        file_text = open("C:\\Users\marij\PycharmProjects\M11_3\DeepCASE-Dashboard\Dashboard\\app\main\server.py", 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        parse_contents(file_encode,"test_123", 0.0)

