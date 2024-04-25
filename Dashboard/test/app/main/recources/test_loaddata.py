from unittest import TestCase
from unittest.mock import patch

from Dashboard.app.main.recources.setters_getters_cluster import *
from Dashboard.data.dao.dao import DAO


class Test(TestCase):
    def setUp(self):
        dao = DAO()
        dao.switch_current_file(dao.get_filenames().iloc[0].at["custom_name"])
        if not is_file_selected:
            raise Exception("No file present, run first deepcase")



    def test_start_automatic(self):
        start_automatic()  # Check for no errors.

    def test_get_risk_cluster(self):
        self.assertIsInstance(get_risk_cluster(0), float)





    def test_function_risk(self):
        self.assertIsInstance(function_risk(0), str)
