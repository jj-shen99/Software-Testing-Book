# Dashboard Integration Guide

## Quick Start
```bash
# Start dashboard integration
./scripts/dashboard_integration.py

# Push metrics
./scripts/dashboard_integration.py --push-metrics

# Export dashboard
./scripts/dashboard_integration.py --export-dashboard
```

## Integration Components

### 1. Prometheus Integration
```yaml
prometheus:
  gateway: localhost:9091
  job_name: test_metrics
  metrics:
    - test_response_time_ms
    - test_cpu_usage_percent
    - test_memory_usage_bytes
```

### 2. Grafana Integration
```yaml
grafana:
  url: http://localhost:3000
  dashboard:
    title: Test Metrics
    refresh: 30s
    panels:
      - response_time
      - cpu_usage
      - memory_usage
```

### 3. Alert Integration
```yaml
alerts:
  rules:
    - metric: test_response_time_ms
      threshold: 1000
      severity: warning
    - metric: test_cpu_usage_percent
      threshold: 80
      severity: critical
```

## Configuration

### Metric Export
```yaml
export:
  formats:
    - prometheus
    - json
    - csv
  
  prometheus:
    gateway: localhost:9091
    retention: 15d
    
  file:
    path: metrics/export
    format: json
```

### Dashboard Layout
```yaml
layout:
  theme: light
  refresh: 30
  panels:
    response_time:
      type: graph
      size: medium
    cpu_usage:
      type: gauge
      size: small
```

## Best Practices

### 1. Metric Collection
- Use consistent naming
- Set appropriate intervals
- Define clear thresholds
- Document metrics

### 2. Dashboard Design
- Group related metrics
- Use appropriate visualizations
- Set refresh intervals
- Configure alerts

### 3. Integration Setup
- Test connections
- Monitor performance
- Handle errors
- Back up configurations

## Troubleshooting

### Common Issues
1. **Connection Issues**
   ```bash
   # Test connections
   ./scripts/dashboard_integration.py --test-connection
   ```

2. **Metric Issues**
   ```bash
   # Validate metrics
   ./scripts/dashboard_integration.py --validate-metrics
   ```

3. **Export Issues**
   ```bash
   # Check export
   ./scripts/dashboard_integration.py --check-export
   ```

### Getting Help
```bash
# Show integration help
./scripts/dashboard_integration.py --help

# List available commands
./scripts/dashboard_integration.py --list-commands
```

## Integration Examples

### 1. With CI Pipeline
```python
# Integrate with CI
from dashboard_integration import DashboardIntegration
integration = DashboardIntegration()

# Push CI metrics
integration.integrate_with_ci({
    'cpu_usage': 45.5,
    'memory_usage': 1024 * 1024 * 100,
    'test_results': {
        'pass': 95,
        'fail': 5
    }
})
```

### 2. With Alert System
```python
# Integrate with alerts
from alert_manager import AlertManager
alert_manager = AlertManager()

# Configure alert integration
integration.integrate_with_alerts(alert_manager)
```

### 3. With Monitoring
```python
# Integrate with monitoring
from ci_monitor import CIMonitor
monitor = CIMonitor()

# Configure monitoring integration
integration.integrate_with_monitoring(monitor)
```

## API Reference

### Metric Push
```python
# Push custom metrics
integration.push_metrics({
    'performance': {
        'avg_response_time': 150,
        'p95_response_time': 250
    },
    'test': {
        'results': {'pass': 95, 'fail': 5},
        'duration': 2.5
    },
    'quality': {
        'score': 0.95,
        'coverage': 0.85
    }
})
```

### Dashboard Export
```python
# Export dashboard configuration
dashboard_file = integration.export_grafana_dashboard()

# Export metrics
metrics_file = integration.export_metrics('json')
```

### Alert Configuration
```python
# Configure alert rules
integration.configure_alerts([
    {
        'metric': 'response_time',
        'threshold': 1000,
        'severity': 'warning'
    },
    {
        'metric': 'error_rate',
        'threshold': 5,
        'severity': 'critical'
    }
])
```
