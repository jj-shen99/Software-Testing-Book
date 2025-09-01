# Test Workflow Guide

## Quick Start
```bash
# Run all tests
./scripts/test_workflow_runner.py

# Run specific category
./scripts/test_workflow_runner.py --category unit

# Generate report only
./scripts/test_workflow_runner.py --report-only
```

## Workflow Components

### 1. Test Categories
```yaml
categories:
  unit:
    priority: high
    parallel: true
    timeout: 60
    
  integration:
    priority: medium
    parallel: false
    timeout: 120
```

### 2. Environment Setup
```yaml
environment:
  setup:
    - clean_workspace
    - init_database
    - load_test_data
```

### 3. Test Execution
```python
# Run tests with custom config
runner = TestWorkflowRunner()
results = runner.run_tests(
    category='unit',
    parallel=True,
    timeout=60
)
```

## Configuration

### Test Settings
```yaml
execution:
  parallel: true
  max_workers: 4
  timeout: 300
  retry:
    enabled: true
    max_attempts: 3
```

### Resource Limits
```yaml
resources:
  cpu:
    limit: 4
    request: 2
  memory:
    limit: "4Gi"
    request: "2Gi"
```

## Test Results

### Results Structure
```json
{
    "total_tests": 100,
    "passed": 95,
    "failed": 3,
    "errors": 2,
    "categories": {
        "unit": {
            "total": 50,
            "passed": 48,
            "failed": 2
        }
    }
}
```

### Report Generation
```bash
# Generate HTML report
./scripts/test_workflow_runner.py --format html

# Generate markdown report
./scripts/test_workflow_runner.py --format markdown
```

## Best Practices

### 1. Test Organization
- Group by category
- Follow naming conventions
- Set appropriate timeouts
- Enable parallel execution

### 2. Resource Management
- Monitor usage
- Set resource limits
- Clean up after tests
- Archive results

### 3. CI/CD Integration
- Configure triggers
- Set up notifications
- Monitor builds
- Archive artifacts

## Troubleshooting

### Common Issues
1. **Test Timeouts**
   ```bash
   # Increase timeout
   ./scripts/test_workflow_runner.py --timeout 600
   ```

2. **Resource Constraints**
   ```bash
   # Reduce parallel execution
   ./scripts/test_workflow_runner.py --workers 2
   ```

3. **Environment Issues**
   ```bash
   # Validate environment
   ./scripts/test_workflow_runner.py --check-env
   ```

### Getting Help
```bash
# Show workflow help
./scripts/test_workflow_runner.py --help

# List available commands
./scripts/test_workflow_runner.py --list-commands
```

## Integration

### 1. With Data Quality
```python
# Integrate with data validation
from data_quality_validator import DataQualityValidator
validator = DataQualityValidator()
validation = validator.validate_dataset(data)
```

### 2. With Monitoring
```python
# Monitor test execution
from data_quality_monitor import DataQualityMonitor
monitor = DataQualityMonitor()
monitor.track_execution(workflow)
```

### 3. With Dashboard
```python
# View results in dashboard
from data_quality_dashboard import DataQualityDashboard
dashboard = DataQualityDashboard()
dashboard.show_workflow_results(results)
```
