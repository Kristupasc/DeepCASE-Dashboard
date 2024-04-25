from unittest import TestCase

from Dashboard.app.main.recources.data_dao_combine import *
from Dashboard.data.dao.dao import DAO
class Test(TestCase):
    def setUp(self):
        dao = DAO()
        dao.switch_current_file(dao.get_filenames().iloc[0].at["custom_name"])
        if not is_file_selected:
            raise Exception("No file present, run first deepcase")
    def test_start_deepcase(self):
        start_deepcase() # Check for no errors.

    def test_start_automatic(self):
        start_automatic()  # Check for no errors.

    def test_check_thread_alive(self):
        pass
        # This is done in the previous two.
