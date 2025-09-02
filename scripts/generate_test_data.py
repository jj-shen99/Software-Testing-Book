#!/usr/bin/env python3

import os
import json
import random
from datetime import datetime, timedelta

def generate_test_results(num_tests=100, days=7):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    metrics_dir = os.path.join(
        base_dir,
        "sample_analysis_results",
        f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
        "metrics"
    )
    os.makedirs(metrics_dir, exist_ok=True)
    
    # Generate data for each day
    for day in range(days):
        date = datetime.now() - timedelta(days=day)
        metrics = {
            'timestamp': date.isoformat(),
            'performance': {
                'response_time': [random.uniform(50, 500) for _ in range(num_tests)],
                'throughput': [random.randint(800, 2000) for _ in range(num_tests)],
                'error_rate': [random.uniform(0, 0.05) for _ in range(num_tests)]
            },
            'quality': {
                'completeness': random.uniform(0.90, 1.0),
                'consistency': random.uniform(0.85, 1.0),
                'validity': random.uniform(0.95, 1.0)
            },
            'tests': {
                'passed': random.randint(85, 98),
                'failed': random.randint(1, 5),
                'skipped': random.randint(0, 3)
            }
        }
        
        # Add system metrics
        metrics['system'] = {
            'cpu_usage': [random.uniform(20, 80) for _ in range(24)],  # 24 hours
            'memory_usage': [random.uniform(512 * 1024 * 1024, 2048 * 1024 * 1024) for _ in range(24)]
        }
        
        # Save metrics
        filename = f'metrics_{date.strftime("%Y%m%d_%H%M%S")}.json'
        filepath = os.path.join(metrics_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
            
if __name__ == '__main__':
    generate_test_results()
