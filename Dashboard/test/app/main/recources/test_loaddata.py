from unittest import TestCase
from unittest.mock import MagicMock, patch

from Dashboard.app.main.recources.loaddata import *
from Dashboard.data.dao.dao import DAO


class Test(TestCase):
    def test_format_sequence_cluster(self):
        self.fail()

    def test_possible_clusters(self):
        self.fail()

    def test_format_context(self):
        self.fail()

    def test_select_event_formatted(self):
        # Call the function without DAO input
        formatted_df = selectEventFormatted(cluster=1, index=0, id_str='_test_')

        # Assert the result
        self.assertIsInstance(formatted_df, pd.DataFrame)
        self.assertEqual(formatted_df.columns.tolist(),
                         ['machine_test_', 'timestamp_test_', 'name_test_', 'id_cluster_test_', 'risk_label_test_',
                          'id_event_test_'])
        self.assertIsInstance(formatted_df['machine_test_'].iloc[0], str)
        self.assertIsInstance(formatted_df['timestamp_test_'].iloc[0],
                         str)  # Assuming format_time is defined elsewhere
        self.assertIsInstance(formatted_df['name_test_'].iloc[0], str)
        try:
            int(formatted_df['id_cluster_test_'].iloc[0])
            int(formatted_df['risk_label_test_'].iloc[0])
            int(formatted_df['id_event_test_'].iloc[0])
        except ValueError:
            assert False, "Some values are not int, when expected."

    def test_get_event_id(self):
        # test existing event
        # Call the function
        dao = DAO()
        event_id = get_event_id("ET DNS Query for .cc TLD")

        # Assert the result
        self.assertIsInstance(int(event_id), int)

        # test nonexistent event
        # Call the function
        event_id = get_event_id("nonexistent_event")

        # Assert the result
        self.assertEqual(event_id, "nonexistent_event")

    def test_set_riskvalue(self):
        self.fail()

    def test_set_cluster_name(self):
        self.fail()

    def test_get_random_cluster(self):
        self.fail()

    @patch('Dashboard.app.main.recources.loaddata.random')
    def test_get_random_sequence(self, mock_random):
        # Mocking random function
        mock_random.randrange.return_value = 7  # Example random index

        # Call the function
        result = get_random_sequence(1)

        # Assert the result
        self.assertEqual(result, 7)