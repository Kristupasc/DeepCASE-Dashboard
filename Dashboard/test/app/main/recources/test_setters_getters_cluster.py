from unittest import TestCase


from Dashboard.app.main.recources.data_dao_combine import *
from Dashboard.data.dao.dao import DAO
class Test(TestCase):
    def setUp(self):
        dao = DAO()
        dao.switch_current_file(dao.get_filenames().iloc[0].at["custom_name"])
        if not is_file_selected:
            raise Exception("No file present, run first deepcase")
    def test_get_event_id(self):
        # test existing event
        # Call the function
        event_id = get_event_id("ET DNS Query for .cc TLD")

        # Assert the result
        self.assertIsInstance(int(event_id), int)

        # test nonexistent event
        # Call the function
        event_id = get_event_id("nonexistent_event")

        # Assert the result
        self.assertEqual(event_id, "nonexistent_event")

    def test_set_riskvalue(self):
        self.assertTrue(set_riskvalue(0, 0, 0))

    def test_set_cluster_name(self):
        self.assertTrue(set_cluster_name(0, "0 test"))
