from abc import ABC, abstractmethod


class DAO(ABC):
    @abstractmethod
    def save_sequencing_results(self, context, events, labels, mapping):
        pass

    # @abstractmethod
    # def save_clustering_results(self, context, events, labels, mapping):
    #     pass
    #
    # @abstractmethod
    # def save_prediction_results(self, prediction):
    #     pass
    #
    # @abstractmethod
    # def load(self):
    #     pass
    
