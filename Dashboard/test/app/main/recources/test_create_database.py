from unittest import TestCase

from Dashboard.app.main.recources.loaddata import is_file_selected
from Dashboard.data.dao.dao import DAO


class Test(TestCase):
    def setUp(self):
        dao = DAO()
        dao.switch_current_file(dao.get_filenames().iloc[0].at["custom_name"])
        if not is_file_selected:
            raise Exception("No file present, run first deepcase")
    def test_parse_contents(self):
        self.fail()
