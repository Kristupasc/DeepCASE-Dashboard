from unittest import TestCase
from Dashboard.data.dao.dao import Database
import pandas as pd
from io import StringIO

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class DB_Test(TestCase):
    def setUp(self) -> None:
        self.db = Database()
        self.filename = "test_file"
        self.db.filename = self.filename

    def tearDown(self):
        self.db.drop_database()
        self.db.reset()

    def test_create_tables(self):
        return

    def test_store_input_file(self):
        # Data stored in a dictionary
        data = {
            "id_event": [0, 1, 2],
            "timestamp": [1499075798.10912, 1499075798.10912, 1499075818.362352],
            "machine": ["192.168.10.9", "192.168.10.3", "192.168.10.9"],
            "event": ["SURICATA STREAM CLOSEWAIT FIN out of window"] * 3,
            "label": [3, 3, 3]
        }
        pand
        self.db.store_input_file(input_file_df=df, )
        return

    def test_switch_current_file(self):
        return

    def test_store_sequences(self):
        return

    def test_store_mapping(self):
        return

    def test_store_context(self):
        return

    def test_store_clusters(self):
        return

    def test_store_attention(self):
        return

    def test_update_sequence_score(self):
        return

    def test_fill_cluster_table(self):
        return

    def test_update_cluster_table(self):
        return

    def test_set_cluster_name(self):
        return

    def test_set_risk_value(self):
        return

    def test_set_filer_name(self):
        return

    def test_set_run_flag(self):
        return

    def test_get_input_table(self):
        return

    def test_get_sequences(self):
        return

    def test_get_sequence_by_id(self):
        return

    def test_get_context_by_sequence_id(self):
        return

    def test_get_clusters(self):
        return

    def test_get_sequences_per_cluster(self):
        return

    def test_get_mapping(self):
        return

    def test_get_filenamese(self):
        return

    def test_is_file_saved(self):
        return

    def test_display_current_file(self):
        return

    def test_get_context_for_automatic(self):
        return

    def test_get_events_for_automatic(self):
        return

    def test_get_run_flag(self):
        return

    def test_drop_database(self):
        return
