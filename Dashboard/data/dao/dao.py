import numpy as np
import torch
import pandas as pd
from Dashboard.data.dao.database import Database


class DAO(object):
    def __init__(self):
        self.data_object = Database()

    def switch_current_file(self, filename):
        """
        Calls database to switch currently used file
        Parameters
        ----------
            filename (str) : name of file to become a currently used file
        Returns
        -------
            (bool) : indicator whether file was switched successfully
        """
        return self.data_object.switch_current_file(filename)

    ########################################################################
    #                         Data insertion                               #
    ########################################################################
    def save_input(self, input_file_df: pd.DataFrame, filename: str):
        """
        Calls database to store input file and its data.

        Parameters
        ----------
            input_file_df (pd.DataFrame) : contains initial information about all events
            filename (str) : name of the file DeepCase should perform analysis onto
        Returns
        -------
            None
        """
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
        """
        Stores clusters and attention vector produced by DeepCase

        Parameters
        ----------
            clusters_df (pd.DataFrame) : contains the ids of clusters for each sequence
            attention_df (pd.DataFrame) : attention vector of context events
        Returns
        -------
            None
        """
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
    def set_new_cluster_scores(self, risk_labels: np.ndarray):
        """
        Updates the risk label and store generated clusters into data object.

        Returns
        -------
            None
        """
        risk_labels_df = pd.DataFrame(risk_labels)
        risk_labels_df.reset_index(inplace=True)
        risk_labels_df.rename(
            columns={0: 'risk_label', 'index': 'id_sequence'},
            inplace=True)
        self.data_object.update_sequence_score(risk_labels_df)
        self.data_object.fill_cluster_table()
        return

    def set_run_status(self):
        """
        Changes run status DeepCase finishes its analysis

        Returns
        -------
            None
        """
        self.data_object.set_run_flag()
        return

    def set_clustername(self, cluster_id, cluster_name):
        """
        Updates the name of the existing cluster into the custom one in the data object.

        Parameters
        ----------
            cluster_id (int) : id of cluster which name is to be changed
            cluster_name (str) : new name to be assigned to a selected cluster
        Returns
        -------
            None
        """
        self.data_object.set_cluster_name(cluster_id, cluster_name)
        return

    def set_riskvalue(self, event_id: int, risk_value: int):
        """
        Updates the risk label of the selected sequence in data object.

        Parameters
        ----------
            event_id (int) : unique id of the event which score is to be changed
            risk_value (int) : new risk value to set to selected event
        Returns
        -------
            None
        """
        self.data_object.set_risk_value(event_id, risk_value)
        return

    def set_new_filename(self, file, new_filename):
        """
        Updates the file name of the selected file in data object.

        Parameters
        ----------
            file (str) : unique name of the file to be changed
            new_filename (str) : custom filename to set to selected file
        Returns
        -------
            None
        """
        self.data_object.set_file_name(file, new_filename)
        return

    ########################################################################
    #                         Data update                                  #
    ########################################################################
    def update_attention(self, confidence, attention):
        """
        Updates attention vector produced by DeepCase.

        Parameters
        ----------
            confidence (pd.DataFrame) : confidence level of each context event
            attention (pd.DataFrame) : attention vector of context events
        Returns
        -------
            None
        """
        if attention.is_cuda:
            attention = attention.cpu()
        attention_df = pd.DataFrame(attention)
        attention_melted_df = attention_df.reset_index().melt(id_vars=["index"], var_name='event_position',
                                                              value_name='attention')
        attention_melted_df.rename(columns={'index': 'id_sequence'}, inplace=True)
        self.data_object.store_attention(attention_melted_df)
        return

    def update_cluster_scores(self, risk_labels: np.ndarray):
        """
        Updates the risk label of all the sequences and clusters as the result of DeepCase analysis.

        Parameters
        ----------
            risk_labels (pd.DataFrame) : dataframe containing all the new scores for each sequence
        Returns
        -------
            None
        """
        risk_labels_df = pd.DataFrame(risk_labels)
        risk_labels_df.reset_index(inplace=True)
        risk_labels_df.rename(
            columns={0: 'risk_label', 'index': 'id_sequence'},
            inplace=True)
        self.data_object.update_sequence_score(risk_labels_df)
        self.data_object.update_cluster_table()
        return

    ########################################################################
    #                         Data aggregation                             #
    ########################################################################
    def get_all_files(self):
        """
        Retrieves all the files currently stored by the system.

        Returns
        -------
            (pd.DataFrame) : dataframe with all the files from database
        """
        return self.data_object.get_filenames()

    def is_input_file_empty(self):
        """
        Checks whether events were stored in the system. This check is necessary to confirm
        that input data was transferred from file into a database.

        Returns
        -------
            (bool) : status whether the events of the considered file are stored in the system
        """
        return self.data_object.is_file_saved()

    def display_selected_file(self):
        """
        Displays the name of the file DeepCase uses for processing at the moment.

        Returns
        -------
            (str) : the name of the currently selected file
        """
        return self.data_object.display_current_file()
    def get_initial_table(self):
        """
        Retrieves initial data passed to DeepCase.

        Returns
        -------
            (pd.DataFrame) : dataframe with all the events in the format initially passed to DeepCase
        """
        return self.data_object.get_input_table()

    def get_sequence_result(self):
        """
        Retrieves all the sequences main events from database.

        Returns
        -------
            (pd.DataFrame) : dataframe with all the sequences including the detailed info about each event
        """
        return self.data_object.get_sequences()

    def get_context_per_sequence(self, sequence_id):
        """
        Retrieves context events of the chosen sequence.
        Parameters:
        -----------
            sequence_id (int) : unique id of a chosen sequence
        Returns
        -------
            (pd.DataFrame) : dataframe with the specified context events including the detailed info about each event
        """
        return self.data_object.get_context_by_sequence_id(sequence_id)

    def get_clusters_result(self):
        """
        Retrieves all the clusters of specified filename.

        Returns
        -------
            (pd.DataFrame) : dataframe with all the clusters stored in the system
        """
        return self.data_object.get_clusters()

    def get_sequences_per_cluster(self, cluster_id):
        """
        Retrieves all teh sequences in the selected cluster
        Parameters:
        -----------
            cluster_id (int) : id of a cluster

        Returns
        -------
            (pd.DataFrame) : dataframe with the specified sequences per cluster
             including the detailed info about each event
        """
        return self.data_object.get_sequences_per_cluster(cluster_id)

    def get_mapping(self):
        """
        Retrieves the mapping events name of the considered file.

        Returns
        -------
            (pd.DataFrame) : dataframe with the events' unique mapping
        """
        return self.data_object.get_mapping()
    def get_context_auto(self):
        """
        Retrieve the context events by filename

        Returns
        -------
            (torch.Tensor) : tensor with all the events
        """
        return self.data_object.get_context_for_automatic()

    def get_events_auto(self):
        """
        Retrieve the sequences by filename

        Returns
        -------
            (torch.Tensor) : tensor with all the sequences
        """
        return self.data_object.get_events_for_automatic()

    def get_run_status(self):
        """
        Retrieve the run flag of the current file

        Returns
        -------
            (int) : status flag indicating whether DeepCase was run on selected file
        """
        return self.data_object.get_run_flag()
    def get_filenames(self):
        """
        Retrieves all the files that were uploaded to the system.

        Returns
        -------
            (pd.DataFrame) : dataframe with all the files from database
        """
        return self.data_object.get_filenames()