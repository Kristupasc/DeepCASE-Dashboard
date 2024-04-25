from unittest import TestCase
from unittest.mock import patch

from Dashboard.app.main.recources.data_dao_combine import *
from Dashboard.data.dao.dao import DAO

class Test(TestCase):
    def setUp(self):
        dao = DAO()
        dao.switch_current_file(dao.get_filenames().iloc[0].at["custom_name"])
        if not is_file_selected():
            raise Exception("No file present, run first deepcase")
    @patch('Dashboard.app.main.recources.select_cluster_sequence.random')
    def test_get_algorithm_sequence(self, mock_random):
        # Mocking random function
        mock_random.choice.return_value = 2  # Example random index

        # Call the function
        result = get_algorithm_sequence(0)

        # Assert the result
        self.assertTrue(result == 2 or result is None)

    @patch('Dashboard.app.main.recources.select_cluster_sequence.random')
    def test_get_algorithm_cluster(self, mock_random):
        # Mocking random function
        mock_random.choice.return_value = 2  # Example random index

        # Call the function
        result = get_algorithm_cluster()

        # Assert the result
        self.assertTrue(result == 2 or result is None)

    @patch('Dashboard.app.main.recources.select_cluster_sequence.random')
    def test_get_random_cluster(self, mock_random):
        # Mocking random function
        mock_random.randrange.return_value = 6  # Example random index

        # Call the function
        result = get_random_cluster()

        # Assert the result
        self.assertEqual(result, 6 - 1)

    @patch('Dashboard.app.main.recources.select_cluster_sequence.random')
    def test_get_random_sequence(self, mock_random):
        # Mocking random function
        mock_random.randrange.return_value = 7  # Example random index

        # Call the function
        result = get_random_sequence(1)

        # Assert the result
        self.assertEqual(result, 7)

    def test_get_row(self):
        # Trivial test, check for unexpected errors.
        get_row(0)

