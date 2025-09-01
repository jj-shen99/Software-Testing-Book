#!/usr/bin/env python3

import os
import json
import yaml
import logging
from datetime import datetime
from typing import Dict, Any, List
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

class DashboardIntegration:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(self.base_dir, "scripts/dashboard_layout.yml")
        self.integration_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "integrations"
        )
        os.makedirs(self.integration_dir, exist_ok=True)
        self.setup_logging()
        self.load_config()
        self.setup_prometheus()

    def setup_logging(self):
        """Configure logging"""
        log_file = os.path.join(self.integration_dir, 'integration.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self):
        """Load dashboard configuration"""
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def setup_prometheus(self):
        """Setup Prometheus metrics"""
        self.registry = CollectorRegistry()
        
        # Performance metrics
        self.response_time = Gauge(
            'test_response_time_ms',
            'Test response time in milliseconds',
            ['type'],
            registry=self.registry
        )
        self.cpu_usage = Gauge(
            'test_cpu_usage_percent',
            'Test CPU usage percentage',
            registry=self.registry
        )
        self.memory_usage = Gauge(
            'test_memory_usage_bytes',
            'Test memory usage in bytes',
            registry=self.registry
        )
        
        # Test metrics
        self.test_results = Gauge(
            'test_results_total',
            'Test results count',
            ['status'],
            registry=self.registry
        )
        self.test_duration = Gauge(
            'test_duration_seconds',
            'Test execution duration',
            ['type'],
            registry=self.registry
        )
        
        # Quality metrics
        self.quality_score = Gauge(
            'test_quality_score',
            'Test quality score',
            ['metric'],
            registry=self.registry
        )

    def push_metrics(self, metrics: Dict[str, Any]):
        """Push metrics to Prometheus"""
        try:
            # Performance metrics
            self.response_time.labels('avg').set(metrics['performance']['avg_response_time'])
            self.response_time.labels('p95').set(metrics['performance']['p95_response_time'])
            self.cpu_usage.set(metrics['performance']['cpu_percent'])
            self.memory_usage.set(metrics['performance']['memory_bytes'])
            
            # Test metrics
            for status, count in metrics['test']['results'].items():
                self.test_results.labels(status).set(count)
            self.test_duration.labels('avg').set(metrics['test']['avg_duration'])
            
            # Quality metrics
            for metric, value in metrics['quality'].items():
                self.quality_score.labels(metric).set(value)
            
            # Push to Prometheus
            push_to_gateway(
                self.config['export']['prometheus']['gateway'],
                job='test_metrics',
                registry=self.registry
            )
            
            self.logger.info("Metrics pushed to Prometheus successfully")
            
        except Exception as e:
            self.logger.error(f"Error pushing metrics: {str(e)}")

    def export_grafana_dashboard(self):
        """Export Grafana dashboard configuration"""
        dashboard = {
            'title': 'Test Metrics Dashboard',
            'timezone': 'browser',
            'panels': []
        }
        
        # Add panels from layout config
        for panel_id, panel in enumerate(self.config['panels'].values()):
            dashboard['panels'].append({
                'id': panel_id,
                'title': panel['title'],
                'type': panel['type'],
                'gridPos': {
                    'x': panel['position']['col'] - 1,
                    'y': (panel['position']['row'] - 1) * 8,
                    'w': self.config['layout']['sizes'][panel['size']]['width'] * 6,
                    'h': self.config['layout']['sizes'][panel['size']]['height'] * 8
                },
                'targets': [
                    {'expr': f'test_{metric}' for metric in panel['metrics']}
                ]
            })
        
        # Save dashboard
        dashboard_file = os.path.join(
            self.integration_dir,
            f"grafana_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(dashboard_file, 'w') as f:
            json.dump(dashboard, f, indent=2)
            
        self.logger.info(f"Grafana dashboard exported to {dashboard_file}")
        
        return dashboard_file

    def export_metrics(self, format: str):
        """Export metrics in specified format"""
        metrics_file = os.path.join(
            self.integration_dir,
            f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        )
        
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'metrics': {
                    name: gauge._value
                    for name, gauge in self.registry._names_to_collectors.items()
                }
            }
            
            if format == 'json':
                with open(metrics_file, 'w') as f:
                    json.dump(metrics, f, indent=2)
            elif format == 'csv':
                import pandas as pd
                df = pd.DataFrame([metrics])
                df.to_csv(metrics_file, index=False)
                
            self.logger.info(f"Metrics exported to {metrics_file}")
            
            return metrics_file
            
        except Exception as e:
            self.logger.error(f"Error exporting metrics: {str(e)}")
            return None

    def integrate_with_ci(self, ci_metrics: Dict[str, Any]):
        """Integrate with CI pipeline"""
        try:
            # Update metrics with CI data
            self.cpu_usage.set(ci_metrics.get('cpu_usage', 0))
            self.memory_usage.set(ci_metrics.get('memory_usage', 0))
            
            for status, count in ci_metrics.get('test_results', {}).items():
                self.test_results.labels(status).set(count)
                
            # Export metrics
            self.export_metrics('json')
            
            self.logger.info("CI metrics integrated successfully")
            
        except Exception as e:
            self.logger.error(f"Error integrating CI metrics: {str(e)}")

    def integrate_with_alerts(self, alert_manager):
        """Integrate with alert system"""
        try:
            # Set up alert rules based on metrics
            rules = []
            
            # Performance alerts
            rules.append({
                'metric': 'test_response_time_ms{type="p95"}',
                'threshold': self.config['panels']['response_time']['thresholds']['warning'],
                'severity': 'warning'
            })
            
            # Resource alerts
            rules.append({
                'metric': 'test_cpu_usage_percent',
                'threshold': self.config['panels']['cpu_usage']['thresholds']['warning'],
                'severity': 'warning'
            })
            
            # Quality alerts
            rules.append({
                'metric': 'test_quality_score{metric="overall"}',
                'threshold': self.config['panels']['quality_score']['thresholds']['warning'],
                'severity': 'warning'
            })
            
            # Register alert rules
            alert_manager.register_rules(rules)
            
            self.logger.info("Alert integration configured successfully")
            
        except Exception as e:
            self.logger.error(f"Error integrating alerts: {str(e)}")

def main():
    integration = DashboardIntegration()
    
    # Example metrics
    metrics = {
        'performance': {
            'avg_response_time': 150,
            'p95_response_time': 250,
            'cpu_percent': 45,
            'memory_bytes': 1024 * 1024 * 100
        },
        'test': {
            'results': {
                'pass': 95,
                'fail': 5
            },
            'avg_duration': 2.5
        },
        'quality': {
            'overall': 0.95,
            'coverage': 0.85
        }
    }
    
    # Push metrics
    integration.push_metrics(metrics)
    
    # Export dashboard
    integration.export_grafana_dashboard()
    
    # Export metrics
    integration.export_metrics('json')

if __name__ == "__main__":
    main()
