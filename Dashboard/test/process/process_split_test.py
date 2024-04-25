import unittest
from unittest.mock import patch
import pandas as pd

from Dashboard.processing.process_split import ProcessorAccessObject

class TestProcessorAccessObject(unittest.TestCase):
    def setUp(self):
        self.patcher_dao = patch('Dashboard.data.dao.dao.DAO')
        self.patcher_processor = patch('Dashboard.processing.processor.Processor')

        MockDAO = self.patcher_dao.start()
        MockProcessor = self.patcher_processor.start()

        self.mock_dao = MockDAO()
        self.mock_processor = MockProcessor()

        self.pao = ProcessorAccessObject()

        self.pao.dao = self.mock_dao
        self.pao.processor = self.mock_processor

        dummy_data = {'timestamp': {0: 1499075798.10912, 1: 1499075798.10912, 2: 1499075818.362352},
                      'machine': {0: '192.168.10.9', 1: '192.168.10.3', 2: '192.168.10.9'},
                      'event': {0: 'SURICATA STREAM CLOSEWAIT FIN out of window',
                                1: 'SURICATA STREAM CLOSEWAIT FIN out of window',
                                2: 'SURICATA STREAM CLOSEWAIT FIN out of window'},
                      'label': {0: 3, 1: 3, 2: 3}
                      }
        self.dummy_df = pd.DataFrame(dummy_data)
        self.filename = "test_alerts.csv"

    def tearDown(self):
        self.patcher_dao.stop()
        self.patcher_processor.stop()

    def test_run_DeepCase(self):
        # Set up expected returns
        self.mock_dao.save_input.return_value = None

        self.mock_processor.sequence_data.return_value = ('context', 'events', 'labels', 'mapping')
        self.mock_dao.save_sequencing_results.return_value = None

        self.mock_processor.train_context_builder.return_value = None

        self.mock_processor.clustering.return_value = 'clusters'
        self.mock_processor.get_attention.return_value = ('confidence', 'attention')
        self.mock_dao.save_clustering_results.return_value = None

        self.mock_processor.scoring.return_value = 'scores'
        self.mock_dao.set_new_cluster_scores.return_value = None

        self.mock_dao.set_run_status.return_value = None

        # Run method to be tested
        self.mock_dao.save_input(self.dummy_df, filename=self.filename)
        self.pao.run_DeepCASE()

        # Verify call to mock processes
        self.mock_dao.save_input.assert_called_once()

        self.mock_processor.sequence_data.assert_called_once()
        self.mock_dao.save_sequencing_results.assert_called_once()

        self.mock_processor.train_context_builder.assert_called_once()

        self.mock_processor.clustering.assert_called_once()
        self.mock_processor.get_attention.assert_called_once()
        self.mock_dao.save_clustering_results.assert_called_once()

        self.mock_processor.scoring.assert_called_once()
        self.mock_dao.set_new_cluster_scores.assert_called_once()

        self.mock_dao.set_run_status.assert_called_once()

    def test_run_automatic(self):
        # Set up expected returns
        self.mock_processor.predict.return_value = 'prediction'
        self.mock_dao.update_cluster_scores.return_value = None
        self.mock_processor.get_attention.return_value = ('confidence', 'attention')
        self.mock_dao.update_attention.return_value = None

        # Call method
        self.pao.run_automatic_mode()

        # Verify interactions with mock processes
        self.mock_processor.predict.assert_called_once()
        self.mock_dao.update_cluster_scores.assert_called_once()
        self.mock_processor.get_attention.assert_called_once()
        self.mock_dao.update_attention.assert_called_once()

    def test_get_context_tensor(self):
        # Set up expected cals and returns
        self.mock_dao.get_context_auto.result_value = 'result_tensor'
        # Call method
        self.pao.get_context_tensor()
        # Verify interactions with mock
        self.mock_dao.get_context_auto.assert_called_once()

    def test_get_event_tensor(self):
        # Set up expected cals and returns
        self.mock_dao.get_events_auto.result_value = 'result_tensor'
        # Call method
        self.pao.get_event_tensor()
        # Verify interactions with mock
        self.mock_dao.get_events_auto.assert_called_once()

if __name__ == '__main__':
    unittest.main()
