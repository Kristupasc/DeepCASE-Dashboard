# Other imports
import numpy as np
import pandas
import torch

# DeepCASE Imports
from DeepCase.deepcase.preprocessing import Preprocessor
from DeepCase.deepcase.context_builder import ContextBuilder
from DeepCase.deepcase.interpreter import Interpreter

#class of main functionality of DeepCASE
class Processor(object):

    def __init__(self):
        # Create preprocessor
        self.preprocessor = Preprocessor(
            length=10,  # 10 events in context
            timeout=86400,  # Ignore events older than 1 day (60*60*24 = 86400 seconds)
        )
        # Create context builder
        self.context_builder = ContextBuilder(
            input_size=100,  # Number of input features to expect
            output_size=100,  # Same as input size
            hidden_size=128,  # Number of nodes in hidden layer, in paper we set this to 128
            max_length=10,  # Length of the context, should be same as context in Preprocessor
        )
        # Create interpreter
        self.interpreter = Interpreter(
            context_builder=self.context_builder,  # ContextBuilder used to fit data
            features=100,  # Number of input features to expect, should be same as ContextBuilder
            eps=0.1,  # Epsilon value to use for DBSCAN clustering, in paper this was 0.1
            min_samples=5,  # Minimum number of samples to use for DBSCAN clustering, in paper this was 5
            threshold=0.2,
            # Confidence threshold used for determining if attention from the ContextBuilder can be used, in paper this was 0.2
        )

        if torch.cuda.is_available():
            self.context_builder = self.context_builder.to('cuda')

    ########################################################################
    #                             Loading data                             #
    ########################################################################

    def sequence_data(self, data: pandas.DataFrame):
        """
        Processes input data to generate context, events, labels, and a mapping.

        This method takes a DataFrame as input and uses the DeepCASE preprocessor to transform this data
        into sequences of context and events, along with generating labels and a mapping. If no labels
        are generated, a default label of -1 is assigned to all events.

        Parameters
        ----------
        data : pd.DataFrame
            The input data to be sequenced.

        Returns
        -------
        context (torch.Tensor): The context tensor.
        events (torch.Tensor): The events tensor.
        labels (numpy.ndarray): An array of labels for the events. Defaults to -1 if not provided.
        mapping (dict): A dictionary representing the mapping of events generated during the sequencing process.
        """

        context, events, labels, mapping = self.preprocessor.sequence(data=data, verbose=True)

        if labels is None:
            labels = np.full(events.shape[0], -1, dtype=int)

        # Cast to cuda if available
        if torch.cuda.is_available():
            events = events.to('cuda')
            context = context.to('cuda')
        return context, events, labels, mapping

    ########################################################################
    #                         Using ContextBuilder                         #
    ########################################################################

    def train_context_builder(self, context_train, events_train):
        """
               Trains the model on context and events via Context Builder.

               Parameters
               ----------
               context_train : torch.Tensor
                   The input data of context events.

               events_train: torch.Tensor
                    The input data of main sequence events.

               Returns
               -------
                None
               """
        self.context_builder.fit(
            X=context_train,  # Context to train with
            y=events_train.reshape(-1, 1),  # Events to train with, note that these should be of shape=(n_events, 1)
            epochs=10,  # Number of epochs to train with
            batch_size=128,  # Number of samples in each training batch, in paper this was 128
            learning_rate=0.01,  # Learning rate to train with, in paper this was 0.01
            verbose=True,  # If True, prints progress
        )
        return

    ########################################################################
    #                          Using Interpreter                           #
    ########################################################################

    def clustering(self, context_train, events_train):
        """
           Clusters the sequences based on context events and main sequence event.

           Parameters
           ----------
           context_train : torch.Tensor
                   The input data of context events.

           events_train: torch.Tensor
                The input data of main sequence events.

           Returns
           -------
           clusters (numpy.ndarray): array of cluster values assigned to sequences.
       """
        clusters = self.interpreter.cluster(
            X=context_train,  # Context to train with
            y=events_train.reshape(-1, 1),  # Events to train with, note that these should be of shape=(n_events, 1)
            iterations=100,  # Number of iterations to use for attention query, in paper this was 100
            batch_size=1024,  # Batch size to use for attention query, used to limit CUDA memory usage
            verbose=True,  # If True, prints progress
        )
        return clusters

    def get_attention(self, context, events):
        """
           Attention and confidence level is assigned to each context event

           Parameters
           ----------
           context : torch.Tensor
                   The input data of context events.

           events: torch.Tensor
                The input data of main sequence events.

           Returns
           -------
           confidence (torch.Tensor): confidence  level of context event in regards to sequence
           attention (torch.Tensor): attention vector for all context events
       """
        confidence, attention, inverse = self.context_builder.query(
            X=context,  # Context to train with
            y=events.reshape(-1, 1),  # Events to train with, note that these should be of shape=(n_events, 1)
            iterations=100,  # Number of iterations to use for attention query, in paper this was 100
            batch_size=1024,  # Batch size to use for attention query, used to limit CUDA memory usage
            verbose=True,  # If True, prints progress
        )
        confidence = confidence[inverse]
        attention = attention[inverse]

        return confidence, attention

    ########################################################################
    #                             Manual mode                              #
    ########################################################################

    def scoring(self, labels_train):
        """
           Each sequence gets a security score to further be analyzed in manual mode

           Parameters
           ----------
           labels_train: torch.Tensor
                The input labels of main sequence events.

           Returns
           -------
           scores (torch.Tensor): tensor of all the score values per sequence
       """
        scores = self.interpreter.score_clusters(
            scores=labels_train,
            # Labels used to compute score (either as loaded by Preprocessor, or put your own labels here)
            strategy="max",  # Strategy to use for scoring (one of "max", "min", "avg")
            NO_SCORE=-1,  # Any sequence with this score will be ignored in the strategy.
            # If assigned a cluster, the sequence will inherit the cluster score.
            # If the sequence is not present in a cluster, it will receive a score of NO_SCORE.
        )

        self.interpreter.score(
            scores=scores,  # Scores to assign to sequences
            verbose=True,  # If True, prints progress
        )
        return scores

    ########################################################################
    #                        (Semi-)Automatic mode                         #
    ########################################################################

    def predict(self, context_test, events_test):
        """
          Semi-automatic mode predicts new risk labels based on Manual mode results

           Parameters
           ----------
           context_test : torch.Tensor
                   The input data of context events.

           events_test: torch.Tensor
                The input data of main sequence events.

           Returns
           -------
           prediction (torch.Tensor): tensor with predicted scores per sequence
       """
        prediction = self.interpreter.predict(
            X=context_test,  # Context to predict
            y=events_test.reshape(-1, 1),  # Events to predict, note that these should be of shape=(n_events, 1)
            iterations=100,  # Number of iterations to use for attention query, in paper this was 100
            batch_size=1024,  # Batch size to use for attention query, used to limit CUDA memory usage
            verbose=True,  # If True, prints progress
        )
        return prediction

    # repeat get_attention method with test data
