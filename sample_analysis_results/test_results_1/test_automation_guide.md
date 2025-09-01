# Test Automation Guide

## Running Triangle Tests
```bash
# Run all tests
./scripts/run_triangle_tests.py

# Run with specific configuration
./scripts/run_triangle_tests.py --config custom_config.yml

# Run performance tests only
./scripts/run_triangle_tests.py --type performance
```

## Test Configuration
```yaml
# config.yml
test_settings:
  unit_tests:
    enabled: true
    parallel: true
    max_workers: 4
    
  performance_tests:
    enabled: true
    iterations: 1000000
    concurrent_users: 10
    
  reporting:
    format: json
    save_metrics: true
    generate_graphs: true
```

## Test Results Location
```
sample_analysis_results/
└── test_results_[DATE]/
    ├── unit/
    │   └── triangle_tests.md
    ├── performance/
    │   ├── performance_metrics.md
    │   ├── response_time_analysis.md
    │   └── triangle_performance_analysis.md
    └── triangle_test_report.md
```

## Adding New Test Cases
```python
def test_new_scenario(self):
    # Add test case to run_unit_tests()
    test_cases.append((
        side_a,    # First side
        side_b,    # Second side
        side_c,    # Third side
        expected   # Expected area
    ))
```

## Performance Test Configuration
```python
# Modify in run_performance_tests()
ITERATIONS = 1000000      # Number of iterations
MAX_WORKERS = 10         # Concurrent threads
TIMEOUT_MS = 1000       # Test timeout
```

## Report Generation
```python
# Custom report format
report = {
    'timestamp': datetime.now(),
    'test_suite': 'triangle_tests',
    'results': {
        'unit_tests': unit_results,
        'performance': perf_results
    }
}
```

## Monitoring Metrics
- Response time (ms)
- Throughput (req/sec)
- Error rate (%)
- Resource usage (CPU, Memory)

## Error Handling
```python
try:
    result = triangle_area(a, b, c)
    assert abs(result - expected) < 0.001
except AssertionError:
    log_error(f"Incorrect area for triangle ({a},{b},{c})")
except Exception as e:
    log_error(f"Test execution error: {str(e)}")
```

## Best Practices
1. Run tests in isolated environment
2. Use consistent test data
3. Monitor resource usage
4. Save all test artifacts
5. Document failures and fixes
