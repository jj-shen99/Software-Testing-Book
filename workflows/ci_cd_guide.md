# CI/CD Pipeline Guide

## Quick Start
```bash
# Run CI pipeline locally
./scripts/test_workflow_runner.py --ci

# Validate CI configuration
./scripts/test_workflow_runner.py --validate-ci

# Test deployment
./scripts/test_workflow_runner.py --deploy-dry-run
```

## Pipeline Components

### 1. Test Execution
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - name: Run tests
      run: python scripts/test_workflow_runner.py
```

### 2. Data Validation
```yaml
steps:
  - name: Validate data
    run: |
      python scripts/data_quality_validator.py
      python scripts/test_data_profiler.py
```

### 3. Report Generation
```yaml
steps:
  - name: Generate reports
    run: |
      python scripts/data_quality_dashboard.py
      python scripts/profile_visualizer.py
```

## Configuration

### Pipeline Settings
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 0 * * *'  # Daily
```

### Environment Matrix
```yaml
strategy:
  matrix:
    python-version: [3.8, 3.9]
    os: [ubuntu-latest]
```

## Artifacts

### Test Results
```yaml
- name: Upload results
  uses: actions/upload-artifact@v2
  with:
    name: test-results
    path: sample_analysis_results/test_results_*
```

### Reports
```yaml
- name: Upload reports
  uses: actions/upload-artifact@v2
  with:
    name: test-reports
    path: sample_analysis_results/*/reports
```

## Best Practices

### 1. Pipeline Organization
- Separate test stages
- Use build matrix
- Cache dependencies
- Parallelize tests

### 2. Result Management
- Archive artifacts
- Clean old results
- Monitor trends
- Track metrics

### 3. Security
- Secure secrets
- Limit permissions
- Scan dependencies
- Validate inputs

## Monitoring

### 1. Pipeline Metrics
```yaml
steps:
  - name: Collect metrics
    run: |
      python scripts/metrics_collector.py
      python scripts/test_analyzer.py
```

### 2. Notifications
```yaml
steps:
  - name: Send notifications
    if: always()
    run: |
      if [ ${{ job.status }} == 'success' ]; then
        echo "Tests passed"
      else
        echo "Tests failed"
      fi
```

## Troubleshooting

### Common Issues
1. **Pipeline Failures**
   ```bash
   # Check pipeline logs
   ./scripts/test_workflow_runner.py --show-logs
   ```

2. **Artifact Issues**
   ```bash
   # Validate artifacts
   ./scripts/test_workflow_runner.py --check-artifacts
   ```

3. **Environment Problems**
   ```bash
   # Verify environment
   ./scripts/test_workflow_runner.py --verify-env
   ```

### Getting Help
```bash
# Show CI/CD help
./scripts/test_workflow_runner.py --ci-help

# List available commands
./scripts/test_workflow_runner.py --list-ci-commands
```

## Integration

### 1. With Test Workflow
```yaml
steps:
  - name: Run workflow
    run: python scripts/test_workflow_runner.py
```

### 2. With Data Quality
```yaml
steps:
  - name: Check quality
    run: python scripts/data_quality_validator.py
```

### 3. With Monitoring
```yaml
steps:
  - name: Monitor execution
    run: python scripts/data_quality_monitor.py
```
