#!/usr/bin/env python3

import os
import json
import time
import logging
import unittest
from datetime import datetime
from metrics_collector import MetricsCollector
from ci_monitor import CIMonitor
from alert_manager import AlertManager

class TestMetricsCollection(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.test_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "test_metrics"
        )
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Setup logging
        log_file = os.path.join(self.test_dir, 'test_metrics.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.collector = MetricsCollector()
        self.monitor = CIMonitor()
        self.alert_manager = AlertManager()

    def test_metrics_collection(self):
        """Test basic metrics collection"""
        # Start collection
        self.collector.start_collection()
        time.sleep(2)  # Allow some metrics to be collected
        
        # Verify metrics
        metrics = self.collector.metrics
        self.assertIn('timestamps', metrics)
        self.assertIn('cpu_usage', metrics)
        self.assertIn('memory_usage', metrics)
        
        # Stop collection
        self.collector.stop_collection()

    def test_performance_metrics(self):
        """Test performance metrics collection"""
        # Simulate test execution
        test_result = {
            'duration': 1.5,
            'status': 'pass',
            'error': None
        }
        
        # Collect metrics
        self.collector.collect_test_metrics(test_result)
        
        # Verify metrics
        self.assertIn('test_results', self.collector.metrics)
        self.assertEqual(
            self.collector.metrics['test_results'][-1]['status'],
            'pass'
        )

    def test_quality_metrics(self):
        """Test quality metrics collection"""
        # Simulate quality data
        quality_data = {
            'completeness': 0.95,
            'consistency': 0.98,
            'validity': 0.97
        }
        
        # Analyze metrics
        analysis = self.collector.analyze_metrics()
        
        # Verify analysis
        self.assertIn('system', analysis)
        self.assertIn('tests', analysis)

    def test_metrics_storage(self):
        """Test metrics storage functionality"""
        # Generate test metrics
        test_metrics = {
            'response_time': 150,
            'cpu_usage': 45,
            'memory_usage': 1024 * 1024 * 100
        }
        
        # Save metrics
        metrics_file = self.collector.save_metrics()
        
        # Verify storage
        self.assertIsNotNone(metrics_file)
        self.assertTrue(os.path.exists(metrics_file))
        
        # Verify content
        with open(metrics_file, 'r') as f:
            data = json.load(f)
            self.assertIn('metrics', data)
            self.assertIn('analysis', data)
            self.assertIn('timestamp', data)

    def test_alert_integration(self):
        """Test alert integration"""
        # Set test thresholds
        thresholds = {
            'cpu_p95': 80,
            'memory_p95': 1024,
            'failure_rate': 0.1
        }
        
        # Check thresholds
        alerts = self.collector.check_thresholds(thresholds)
        
        # Verify alerts
        self.assertIsInstance(alerts, list)

    def test_monitor_integration(self):
        """Test monitor integration"""
        # Start monitoring
        self.monitor.start_monitoring()
        time.sleep(2)
        
        # Collect metrics
        metrics = self.monitor._get_test_metrics()
        
        # Verify metrics
        self.assertIsInstance(metrics, dict)
        self.assertIn('total', metrics)
        
        # Stop monitoring
        self.monitor.stop_monitoring()

    def test_error_handling(self):
        """Test error handling"""
        # Test invalid metrics
        with self.assertRaises(Exception):
            self.collector.analyze_metrics(None)
        
        # Test invalid thresholds
        with self.assertRaises(Exception):
            self.collector.check_thresholds(None)

    def tearDown(self):
        """Clean up test artifacts"""
        self.collector.stop_collection()
        self.logger.info("Test cleanup completed")

def run_tests():
    """Run test suite"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMetricsCollection)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
