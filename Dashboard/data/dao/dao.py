import numpy as np
import torch
import pandas as pd
from Dashboard.data.dao.database import Database


class DAO(object):
    def __init__(self):
        self.data_object = Database()




    def switch_current_file(self, filename):
        """Call to database to switch the current file.

              Parameters
              ----------
              filename : name of the file to set as current file

              Returns
              -------
              True : if filename is changed successfully
              """
        return self.data_object.switch_current_file(filename)

    def get_filenames(self):
        return self.data_object.get_filenames()

    def save_input(self, input_file_df: pd.DataFrame, filename: str):
        input_file_df.reset_index(inplace=True)
        input_file_df.rename(columns={'index': 'id_event'}, inplace=True)
        self.data_object.store_input_file(input_file_df, filename)
        return

    def save_sequencing_results(self, context, events, labels, mapping):
        """
        Saves context, events, labels, mapping into data object.
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
            Mapping from new event_id to original name.

        """
        if context.is_cuda:
            context = context.cpu()
        if events.is_cuda:
            events = events.cpu()
        if labels.is_cuda:
            labels = labels.cpu()
        context_df = pd.DataFrame(context.numpy())
        events_df = pd.DataFrame(events.numpy())
        labels_df = pd.DataFrame(labels.numpy())
        # Melt the context_df DataFrame to put columns in event_position column
        melted_context_df = context_df.reset_index().melt(id_vars=["index"], var_name='event_position',
                                                          value_name='mapping_value')
        melted_context_df.rename(columns={'index': 'id_sequence'}, inplace=True)
        # Join the DataFrame
        joined_sequence_df = events_df.join(labels_df, lsuffix='mapping_value', rsuffix='risk_label')
        joined_sequence_df.rename(
            columns={'0mapping_value': 'mapping_value', '0risk_label': 'risk_label', 'index': 'id_sequence'},
            inplace=True)
        self.data_object.store_sequences(sequence_df=joined_sequence_df)
        self.data_object.store_context(context_df=melted_context_df)
        self.data_object.store_mapping(mapping=mapping)
        return

    def save_clustering_results(self, clusters, confidence, attention):
        clusters_df = pd.DataFrame(clusters, columns=['id_cluster'])
        clusters_df = clusters_df.reset_index()
        clusters_df.rename(columns={'index': 'id_sequence'}, inplace=True)
        if attention.is_cuda:
            attention = attention.cpu()
        attention_df = pd.DataFrame(attention)
        attention_melted_df = attention_df.reset_index().melt(id_vars=["index"], var_name='event_position',
                                                              value_name='attention')
        attention_melted_df.rename(columns={'index': 'id_sequence'}, inplace=True)
        self.data_object.store_clusters(clusters_df=clusters_df)
        self.data_object.store_attention(attention_melted_df)
        return

    def update_attention(self, confidence, attention):
        if attention.is_cuda:
            attention = attention.cpu()
        attention_df = pd.DataFrame(attention)
        attention_melted_df = attention_df.reset_index().melt(id_vars=["index"], var_name='event_position',
                                                              value_name='attention')
        attention_melted_df.rename(columns={'index': 'id_sequence'}, inplace=True)
        self.data_object.store_attention(attention_melted_df)
        return

    def set_new_cluster_scores(self, risk_labels: np.ndarray):
        risk_labels_df = pd.DataFrame(risk_labels)
        risk_labels_df.reset_index(inplace=True)
        risk_labels_df.rename(
            columns={0: 'risk_label', 'index': 'id_sequence'},
            inplace=True)
        self.data_object.update_sequence_score(risk_labels_df)
        self.data_object.fill_cluster_table()
        return

    def update_cluster_scores(self, risk_labels: np.ndarray):
        risk_labels_df = pd.DataFrame(risk_labels)
        risk_labels_df.reset_index(inplace=True)
        risk_labels_df.rename(
            columns={0: 'risk_label', 'index': 'id_sequence'},
            inplace=True)
        self.data_object.update_sequence_score(risk_labels_df)
        self.data_object.update_cluster_table()
        return
    def set_run_status(self):
        self.data_object.set_run_flag()
        return

    def get_initial_table(self):
        return self.data_object.get_input_table()

    def get_sequence_result(self):
        return self.data_object.get_sequences()

    def get_context_per_sequence(self, sequence_id):
        return self.data_object.get_context_by_sequence_id(sequence_id)

    def get_clusters_result(self):
        return self.data_object.get_clusters()

    def get_sequences_per_cluster(self, cluster_id):
        return self.data_object.get_sequences_per_cluster(cluster_id)

    def get_mapping(self):
        return self.data_object.get_mapping()

    def set_clustername(self, cluster_id, cluster_name):
        self.data_object.set_cluster_name(cluster_id, cluster_name)

    def set_riskvalue(self, event_id: int, risk_value: int):
        return self.data_object.set_risk_value(event_id, risk_value)

    def set_new_filename(self, file, new_filename):
        return self.data_object.set_file_name(file, new_filename)

    def get_all_files(self):
        return self.data_object.get_filenames()

    def is_input_file_empty(self):
        return self.data_object.is_file_saved()

    def display_selected_file(self):
        return self.data_object.display_current_file()

    def get_context_auto(self):
        return self.data_object.get_context_for_automatic()

    def get_events_auto(self):
        return self.data_object.get_events_for_automatic()
