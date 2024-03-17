# Other imports
import numpy as np
import pandas as pd
# DeepCASE Imports
from Dashboard.processing.processor import Processor
from Dashboard.data.dao.dao import DAO


class ProcessorAccessObject(object):
    def __init__(self):
        # Initialise new processor
        self.processor = Processor()

        # Initialise empty tensors
        self.context = np.zeros(0)
        self.events = np.zeros(0)
        self.labels = np.zeros(0)
        # self.context_train = np.zeros(0)
        # self.context_test = np.zeros(0)
        # self.events_train = np.zeros(0)
        # self.events_test = np.zeros(0)
        # self.labels_train = np.zeros(0)
        # self.labels_test = np.zeros(0)

        # initialise dao
        self.dao = DAO()

    def create_sequences(self, path):
        self.context, self.events, self.labels, mapping = self.processor.sequence_data(path)
        # CALL DAO
        events_df = pd.read_csv(path)
        self.dao.save_sequencing_results(self.context, self.events, self.labels, mapping, events_df)



        # self.events_train = self.events[:self.events.shape[0] // 5]
        # self.events_test = self.events[self.events.shape[0] // 5:]
        #
        # self.context_train = self.context[:self.events.shape[0] // 5]
        # self.context_test = self.context[self.events.shape[0] // 5:]
        #
        # self.labels_train = self.labels[:self.events.shape[0] // 5]
        # self.labels_test = self.labels[self.events.shape[0] // 5:]
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
        print(type(clusters),clusters.shape)
        # DAOOOOOOOOO clusters
        # confidence, attention = self.processor.get_attention(self.context_train, self.events_train)
        confidence, attention = self.processor.get_attention(self.context, self.events)
        print(type(attention),attention.get_shape())
        self.dao.save_clustering_results(clusters, confidence, attention)
        return

    def manual_mode(self):
        """
        scores : np.array of shape=(n_samples)
                Scores for individual sequences computed using clustering
                strategy. All datapoints within a cluster are guaranteed to have
                the same score.
        """
        # scores = self.processor.scoring(self.labels_train)
        scores = self.processor.scoring(self.labels)
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
        # prediction = self.processor.predict(self.context_test, self.events_test)
        prediction = self.processor.predict(self.context, self.events)

        # confidence, attention = self.processor.get_attention(self.context_test, self.events_test)
        confidence, attention = self.processor.get_attention(self.context, self.events)
        return


if __name__ == '__main__':
    pao = ProcessorAccessObject()
    pao.create_sequences('alerts.csv')
    pao.train_context_builder()
    pao.create_interpreter_clusters()
    # # pao.manual_mode()
    # # pao.automatic_mode()
