#!/usr/bin/env python3

import os
import json
import time
import psutil
import threading
from datetime import datetime
from collections import defaultdict
import numpy as np

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
        self.metrics = defaultdict(list)
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
            
    def collect_test_metrics(self, test_result):
        """Collect test execution metrics"""
        self.metrics['test_results'].append({
            'timestamp': datetime.now().isoformat(),
            'duration': test_result.get('duration'),
            'status': test_result.get('status'),
            'error': test_result.get('error')
        })
        
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
        analysis = {
            'system': {
                'cpu': {
                    'avg': np.mean(self.metrics['cpu_usage']),
                    'max': np.max(self.metrics['cpu_usage']),
                    'p95': np.percentile(self.metrics['cpu_usage'], 95)
                },
                'memory': {
                    'avg': np.mean(self.metrics['memory_usage']),
                    'max': np.max(self.metrics['memory_usage']),
                    'p95': np.percentile(self.metrics['memory_usage'], 95)
                }
            },
            'tests': {
                'total': len(self.metrics['test_results']),
                'success': sum(1 for t in self.metrics['test_results'] 
                             if t['status'] == 'pass'),
                'failure': sum(1 for t in self.metrics['test_results'] 
                             if t['status'] == 'fail'),
                'avg_duration': np.mean([t['duration'] for t in self.metrics['test_results']
                                      if t['duration'] is not None])
            }
        }
        
        if self.metrics['performance']:
            analysis['performance'] = {
                'response_time': {
                    'avg': np.mean([p['response_time'] for p in self.metrics['performance']]),
                    'p95': np.percentile([p['response_time'] for p in self.metrics['performance']], 95)
                },
                'throughput': {
                    'avg': np.mean([p['throughput'] for p in self.metrics['performance']]),
                    'max': np.max([p['throughput'] for p in self.metrics['performance']])
                }
            }
            
        return analysis
        
    def save_metrics(self):
        """Save metrics to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        metrics_file = os.path.join(self.metrics_dir, f'metrics_{timestamp}.json')
        
        with open(metrics_file, 'w') as f:
            json.dump({
                'metrics': dict(self.metrics),
                'analysis': self.analyze_metrics()
            }, f, indent=2)
            
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
        failure_rate = (analysis['tests']['failure'] / analysis['tests']['total'] 
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
