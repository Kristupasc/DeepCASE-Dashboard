# Other imports
import numpy as np
import pandas as pd
import torch

# DeepCASE Imports
from Dashboard.processing.processor import Processor
from Dashboard.data.dao.dao import DAO
from Dashboard.processing.status import Status


class ProcessorAccessObject(object):
    _instance = None

    # creates a singleton
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ProcessorAccessObject, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Check if the instance is already initialized
            # Initialise new processor
            self.processor = Processor()
            self.initialized = True  # Mark the instance as initialized
            # Initialise empty tensors
            self.context = torch.empty(0, 0)
            self.events = torch.empty(0, 0)
            self.labels = torch.empty(0, 0)
            # initialise dao
            self.dao = DAO()
        return

    def get_context_tensor(self) -> torch.Tensor:
        """
        Getter for context events. The output is generated from database via use of Data Access Object (DAO)

         Returns
         -------
         torch.Tensor
            Tensor in the form of initial context representing context events."""
        return self.dao.get_context_auto()

    def get_event_tensor(self) -> torch.Tensor:
        """
        Getter for sequence events. The output is generated from database via use of Data Access Object (DAO)

         Returns
         -------
         torch.Tensor
            Tensor in the form of initial events tensor representing main events of sequences."""
        return self.dao.get_events_auto()

    def get_labels_tensor(self) -> torch.Tensor:
        """
        Getter for labels.

         Returns
         -------
         self.labels : torch.Tensor"""
        return self.labels

    def create_sequences(self, data: pd.DataFrame):
        """
        Processes input data to generate sequences and saves the sequencing results.

        This method uses a DeepCASE processor to transform the input DataFrame into sequences
        of context, events, and labels along with a mapping. It then saves these sequences
        and the mapping using a Data Access Object (DAO).

        Parameters
        ----------
        data : pd.DataFrame
            The input data to be processed into sequences.

        Returns
        -------
        None
            This method does not return a value."""
        self.context, self.events, self.labels, mapping = self.processor.sequence_data(data)
        self.dao.save_sequencing_results(self.context, self.events, self.labels, mapping)
        return

    def train_context_builder(self):
        """
        Performs training of DeepCASE context builder using the methods from Processor class
         Returns
         -------
         None
         """
        self.processor.train_context_builder(self.context, self.events)
        return

    def create_interpreter_clusters(self):
        """
        Creates cluster using the method of Processor class and saves output to the database via Cata Access Object.

        Returns:
            None
        """
        clusters = self.processor.clustering(self.context, self.events)
        confidence, attention = self.processor.get_attention(self.context, self.events)
        self.dao.save_clustering_results(clusters, confidence, attention)
        return

    def manual_mode(self):
        """
        Performs scoring of sequences for Manual analysis using corresponding method of Processor. Saves the clusters in database
        using Data Access Object.

        Returns:
            None
        """
        scores = self.processor.scoring(self.labels)
        self.dao.set_new_cluster_scores(scores)
        return

    def run_automatic_mode(self):
        """
        Performs prediction of sequence scores for Semi-Automatic analysis using corresponding method of Processor. Saves the clusters and predictions in database
        using Data Access Object.

        Returns:
            None
        """
        cur_context = self.get_context_tensor()
        cur_events = self.get_event_tensor()
        prediction = self.processor.predict(cur_context, cur_events)
        self.dao.update_cluster_scores(prediction)
        confidence, attention = self.processor.get_attention(cur_context, cur_events)
        self.dao.update_attention(confidence, attention)
        return

    def run_DeepCASE(self):
        """
        Runs DeepCASE stages: Sequencing, ContextBuilder, Interpreter, Manual Analysis

        Returns
        -------
            None
        """
        dao = DAO()
        data = dao.get_initial_table()
        self.create_sequences(data=data)
        self.train_context_builder()
        self.create_interpreter_clusters()
        self.manual_mode()
        self.dao.set_run_status()


 # Testing only
    def run_DeepCASE_dummy(self):
        data = pd.read_csv('alerts.csv')
        self.dao.save_input(data, "alerts.csv")
        self.dao.set_run_status()
        self.create_sequences(data=data)
        # self.train_context_builder()
        # self.create_interpreter_clusters()
        # self.manual_mode()
        # self.run_automatic_mode()


if __name__ == '__main__':
    pao = ProcessorAccessObject()
    pao.run_DeepCASE_dummy()