#!/usr/bin/env python3

import os
import json
import time
import logging
import threading
import numpy as np
from datetime import datetime
from collections import defaultdict
from load_metrics import load_metrics
import psutil

class MetricsCollector:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.metrics_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "metrics"
        )
        os.makedirs(self.metrics_dir, exist_ok=True)
        
        # Setup logging
        log_file = os.path.join(self.metrics_dir, 'metrics.log')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Add handlers if they don't exist
        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(file_handler)
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(console_handler)
        
        self.metrics = {
            'timestamps': [],
            'cpu_usage': [0],
            'memory_usage': [0],
            'test_results': [],
            'performance': [],
            'quality_metrics': {
                'completeness': 1.0,
                'consistency': 1.0,
                'validity': 1.0
            }
        }
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.metrics_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "metrics"
        )
        os.makedirs(self.metrics_dir, exist_ok=True)
        
        # Setup logging
        log_file = os.path.join(self.metrics_dir, 'metrics.log')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Add handlers if they don't exist
        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(file_handler)
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(console_handler)
        
        self.metrics = {
            'timestamps': [],
            'cpu_usage': [0],
            'memory_usage': [0],
            'test_results': [],
            'performance': [],
            'quality_metrics': {
                'completeness': 1.0,
                'consistency': 1.0,
                'validity': 1.0
            }
        }
        self.running = False
        
    def start_collection(self, interval=1):
        """Start collecting metrics"""
        self.running = True
        self.collection_thread = threading.Thread(
            target=self._collect_metrics,
            args=(interval,)
        )
        self.collection_thread.start()
        
    def stop_collection(self):
        """Stop collecting metrics"""
        self.running = False
        if hasattr(self, 'collection_thread'):
            self.collection_thread.join()
            
    def _collect_metrics(self, interval):
        """Collect system and test metrics"""
        while self.running:
            timestamp = datetime.now().isoformat()
            
            # System metrics
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # Store metrics
            self.metrics['timestamps'].append(timestamp)
            self.metrics['cpu_usage'].append(cpu)
            self.metrics['memory_usage'].append(memory)
            
            time.sleep(interval)
            
    def _calculate_stats(self, values):
        """Calculate statistics for a list of values"""
        try:
            if not values or len(values) == 0:
                return {'mean': 0, 'max': 0, 'p95': 0}
                
            values = np.array(values)
            if not np.isfinite(values).all():
                values = values[np.isfinite(values)]
                
            if len(values) == 0:
                return {'mean': 0, 'max': 0, 'p95': 0}
                
            return {
                'mean': float(np.mean(values)),
                'max': float(np.max(values)),
                'p95': float(np.percentile(values, 95)) if len(values) > 1 else float(np.max(values))
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating stats: {str(e)}")
            return {'mean': 0, 'max': 0, 'p95': 0}
            
    def collect_test_metrics(self, test_result):
        """Collect test execution metrics"""
        try:
            metrics = load_metrics(self.metrics_dir, '1h')
            
            # Update test metrics
            if test_result:
                # Add test result
                self.metrics['test_results'].append({
                    'timestamp': datetime.now().isoformat(),
                    'duration': test_result.get('duration', 0),
                    'status': test_result.get('status', 'unknown'),
                    'error': test_result.get('error')
                })
                
                # Update quality metrics if available
                if 'quality' in test_result:
                    self.metrics['quality_metrics'].update(test_result['quality'])
                    
                self.logger.info(f"Collected test metrics: {test_result}")
                
        except Exception as e:
            self.logger.error(f"Error collecting test metrics: {str(e)}")
                
    def collect_performance_metrics(self, perf_data):
        """Collect performance test metrics"""
        self.metrics['performance'].append({
            'timestamp': datetime.now().isoformat(),
            'response_time': perf_data.get('response_time'),
            'throughput': perf_data.get('throughput'),
            'concurrent_users': perf_data.get('users')
        })
        
    def analyze_metrics(self):
        """Analyze collected metrics"""
        try:
            # Get metrics with defaults
            cpu_metrics = self.metrics.get('cpu_usage', [0])
            memory_metrics = self.metrics.get('memory_usage', [0])
            test_results = self.metrics.get('test_results', [])
            quality_metrics = self.metrics.get('quality_metrics', {
                'completeness': 1.0,
                'consistency': 1.0,
                'validity': 1.0
            })
            
            # Calculate system metrics safely
            system_metrics = {
                'cpu': self._calculate_stats(cpu_metrics),
                'memory': self._calculate_stats(memory_metrics)
            }
            
            # Calculate test metrics
            test_metrics = {
                'total': len(test_results),
                'passed': sum(1 for r in test_results if r.get('status') == 'pass'),
                'failed': sum(1 for r in test_results if r.get('status') == 'fail')
            }
            
            return {
                'system': system_metrics,
                'tests': test_metrics,
                'quality': quality_metrics
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing metrics: {str(e)}")
            return {
                'system': {'cpu': {'mean': 0, 'max': 0, 'p95': 0},
                          'memory': {'mean': 0, 'max': 0, 'p95': 0}},
                'tests': {'total': 0, 'passed': 0, 'failed': 0},
                'quality': {'completeness': 1.0, 'consistency': 1.0, 'validity': 1.0}
            }
        
    def save_metrics(self):
        """Save metrics to file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            metrics_file = os.path.join(self.metrics_dir, f'metrics_{timestamp}.json')
            
            with open(metrics_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'metrics': dict(self.metrics),
                    'analysis': self.analyze_metrics()
                }, f, indent=2)
                
            self.logger.info(f"Metrics saved to {metrics_file}")
            return metrics_file
            
        except Exception as e:
            self.logger.error(f"Error saving metrics: {str(e)}")
            return None
            
    def check_thresholds(self, thresholds):
        """Check metrics against thresholds"""
        alerts = []
        analysis = self.analyze_metrics()
        
        # CPU threshold
        if analysis['system']['cpu']['p95'] > thresholds.get('cpu_p95', 80):
            alerts.append({
                'level': 'warning',
                'metric': 'cpu',
                'message': f"CPU usage above threshold: {analysis['system']['cpu']['p95']}%"
            })
            
        # Memory threshold
        if analysis['system']['memory']['p95'] > thresholds.get('memory_p95', 1024):
            alerts.append({
                'level': 'warning',
                'metric': 'memory',
                'message': f"Memory usage above threshold: {analysis['system']['memory']['p95']}MB"
            })
            
        # Test failure threshold
        failure_rate = (analysis['tests']['failed'] / analysis['tests']['total'] 
                       if analysis['tests']['total'] > 0 else 0)
        if failure_rate > thresholds.get('failure_rate', 0.1):
            alerts.append({
                'level': 'error',
                'metric': 'tests',
                'message': f"Test failure rate above threshold: {failure_rate:.2%}"
            })
            
        return alerts

def main():
    collector = MetricsCollector()
    
    try:
        # Start metrics collection
        collector.start_collection(interval=1)
        
        # Simulate test execution
        time.sleep(10)
        
        # Stop collection and save results
        collector.stop_collection()
        collector.save_metrics()
        
        # Check thresholds
        alerts = collector.check_thresholds({
            'cpu_p95': 80,
            'memory_p95': 1024,
            'failure_rate': 0.1
        })
        
        if alerts:
            print("\nAlerts:")
            for alert in alerts:
                print(f"[{alert['level'].upper()}] {alert['message']}")
                
    except KeyboardInterrupt:
        collector.stop_collection()
        collector.save_metrics()

if __name__ == "__main__":
    main()
