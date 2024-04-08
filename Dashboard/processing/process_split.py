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
            print('initialized')
        print('pao created')
        return

    def get_context_tensor(self) -> torch.Tensor:
        return self.dao.get_context_auto()

    def get_event_tensor(self) -> torch.Tensor:
        return self.dao.get_events_auto()

    def get_labels_tensor(self) -> torch.Tensor:
        return self.labels

    def create_sequences(self, data: pd.DataFrame):
        self.context, self.events, self.labels, mapping = self.processor.sequence_data(data)
        self.dao.save_sequencing_results(self.context, self.events, self.labels, mapping)
        return

    def train_context_builder(self):
        # self.processor.train_context_builder(self.context_train, self.events_train)
        self.processor.train_context_builder(self.context, self.events)
        return

    def create_interpreter_clusters(self):
        """
        clusters : np.array of shape=(n_samples,)
                Clusters per input sample.
        """
        clusters = self.processor.clustering(self.context, self.events)
        confidence, attention = self.processor.get_attention(self.context, self.events)
        # print(type(attention))
        # print(len(attention))
        # print(attention[-1])
        # print(attention.shape)
        self.dao.save_clustering_results(clusters, confidence, attention)
        return

    def manual_mode(self):
        """
        scores : np.array of shape=(n_samples)
                Scores for individual sequences computed using clustering
                strategy. All datapoints within a cluster are guaranteed to have
                the same score.
        """
        scores = self.processor.scoring(self.labels)
        self.dao.set_new_scores(scores)
        self.dao.save_cluster_scores()
        return

    def run_automatic_mode(self):
        """
        prediction : np.array of shape=(n_samples,)
                    Predicted maliciousness score.
                    Positive scores are maliciousness scores.
                    A score of 0 means we found a match that was not malicious.
                    Special cases:

                    * -1: Not confident enough for prediction
                    * -2: Label not in training
                    * -3: Closest cluster > epsilon
        """
        cur_context = self.get_context_tensor()
        cur_events = self.get_event_tensor()
        prediction = self.processor.predict(cur_context,cur_events)
        # todo get events from database but still need to save cluster
        self.dao.set_new_scores(prediction)
        self.dao.save_cluster_scores()
        confidence, attention = self.processor.get_attention(cur_context, cur_events)
        self.dao.update_attention(confidence, attention)
        return

    def run_DeepCASE(self):
        dao = DAO()
        data = dao.get_initial_table()
        self.create_sequences(data=data)
        self.train_context_builder()
        self.create_interpreter_clusters()
        self.manual_mode()

    # Testing only
    def run_DeepCASE_dummy(self):
        data = pd.read_csv('alerts.csv')
        self.create_sequences(data=data)
        self.train_context_builder()
        self.create_interpreter_clusters()
        self.manual_mode()
        # self.run_automatic_mode()


if __name__ == '__main__':
    pao = ProcessorAccessObject()
    pao.run_DeepCASE_dummy()
