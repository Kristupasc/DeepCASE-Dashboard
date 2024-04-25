import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import torch
import numpy as np
from DeepCase.deepcase.context_builder import ContextBuilder
from DeepCase.deepcase.interpreter import Interpreter
from DeepCase.deepcase.preprocessing import Preprocessor

from Dashboard.processing.processor import Processor

class TestProcessor(unittest.TestCase):

    def setUp(self):

        # Patch the classes to use the mocks instead of the real things
        self.preprocessor_patch = patch('DeepCase.deepcase.preprocessing.Preprocessor')
        self.context_builder_patch = patch('DeepCase.deepcase.context_builder.ContextBuilder')
        self.interpreter_patch = patch('DeepCase.deepcase.interpreter.Interpreter')

        MockPreprocessor = self.preprocessor_patch.start()
        MockContextBuilder = self.context_builder_patch.start()
        MockInterpreter = self.interpreter_patch.start()

        self.mock_preprocessor = MockPreprocessor()
        self.mock_context_builder = MockContextBuilder()
        self.mock_interpreter = MockInterpreter()

        self.processor = Processor()

        self.processor.preprocessor = self.mock_preprocessor
        self.processor.context_builder = self.mock_context_builder
        self.processor.interpreter = self.mock_interpreter

        dummy_data = {'timestamp': {0: 1499075798.10912, 1: 1499075798.10912, 2: 1499075818.362352},
                      'machine': {0: '192.168.10.9', 1: '192.168.10.3', 2: '192.168.10.9'},
                      'event': {0: 'SURICATA STREAM CLOSEWAIT FIN out of window',
                                1: 'SURICATA STREAM CLOSEWAIT FIN out of window',
                                2: 'SURICATA STREAM CLOSEWAIT FIN out of window'},
                      'label': {0: 3, 1: 3, 2: 3}
                      }
        self.dummy_df = pd.DataFrame(dummy_data)
        self.filename = "test_alerts.csv"

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'


    def tearDown(self):
        self.preprocessor_patch.stop()
        self.context_builder_patch.stop()
        self.interpreter_patch.stop()

    def test_sequence_data(self):
        # Ensure all tensors are on the same device
        dummy_context = torch.tensor([1], device=self.device)
        dummy_events = torch.tensor([2], device=self.device)
        dummy_labels = np.array([3])
        dummy_mapping = {'map': 'test'}

        # Specify return values
        self.mock_preprocessor.sequence.return_value = (dummy_context, dummy_events, dummy_labels, dummy_mapping)

        # Act
        context, events, labels, mapping = self.processor.sequence_data(self.dummy_df)

        # Validate
        self.assertTrue(torch.equal(context, dummy_context))
        self.assertTrue(torch.equal(events, dummy_events))
        self.assertTrue(np.array_equal(labels, dummy_labels))
        self.assertEqual(mapping, dummy_mapping)

    def test_train_context_builder(self):
        dummy_context = torch.tensor([1], device=self.device)
        dummy_events = torch.tensor([2], device=self.device)

        # Specify return vars
        self.mock_context_builder.fit.return_value = None
        # Call Method
        self.processor.train_context_builder(dummy_context, dummy_events)
        # Validate
        self.mock_context_builder.fit.assert_called_once()

    def test_clustering(self):
        dummy_context = torch.tensor([1], device=self.device)
        dummy_events = torch.tensor([2], device=self.device)
        self.mock_interpreter.cluster.return_value = np.array([1])

        clusters = self.processor.clustering(dummy_context, dummy_events)
        print(self.mock_interpreter.cluster.call_args)

        self.mock_interpreter.cluster.assert_called_once_with(
            X=dummy_context,
            y=dummy_events.reshape(-1,1),
            iterations=100,
            batch_size=1024,
            verbose=True
        )
        self.assertTrue(np.array_equal(clusters, np.array([1])))

    def test_get_attention(self):
        dummy_context = torch.tensor([1], device=self.device)
        dummy_events = torch.tensor([2], device=self.device)
        dummy_confidence = torch.tensor([3], device=self.device)
        dummy_attention = torch.tensor([4], device=self.device)
        dummy_inverse = torch.tensor([0], device=self.device)

        self.mock_context_builder.query.return_value = (dummy_confidence, dummy_attention, dummy_inverse)

        confidence, attention = self.processor.get_attention(dummy_context, dummy_events)

        self.mock_context_builder.query.assert_called_once_with(
            X=dummy_context,
            y=dummy_events.reshape(-1, 1),
            iterations=100,
            batch_size=1024,
            verbose=True
        )
        # https://pytorch.org/docs/stable/testing.html
        torch.testing.assert_close(confidence, dummy_confidence[dummy_inverse])
        torch.testing.assert_close(attention, dummy_attention[dummy_inverse])

    def test_scoring(self):
        dummy_labels = torch.tensor([1], device=self.device)
        expected_scores = torch.tensor([2], device=self.device)

        self.mock_interpreter.score_clusters.return_value = expected_scores
        self.mock_interpreter.score.return_value = None

        actual_score = self.processor.scoring(dummy_labels)

        self.mock_interpreter.score_clusters.assert_called_once_with(
            scores = dummy_labels,
            strategy = "max",
            NO_SCORE=-1
        )

        self.mock_interpreter.score.assert_called_once_with(
            scores=expected_scores,
            verbose=True
        )
        # https://pytorch.org/docs/stable/testing.html
        torch.testing.assert_close(actual_score, expected_scores)

    def test_predict(self):
        dummy_context = torch.tensor([1], device=self.device)
        dummy_events = torch.tensor([2], device=self.device)

        dummy_prediction = torch.tensor([3], device=self.device)

        self.mock_interpreter.predict.return_value = dummy_prediction

        prediction = self.processor.predict(dummy_context, dummy_events)

        self.mock_interpreter.predict(
            X=dummy_context,
            y=dummy_events.reshape(-1, 1),
            iterations=100,
            batch_size=1024,
            verbose=True,
        )

        # https://pytorch.org/docs/stable/testing.html
        torch.testing.assert_close(prediction, dummy_prediction)


if __name__ == '__main__':
    unittest.main()
