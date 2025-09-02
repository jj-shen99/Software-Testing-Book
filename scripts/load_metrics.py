#!/usr/bin/env python3

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

def load_metrics(metrics_dir: str, time_range: str) -> Dict[str, Any]:
    """Load metrics from files based on time range"""
    days = {'1h': 1, '1d': 1, '1w': 7}[time_range]
    cutoff_time = datetime.now() - timedelta(days=days)
    
    metrics = {
        'performance': {
            'response_time': [],
            'throughput': [],
            'error_rate': []
        },
        'quality': None,
        'tests': None,
        'system': {
            'cpu_usage': [],
            'memory_usage': []
        }
    }
    
    latest_timestamp = None
    
    for root, _, files in os.walk(metrics_dir):
        for file in files:
            if file.startswith('metrics_'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    timestamp = datetime.fromisoformat(data['timestamp'])
                    
                    if timestamp >= cutoff_time:
                        # Collect performance metrics
                        for metric in metrics['performance']:
                            metrics['performance'][metric].extend(data['performance'][metric])
                        
                        # Collect system metrics
                        for metric in metrics['system']:
                            metrics['system'][metric].extend(data['system'][metric])
                        
                        # Update latest quality and test metrics
                        if latest_timestamp is None or timestamp > latest_timestamp:
                            latest_timestamp = timestamp
                            metrics['quality'] = data['quality']
                            metrics['tests'] = data['tests']
    
    # Set defaults if no data found
    if metrics['quality'] is None:
        metrics['quality'] = {
            'completeness': 1.0,
            'consistency': 1.0,
            'validity': 1.0
        }
    
    if metrics['tests'] is None:
        metrics['tests'] = {
            'passed': 0,
            'failed': 0,
            'skipped': 0
        }
    
    return metrics
