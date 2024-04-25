from unittest import TestCase

from Dashboard.app.main.recources.data_dao_combine import *
from Dashboard.data.dao.dao import DAO


class Test(TestCase):
    def setUp(self):
        if not is_file_selected:
            raise Exception("No file present, run first deepcase")
    def test_get_files(self):
        self.assertTrue(get_files().shape[0] >=1)
        self.assertTrue(get_files().shape[1] == 1)

    def test_switch_file(self):
        dao = DAO()
        dao.switch_current_file(get_files().iloc[0].at["custom_name"])
        self.assertTrue(is_file_selected)

    def test_get_status_file(self):
        dao = DAO()
        dao.switch_current_file(get_files().iloc[0].at["custom_name"])
        self.assertTrue(get_status_file() == 0 or get_status_file() == 1, "Make sure the previous test did run")

    def test_is_file_selected(self):
        dao = DAO()
        dao.switch_current_file(get_files().iloc[0].at["custom_name"])
        self.assertTrue(is_file_selected(), "Make sure the previous test did run")
