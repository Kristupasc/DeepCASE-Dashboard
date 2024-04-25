import json
from unittest import TestCase
from Dashboard.app.main.recources.data_dao_combine import *

class Test(TestCase):
    def setUp(self):
        dao = DAO()
        dao.switch_current_file(dao.get_filenames().iloc[0].at["custom_name"])
        if not is_file_selected:
            raise Exception("No file present, run first deepcase")
    def test_get_colors(self):
        get_colors() # test for no errors, is too trivial methode

    def test_choose_risk(self):
        # This methode is too trivial. and tested in function_risk
        pass

    def test_get_risk_cluster(self):
        self.assertIsInstance(get_risk_cluster(0), float)

    def test_function_risk(self):
        self.assertIsInstance(function_risk(0), str)
