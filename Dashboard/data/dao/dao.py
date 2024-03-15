import torch
import pandas as pd
from Dashboard.data.dao.database import Database


class DAO(object):
    def __init__(self):
        self.data_object = Database()

        # Reset the database
        self.data_object.drop_database()
        self.data_object.create_tables()


    def save_sequencing_results(self, context, events, labels, mapping, input_file_df):
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
        input_file_df : pandas.DataFrame
        Initial input file
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
        input_file_df.reset_index(inplace=True)
        input_file_df.rename(columns={'index': 'id_event'}, inplace=True)

        self.data_object.store_sequences(sequence_df=joined_sequence_df)
        self.data_object.store_context(context_df=melted_context_df)
        self.data_object.store_mapping(mapping=mapping)
        self.data_object.store_input_file(input_file_df)
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

    def save_prediction_results(self, prediction):
        # TODO: Placeholder, add functionality later
        if prediction.is_cuda:
            prediction = prediction.cpu()
        prediction = pd.DataFrame(prediction)
        self.data_object.store_risk_labels(prediction)
        return
