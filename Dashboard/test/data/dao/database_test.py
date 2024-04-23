import sqlite3
import unittest
import torch
from Dashboard.data.dao.dao import Database
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class DB_Test(unittest.TestCase):
    def setUp(self) -> None:
        self.db = Database()
        self.db.conn = sqlite3.connect(':memory:')
        self.db.cur = self.db.conn.cursor()
        self.db.create_tables()
        self.filename = "testfile"
        self.db.filename = self.filename

        sequences_data = {'mapping_value': {0: 1, 1: 2}, 'risk_label': {0: 3, 1: 4}}
        self.sequences_df = pd.DataFrame(sequences_data)

        # Data stored in a dictionary
        input_data = {
            "id_event": [0, 1],
            "timestamp": [1499075798.10912, 1499075798.10912],
            "machine": ["192.168.10.9", "192.168.10.3"],
            "event": ['ET DNS Query for .su TLD (Soviet Union) Often Malware Related', 'ET DNS Query for .to TLD'],
            "label": [3, 4]
        }
        self.input_df = pd.DataFrame(input_data)

        self.mapping_data = {0: 'ET DNS Query for .cc TLD',
                             1: 'ET DNS Query for .su TLD (Soviet Union) Often Malware Related',
                             2: 'ET DNS Query for .to TLD', 3: 'ET DNS Query to a *.pw domain - Likely Hostile'}

        context_data = {'id_sequence': {0: 0, 1: 1}, 'event_position': {0: 0, 1: 0}, 'mapping_value': {0: 2, 1: 3}}
        self.context_df = pd.DataFrame(context_data)

        self.clusters_df = pd.DataFrame(
            [{'id_sequence': 0, 'id_cluster': 1}, {'id_sequence': 1, 'id_cluster': 2}])

        self.attention_df = pd.DataFrame([{'id_sequence': 0, 'event_position': 0, 'attention': 0.01},
                                          {'id_sequence': 1, 'event_position': 0, 'attention': 0.04}])
        score_data = {'id_sequence': {0: 0, 1: 1}, 'risk_label': {0: 3.0, 1: 3.0}}
        self.score_df = pd.DataFrame(score_data)

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def tearDown(self):
        self.db.drop_database()
        self.db.reset()

    def test_store_input_file(self):
        self.assertTrue(self.db.store_input_file(input_file_df=self.input_df, filename=self.filename))
        return

    def test_store_sequences(self):
        self.assertTrue(self.db.store_sequences(sequence_df=self.sequences_df))
        return

    def test_store_mapping(self):
        self.assertTrue(self.db.store_mapping(mapping=self.mapping_data))

        return

    def test_store_context(self):
        self.assertTrue(self.db.store_context(context_df=self.context_df))
        return

    # Method to populate the database right after the saving methods passed
    def populate_database(self):
        self.db.store_input_file(input_file_df=self.input_df, filename=self.filename)
        self.filename = self.db.display_current_file()
        self.db.store_sequences(sequence_df=self.sequences_df)
        self.db.store_mapping(mapping=self.mapping_data)
        self.db.store_context(context_df=self.context_df)
        return

    #########################################################################
    def test_store_clusters(self):
        self.assertTrue(self.db.store_clusters(clusters_df=self.clusters_df))
        return

    def test_store_attention(self):
        self.assertTrue(self.db.store_attention(self.attention_df))
        return

    def test_switch_current_file(self):
        new_file = "new_testfile"
        not_existing_file = "not_file"
        self.db.conn.execute("INSERT INTO files (filename, custom_name, run) VALUES (?, ?, ?)",
                             (new_file, new_file, 0))
        self.db.conn.commit()
        self.assertTrue(self.db.switch_current_file(new_file))
        self.assertFalse(self.db.switch_current_file(not_existing_file))
        return

    def test_update_sequence_score(self):
        self.assertTrue(self.db.update_sequence_score(self.score_df))
        return

    def test_fill_cluster_table(self):
        self.assertTrue(self.db.fill_cluster_table())
        return

    def test_update_cluster_table(self):
        self.assertTrue(self.db.update_cluster_table())
        return

    def test_set_cluster_name(self):
        name = "mew_cluster_name"
        self.assertTrue(self.db.set_cluster_name(id_cluster=0, name_cluster=name))
        return

    def test_set_risk_value(self):
        event = 0
        risk_value = 10
        self.assertTrue(self.db.set_risk_value(event_id=event,
                                               risk_value=risk_value))
        return

    def test_set_file_name(self):
        new_name = "mew_filename"
        self.assertTrue(self.db.set_file_name(self.filename, new_name))
        return

    def test_set_run_flag(self):
        self.assertTrue(self.db.set_run_flag())
        return

    def modify_database(self):
        self.db.store_clusters(self.clusters_df)
        self.db.store_attention(self.attention_df)
        self.db.fill_cluster_table()

    ########################################################################
    #                         Data aggregation                             #
    ########################################################################
    def test_get_input_table(self):
        self.populate_database()
        db_df = self.db.get_input_table()
        # Assert that both DataFrames are equal after reordering (db_df[self.input_df.columns]) columns
        self.assertTrue(db_df[self.input_df.columns].equals(self.input_df))
        return

    def test_get_sequences(self):
        self.populate_database()

        db_df = self.db.get_sequences()
        expected_data = {'name': {0: 'ET DNS Query for .su TLD (Soviet Union) Often Malware Related',
                                  1: 'ET DNS Query for .to TLD'},
                         'timestamp': {0: 1499075798.10912, 1: 1499075798.10912},
                         'machine': {0: "192.168.10.9", 1: "192.168.10.3"},
                         'id_cluster': {0: None, 1: None},
                         'risk_label': {0: 3, 1: 4}}
        expected_df = pd.DataFrame(expected_data)
        self.assertTrue(db_df.equals(expected_df))
        return

    def test_get_sequence_by_id(self):
        self.populate_database()

        db_df = self.db.get_sequence_by_id(0)
        expected_data = {'name': {0: 'ET DNS Query for .su TLD (Soviet Union) Often Malware Related'},
                         'timestamp': {0: 1499075798.10912},
                         'machine': {0: "192.168.10.9"},
                         'id_cluster': {0: None},
                         'risk_label': {0: 3}}
        expected_df = pd.DataFrame(expected_data)
        self.assertTrue(db_df.equals(expected_df))
        return

    def test_get_context_by_sequence_id(self):
        self.populate_database()
        self.modify_database()
        df = self.db.get_context_by_sequence_id(sequence_id=0)
        expected_data = {'event_position': {0: 0},
                         'name': {0: 'ET DNS Query for .to TLD'},
                         'attention': {0: 0.01}}
        expected_df = pd.DataFrame(expected_data)
        print('actual')
        print(df)
        print('expected')
        print(expected_df)
        self.assertTrue(df.equals(expected_df))
        return

    def test_get_clusters(self):
        self.populate_database()
        self.modify_database()

        df = self.db.get_clusters()
        expected_data = {'id_cluster': {0: 1, 1: 2},
                         'name_cluster': {0: 1, 1: 2},
                         'score': {0: 3, 1: 4},
                         'filename': {0: self.filename, 1: self.filename}}
        expected_df = pd.DataFrame(expected_data)
        self.assertTrue(df.equals(expected_df))
        return

    def test_get_sequences_per_cluster(self):
        self.populate_database()
        self.modify_database()

        df = self.db.get_sequences_per_cluster(1)
        expected_data = {'id_event': {0: 1},
                         'id_sequence': {0: 0},
                         'name': {0: 'ET DNS Query for .su TLD (Soviet Union) Often Malware Related'},
                         'timestamp': {0: 1499075798.10912},
                         'machine': {0: '192.168.10.9'},
                         'id_cluster': {0: 1},
                         'risk_label': {0: 3}}

        expected_df = pd.DataFrame(expected_data)
        self.assertTrue(df.equals(expected_df))
        return

    def test_get_mapping(self):
        self.populate_database()
        self.modify_database()

        df = self.db.get_mapping()
        expected_data = {'name':
                              {0: 'ET DNS Query for .cc TLD',
                               1: 'ET DNS Query for .su TLD (Soviet Union) Often Malware Related',
                               2: 'ET DNS Query for .to TLD',
                               3: 'ET DNS Query to a *.pw domain - Likely Hostile'},
                         'id': {0: 0, 1: 1, 2: 2, 3: 3}}

        expected_df = pd.DataFrame(expected_data)
        self.assertTrue(df.equals(expected_df))
        return

    def test_get_filenames(self):
        self.populate_database()
        self.modify_database()

        df = self.db.get_filenames()
        expected_data = {'custom_name': {0: self.filename}}

        expected_df = pd.DataFrame(expected_data)
        self.assertTrue(df.equals(expected_df))
        return

    def test_is_file_saved(self):
        self.populate_database()
        self.modify_database()
        self.assertTrue(self.db.is_file_saved())
        return

    def test_display_current_file(self):
        self.populate_database()
        self.modify_database()
        result = self.db.display_current_file()
        self.assertEqual(result, self.filename)
        return

    def test_get_context_for_automatic(self):
        self.populate_database()
        self.modify_database()
        expected_ts = torch.tensor([[2],[3]], dtype=torch.int32, device=self.device)
        ts = self.db.get_context_for_automatic()
        # https://pytorch.org/docs/stable/testing.html
        torch.testing.assert_close(ts, expected_ts)
        return

    def test_get_events_for_automatic(self):
        self.populate_database()
        self.modify_database()
        expected_ts = torch.tensor([1, 2], device=self.device)
        ts = self.db.get_events_for_automatic()
        # https://pytorch.org/docs/stable/testing.html
        torch.testing.assert_close(ts, expected_ts)
        return

    def test_get_run_flag(self):
        self.populate_database()
        self.modify_database()

        flag = self.db.get_run_flag()
        self.assertEqual(flag, 0)
        return

if __name__ == '__main__':
    unittest.main()
