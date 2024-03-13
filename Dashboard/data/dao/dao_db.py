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

        context_df = pd.DataFrame(context_array)
        events_df = pd.DataFrame(events_array)
        labels_df = pd.DataFrame(labels_array)

        # for key, value in mapping.items():
        #     self.cur.execute("INSERT OR REPLACE INTO mapping (id, name) VALUES (?, ?)", (key, value))
        #     self.conn.commit()

        #read df row by row making row index seq index + main event index
        #loop over columns per row and insert to db after getting all db columns info
        #event id from 0 to 9
        for index, row in context_df.iterrows():
            id_sequence = index
            #loop for i in range(0,len(events))
            mapping_main_event = events_df.iloc[index,0]
            risk_label = labels_df.iloc[index, 0]
            self.cur.execute("INSERT INTO sequences (id_sequence, mapping_value, risk_label) "
                             "VALUES (?, ?, ?)", (id_sequence, mapping_main_event, risk_label))
            self.conn.commit()
            for column, value in row.items():
                id_event = column
                mapping_value = value
                self.cur.execute("INSERT INTO context_events (id_event, id_sequence, mapping_value) "
                                 "VALUES (?, ?, ?)", (id_event, id_sequence, mapping_value))
                self.conn.commit()


    def save_clustering_results(self, context, events, labels, mapping):
        pass

    def save_prediction_results(self, prediction):
        pass
