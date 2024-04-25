from unittest import TestCase

import pandas as pd

from Dashboard.app.main.recources.dao_files import is_file_selected
from Dashboard.app.main.recources.get_tables import get_cluster_table, get_context_table, get_clusters_tuple, \
    get_initial_table
from Dashboard.data.dao.dao import DAO


class Test(TestCase):
    def setUp(self):
        dao = DAO()
        dao.switch_current_file(dao.get_filenames().iloc[0].at["custom_name"])
        if not is_file_selected():
            raise Exception("No file present, run first deepcase")
    def test_get_initial_table(self):
        formatted_df = get_initial_table()

        # Assert the result
        self.assertIsInstance(formatted_df, pd.DataFrame)
        self.assertEqual(formatted_df.columns.tolist(), ['id_event', 'filename', 'timestamp', 'machine', 'event', 'label'])
        self.assertIsInstance(formatted_df['filename'].iloc[0], str)
        self.assertIsInstance(formatted_df['machine'].iloc[0], str)
        self.assertIsInstance(formatted_df['event'].iloc[0], str)
        try:
            int(formatted_df['id_event'].iloc[0])
            int(formatted_df['label'].iloc[0])
            float(formatted_df['timestamp'].iloc[0])
        except ValueError:
            assert False, "Some values are not int, when expected."

    def test_get_cluster_table(self):
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

    def test_get_context_table(self):
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

    def test_get_clusters_tuple(self):
        tuples = get_clusters_tuple()

        # Assert the result
        self.assertIsInstance(tuples, list)
        for tu in tuples:
            try:
                get_cluster_table(tu[0], "")
            except (ValueError, IndexError):
                raise str(tu[0]) + "is not found"
