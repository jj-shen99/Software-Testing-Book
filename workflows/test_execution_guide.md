# Test Execution Guide

## Quick Start
```bash
# Run all tests
./scripts/test_runner.py

# Run specific category
./scripts/test_runner.py --category unit
./scripts/test_runner.py --category integration
./scripts/test_runner.py --category performance
```

## Test Categories

### Unit Tests
```bash
# Run with coverage
./scripts/test_runner.py --category unit --coverage

# Run specific test
./scripts/test_runner.py --test triangle_area_test
```

### Integration Tests
```bash
# Run with specific environment
./scripts/test_runner.py --category integration --env staging

# Run with dependencies
./scripts/test_runner.py --category integration --with-deps
```

### Performance Tests
```bash
# Run load test
./scripts/performance_tester.py --type load --users 100

# Run stress test
./scripts/performance_tester.py --type stress --duration 3600
```

## Configuration

### Test Workflow Config
```yaml
# workflows/yaml_workflows/test_workflow_config.yml
execution:
  parallel: true
  max_workers: 4
  timeout: 300

categories:
  unit:
    priority: high
    parallel: true
  integration:
    priority: medium
    parallel: false
```

### Test Data Config
```yaml
test_data:
  datasets:
    small: 15 cases
    medium: 150 cases
    large: 1500 cases
    performance: 10000 cases
```

## Results Analysis

### Generate Reports
```bash
# HTML report
./scripts/test_analyzer.py --format html

# JSON metrics
./scripts/test_analyzer.py --format json --metrics

# Performance graphs
./scripts/test_analyzer.py --plot performance
```

### View Dashboard
```bash
# Launch dashboard
./scripts/test_dashboard.py

# Monitor live execution
./scripts/test_dashboard.py --live
```

## Best Practices

### 1. Test Organization
- Group related tests
- Use clear naming
- Follow priority order
- Maintain independence

### 2. Test Data
- Use appropriate dataset
- Validate before use
- Clean up after tests
- Version control data

### 3. Performance
- Monitor resource usage
- Set realistic timeouts
- Clean up between runs
- Archive results regularly

### 4. CI/CD Integration
- Configure triggers
- Set up notifications
- Monitor build status
- Review test reports

## Troubleshooting

### Common Issues
1. **Test Timeouts**
   ```bash
   # Increase timeout
   ./scripts/test_runner.py --timeout 600
   ```

2. **Resource Constraints**
   ```bash
   # Reduce parallel execution
   ./scripts/test_runner.py --workers 2
   ```

3. **Data Issues**
   ```bash
   # Validate test data
   ./scripts/test_data_validator.py
   ```

### Getting Help
```bash
# Show help
./scripts/test_runner.py --help
./scripts/test_analyzer.py --help
./scripts/performance_tester.py --help
```
