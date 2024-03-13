# crate csvs - db
import torch
from Dashboard.data.dao.dao import DAO
import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "deepcase.db")


class DAO_db(DAO):
    def __init__(self):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def save_sequencing_results(self, context, events, labels, mapping):
        """Saves context, events, labels, mapping into deepcase database .

            Parameters
            ----------
            context : torch.Tensor of shape=(n_samples, context_length)
                Context events for each event in events.

            events : torch.Tensor of shape=(n_samples,)
                Events in data.

            labels : torch.Tensor of shape=(n_samples,)
                Labels will be None if no labels parameter is given, and if data
                does not contain any 'labels' column.

            mapping : dict()
                Mapping from new event_id to original event_id.
                Sequencing will map all events to a range from 0 to n_events.
                This is because event IDs may have large values, which is
                difficult for a one-hot encoding to deal with. Therefore, we map
                all Event ID values to a new value in that range and provide
                this mapping to translate back.
        """

        if context.is_cuda:
            context = context.cpu()
        if events.is_cuda:
            events = events.cpu()
        if labels.is_cuda:
            labels = labels.cpu()

        context_array = context.numpy()
        events_array = events.numpy()
        labels_array = labels.numpy()

        # TODO: add column names to events, labels and remove suffix line70
        context_df = pd.DataFrame(context_array)
        events_df = pd.DataFrame(events_array)
        labels_df = pd.DataFrame(labels_array)

        for key, value in mapping.items():
            self.cur.execute("INSERT OR REPLACE INTO mapping (id, name) VALUES (?, ?)", (key, value))
            self.conn.commit()

        # Melt the DataFrame
        melted_df = context_df.reset_index().melt(id_vars=["index"], var_name='event_position',
                                                  value_name='mapping_value')
        melted_df.rename(columns={'index': 'id_sequence'}, inplace=True)

        # Upload to context events table
        melted_df.to_sql('context_events', con=self.conn, if_exists='append', index=False)

        # Join the DataFrame
        joined_df = events_df.join(labels_df, lsuffix='mapping_value', rsuffix='risk_label')
        joined_df.rename(
            columns={'0mapping_value': 'mapping_value', '0risk_label': 'risk_label', 'index': 'id_sequence'},
            inplace=True)

        # Upload to sequence table
        joined_df.to_sql('sequences', con=self.conn, if_exists='append', index=False)

    def save_clustering_results(self, clusters, confidence, attention):

        clusters_df = pd.DataFrame(clusters, columns=['id_cluster'])
        clusters_df = clusters_df.reset_index()
        clusters_df.rename(columns={'index': 'id_sequence'}, inplace=True)

        self.cur.execute('''DROP TABLE IF EXISTS temporary''')
        self.cur.execute('''CREATE TABLE temporary (id_sequence INTEGER PRIMARY KEY, id_cluster TEXT)''')
        clusters_df.to_sql('temporary', con=self.conn, if_exists='replace', index=False)

        df = pd.read_sql_query('''SELECT sequences.id_sequence, temporary.id_cluster, sequences.mapping_value, sequences.risk_label
                    FROM sequences, temporary
                     WHERE sequences.id_sequence = temporary.id_sequence''', self.conn)
        df.to_sql('sequences', con=self.conn, if_exists='replace', index=False)

        # self.cur.execute('''UPDATE sequences
        #                     SET id_cluster = (SELECT tm.id_cluster
        #                                       FROM temporary tm
        #                                       WHERE  tm.id_sequence = id_sequence)
        #                     WHERE id_sequence IN (SELECT id_sequence
        #                                           FROM temporary tm
        #                                           WHERE tm.id_sequence= id_sequence
        #                                           )
        #                     AND id_cluster IS NULL''')


        pass

    def save_prediction_results(self, prediction):
        pass
