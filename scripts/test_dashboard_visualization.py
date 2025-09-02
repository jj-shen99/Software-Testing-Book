#!/usr/bin/env python3

import os
import unittest
import json
from datetime import datetime
from metrics_dashboard import MetricsDashboard
from metrics_visualizer import MetricsVisualizer

class TestDashboardVisualization(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.test_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "test_dashboard"
        )
        os.makedirs(self.test_dir, exist_ok=True)
        
        self.dashboard = MetricsDashboard()
        self.visualizer = MetricsVisualizer()
        
    def test_dashboard_layout(self):
        """Test dashboard layout configuration"""
        layout = self.dashboard.get_layout()
        self.assertIsNotNone(layout)
        self.assertIn('panels', layout)
        self.assertIn('styles', layout)
        
    def test_performance_graphs(self):
        """Test performance metric graphs"""
        test_data = {
            'response_time': [100, 150, 200],
            'throughput': [1000, 1200, 800],
            'error_rate': [0.01, 0.02, 0.015]
        }
        graphs = self.visualizer.create_performance_graphs(test_data)
        self.assertGreater(len(graphs), 0)
        
    def test_quality_metrics(self):
        """Test quality metrics visualization"""
        quality_data = {
            'completeness': 0.95,
            'consistency': 0.98,
            'validity': 0.92
        }
        gauges = self.visualizer.create_quality_gauges(quality_data)
        self.assertGreater(len(gauges), 0)
        
    def test_test_results(self):
        """Test test results visualization"""
        test_data = {
            'passed': 95,
            'failed': 3,
            'skipped': 2
        }
        charts = self.visualizer.create_test_charts(test_data)
        self.assertGreater(len(charts), 0)
        
    def test_trend_analysis(self):
        """Test trend analysis visualization"""
        trend_data = {
            'timestamps': ['2025-09-01T10:00:00', '2025-09-01T11:00:00'],
            'values': [95, 97]
        }
        trend_chart = self.visualizer.create_trend_chart(trend_data)
        self.assertIsNotNone(trend_chart)
        
    def test_export_dashboard(self):
        """Test dashboard export functionality"""
        export_file = os.path.join(self.test_dir, 'dashboard_export.json')
        self.dashboard.export_dashboard(export_file)
        self.assertTrue(os.path.exists(export_file))
        
        with open(export_file, 'r') as f:
            data = json.load(f)
            self.assertIn('layout', data)
            self.assertIn('panels', data)
            
    def test_interactive_features(self):
        """Test dashboard interactive features"""
        callbacks = self.dashboard.get_callbacks()
        self.assertGreater(len(callbacks), 0)
        
    def test_data_refresh(self):
        """Test data refresh functionality"""
        refresh_interval = self.dashboard.get_refresh_interval()
        self.assertGreater(refresh_interval, 0)
        
    def tearDown(self):
        """Clean up test artifacts"""
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()
