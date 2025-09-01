#!/usr/bin/env python3

import os
import json
import yaml
import time
import logging
from datetime import datetime
from prometheus_client import start_http_server, Gauge, Counter, Histogram
from typing import Dict, Any

class CIMonitor:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(
            self.base_dir,
            "workflows/yaml_workflows/monitoring_config.yml"
        )
        self.metrics_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "metrics"
        )
        os.makedirs(self.metrics_dir, exist_ok=True)
        self.setup_logging()
        self.load_config()
        self.setup_metrics()

    def setup_logging(self):
        """Configure logging"""
        log_file = os.path.join(self.metrics_dir, 'ci_monitor.log')
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
        """Load monitoring configuration"""
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def setup_metrics(self):
        """Setup Prometheus metrics"""
        # Test execution metrics
        self.test_duration = Histogram(
            'test_execution_duration_seconds',
            'Test execution duration',
            ['category']
        )
        self.test_count = Counter(
            'test_total',
            'Total number of tests',
            ['category', 'status']
        )
        
        # Resource metrics
        self.cpu_usage = Gauge(
            'ci_cpu_usage_percent',
            'CI pipeline CPU usage'
        )
        self.memory_usage = Gauge(
            'ci_memory_usage_bytes',
            'CI pipeline memory usage'
        )
        
        # Quality metrics
        self.quality_score = Gauge(
            'data_quality_score',
            'Data quality score',
            ['metric']
        )
        
        # Pipeline metrics
        self.pipeline_duration = Histogram(
            'pipeline_duration_seconds',
            'Pipeline execution duration',
            ['stage']
        )
        self.pipeline_status = Gauge(
            'pipeline_status',
            'Pipeline execution status',
            ['stage']
        )

    def start_monitoring(self, port: int = 8000):
        """Start monitoring server"""
        start_http_server(port)
        self.logger.info(f"Monitoring server started on port {port}")

    def record_test_execution(self, category: str, duration: float, status: str):
        """Record test execution metrics"""
        self.test_duration.labels(category=category).observe(duration)
        self.test_count.labels(category=category, status=status).inc()

    def record_resource_usage(self, cpu: float, memory: float):
        """Record resource usage metrics"""
        self.cpu_usage.set(cpu)
        self.memory_usage.set(memory)

    def record_quality_metrics(self, metrics: Dict[str, float]):
        """Record quality metrics"""
        for metric, value in metrics.items():
            self.quality_score.labels(metric=metric).set(value)

    def record_pipeline_metrics(self, stage: str, duration: float, status: int):
        """Record pipeline metrics"""
        self.pipeline_duration.labels(stage=stage).observe(duration)
        self.pipeline_status.labels(stage=stage).set(status)

    def check_thresholds(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check metrics against thresholds"""
        alerts = []
        thresholds = self.config['monitoring']['alerts']['thresholds']
        
        # Check CPU usage
        if metrics.get('cpu_usage', 0) > thresholds['cpu_usage']:
            alerts.append({
                'severity': 'warning',
                'metric': 'cpu_usage',
                'value': metrics['cpu_usage'],
                'threshold': thresholds['cpu_usage']
            })
            
        # Check memory usage
        if metrics.get('memory_usage', 0) > thresholds['memory_usage']:
            alerts.append({
                'severity': 'warning',
                'metric': 'memory_usage',
                'value': metrics['memory_usage'],
                'threshold': thresholds['memory_usage']
            })
            
        # Check error rate
        error_rate = metrics.get('error_rate', 0)
        if error_rate > thresholds['error_rate']:
            alerts.append({
                'severity': 'error',
                'metric': 'error_rate',
                'value': error_rate,
                'threshold': thresholds['error_rate']
            })
            
        return alerts

    def save_metrics(self, metrics: Dict[str, Any]):
        """Save metrics to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        metrics_file = os.path.join(self.metrics_dir, f'ci_metrics_{timestamp}.json')
        
        with open(metrics_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'metrics': metrics
            }, f, indent=2)

    def monitor_pipeline(self):
        """Monitor CI pipeline execution"""
        try:
            self.start_monitoring()
            
            while True:
                # Collect metrics
                metrics = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu_usage': self._get_cpu_usage(),
                    'memory_usage': self._get_memory_usage(),
                    'test_metrics': self._get_test_metrics(),
                    'quality_metrics': self._get_quality_metrics()
                }
                
                # Record metrics
                self.record_resource_usage(
                    metrics['cpu_usage'],
                    metrics['memory_usage']
                )
                self.record_quality_metrics(metrics['quality_metrics'])
                
                # Check thresholds
                alerts = self.check_thresholds(metrics)
                if alerts:
                    self._handle_alerts(alerts)
                
                # Save metrics
                self.save_metrics(metrics)
                
                time.sleep(self.config['monitoring']['interval'])
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped")
        except Exception as e:
            self.logger.error(f"Error in monitoring: {str(e)}")
            raise

    def _get_cpu_usage(self) -> float:
        """Get CPU usage"""
        try:
            import psutil
            return psutil.cpu_percent()
        except:
            return 0.0

    def _get_memory_usage(self) -> float:
        """Get memory usage"""
        try:
            import psutil
            return psutil.Process().memory_info().rss
        except:
            return 0.0

    def _get_test_metrics(self) -> Dict[str, Any]:
        """Get test execution metrics"""
        return {
            'total': self.test_count._metrics['test_total'],
            'duration': self.test_duration._metrics['test_execution_duration_seconds']
        }

    def _get_quality_metrics(self) -> Dict[str, float]:
        """Get quality metrics"""
        return {
            name: metric._value
            for name, metric in self.quality_score._metrics.items()
        }

    def _handle_alerts(self, alerts: List[Dict[str, Any]]):
        """Handle monitoring alerts"""
        for alert in alerts:
            self.logger.warning(
                f"Alert: {alert['metric']} = {alert['value']} "
                f"(threshold: {alert['threshold']})"
            )
            
            # Send notifications if configured
            if self.config['monitoring']['alerts']['enabled']:
                self._send_alert_notification(alert)

    def _send_alert_notification(self, alert: Dict[str, Any]):
        """Send alert notification"""
        # Implementation specific to your notification system
        pass

def main():
    monitor = CIMonitor()
    monitor.monitor_pipeline()

if __name__ == "__main__":
    main()
