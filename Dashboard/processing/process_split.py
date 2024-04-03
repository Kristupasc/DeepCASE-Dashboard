# Other imports
import numpy as np
import pandas as pd
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
        # Initialise new processor
        self.processor = Processor()

        # Initialise empty tensors
        self.context = np.zeros(0)
        self.events = np.zeros(0)
        self.labels = np.zeros(0)
        # initialise dao
        self.dao = DAO()
        # TODO: Get status from the DAO, finished if database is populated, empty otherwise
        self.status = Status.EMPTY

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
        # clusters = self.processor.clustering(self.context_train, self.events_train)
        clusters = self.processor.clustering(self.context, self.events)
        confidence, attention = self.processor.get_attention(self.context, self.events)
        # print(type(attention),attention.get_shape())
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
        return

    def automatic_mode(self):
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
        prediction = self.processor.predict(self.context, self.events)
        self.dao.set_new_scores(prediction)
        self.dao.save_cluster_scores()
        confidence, attention = self.processor.get_attention(self.context, self.events)

        return

    def run_DeepCASE(self):
        dao = DAO()
        data = dao.get_initial_table()
        self.create_sequences(data=data)
        self.train_context_builder()
        self.create_interpreter_clusters()
        self.status = Status.FINISHED
        self.manual_mode()
        self.automatic_mode()
        # return status_flag

    def get_status(self):
        return self.status


if __name__ == '__main__':
    pao = ProcessorAccessObject()
    pao.run_DeepCASE()
