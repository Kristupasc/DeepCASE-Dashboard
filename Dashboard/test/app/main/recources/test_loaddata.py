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

    def test_format_sequence_cluster(self):  # Call the function without DAO input
        formatted_df = get_cluster_table(cluster=1, id_str='_test_')

        # Assert the result
        self.assertIsInstance(formatted_df, pd.DataFrame)
        self.assertEqual(formatted_df.columns.tolist(),
                         ['machine_test_',
                          'timestamp_test_',
                          'name_test_',
                          'risk_label_test_',
                          'id_event_test_'])
        self.assertIsInstance(formatted_df['machine_test_'].iloc[0], str)
        self.assertIsInstance(formatted_df['timestamp_test_'].iloc[0],
                              str)  # Assuming format_time is defined elsewhere
        self.assertIsInstance(formatted_df['name_test_'].iloc[0], str)
        try:
            int(formatted_df['risk_label_test_'].iloc[0])
            int(formatted_df['id_event_test_'].iloc[0])
        except ValueError:
            assert False, "Some values are not int, when expected."

    def test_possible_clusters(self):
        tuples = get_clusters_tuple()

        # Assert the result
        self.assertIsInstance(tuples, list)
        for tu in tuples:
            try:
                get_cluster_table(tu[0], "")
            except (ValueError, IndexError):
                raise str(tu[0]) + "is not found"

    def test_format_context(self):
        # Call the function without DAO input
        formatted_df = get_context_table(cluster=1, index=0, id_str='_test_')

        # Assert the result
        self.assertIsInstance(formatted_df, pd.DataFrame)
        self.assertEqual(formatted_df.columns.tolist(),
                         ['event_position_test_', 'name_test_', 'attention_test_', 'event_test_'])
        self.assertIsInstance(formatted_df['name_test_'].iloc[0], str)
        try:
            int(formatted_df['event_position_test_'].iloc[0])
            float(formatted_df['attention_test_'].iloc[0])
            int(formatted_df['event_test_'].iloc[0])
        except ValueError:
            assert False, "Some values are not int or float, when expected."

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

    def test_start_automatic(self):
        start_automatic()  # Check for no errors.

    def test_get_risk_cluster(self):
        self.assertIsInstance(get_risk_cluster(0), float)

    def test_is_file_selected(self):
        self.assertIsInstance(is_file_selected(), bool)

    @patch('Dashboard.app.main.recources.loaddata.random')
    def test_get_algorithm_sequence(self, mock_random):
        # Mocking random function
        mock_random.choice.return_value = 2  # Example random index

        # Call the function
        result = get_algorithm_sequence(0)

        # Assert the result
        self.assertTrue(result == 2 or result is None)

    def test_function_risk(self):
        self.assertIsInstance(function_risk(0), str)

    @patch('Dashboard.app.main.recources.loaddata.random')
    def test_get_algorithm(self, mock_random):
        # Mocking random function
        mock_random.choice.return_value = 2  # Example random index

        # Call the function
        result = get_algorithm_cluster()

        # Assert the result
        self.assertTrue(result == 2 or result is None)

    @patch('Dashboard.app.main.recources.loaddata.random')
    def test_get_random_cluster(self, mock_random):
        # Mocking random function
        mock_random.randrange.return_value = 6  # Example random index

        # Call the function
        result = get_random_cluster()

        # Assert the result
        self.assertEqual(result, 6 - 1)

    @patch('Dashboard.app.main.recources.loaddata.random')
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
