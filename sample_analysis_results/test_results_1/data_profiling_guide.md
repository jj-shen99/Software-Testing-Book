# Test Data Profiling Guide

## Quick Start
```bash
# Profile all datasets
./scripts/test_data_profiler.py

# Profile specific dataset
./scripts/test_data_profiler.py --file large_dataset.json

# Generate summary report
./scripts/test_data_profiler.py --summary
```

## Profile Components

### 1. Statistical Analysis
```python
# Basic statistics
stats = profiler.analyze_distributions(df)
print(stats['size_stats'])
print(stats['area_stats'])
```

### 2. Distribution Analysis
```python
# Generate distribution plots
plots = profiler.plot_distributions(df)
```

### 3. Data Quality Metrics
```python
# Quality metrics
metrics = {
    'completeness': df.notna().mean(),
    'uniqueness': 1 - df.duplicated().mean(),
    'validity': df['is_valid'].mean()
}
```

## Available Reports

### 1. HTML Profile
- Comprehensive data overview
- Variable distributions
- Correlation analysis
- Missing value patterns

### 2. Distribution Plots
- Triangle types distribution
- Side lengths distribution
- Area distribution
- Side ratios distribution

### 3. Analysis Report
- Dataset overview
- Statistical summaries
- Quality metrics
- Validation results

## Customization

### Profile Configuration
```yaml
# profile_config.yml
reports:
  html:
    enabled: true
    minimal: false
    
  plots:
    enabled: true
    style: seaborn
    dpi: 300
    
  analysis:
    enabled: true
    format: markdown
```

### Custom Metrics
```python
# Add custom metrics
def custom_metric(df):
    return {
        'metric_name': calculation,
        'threshold': value
    }
```

## Best Practices

### 1. Data Loading
- Validate file format
- Handle missing values
- Convert data types
- Document assumptions

### 2. Analysis
- Set appropriate bins
- Use consistent scales
- Handle outliers
- Document anomalies

### 3. Reporting
- Include timestamps
- Save raw data
- Version reports
- Archive results

## Troubleshooting

### Common Issues
1. **Memory Usage**
   ```bash
   # Reduce memory usage
   ./scripts/test_data_profiler.py --sample 1000
   ```

2. **Long Processing**
   ```bash
   # Profile subset of features
   ./scripts/test_data_profiler.py --features size,type
   ```

3. **Missing Data**
   ```bash
   # Check data completeness
   ./scripts/test_data_profiler.py --check-data
   ```

### Getting Help
```bash
# Show profiler help
./scripts/test_data_profiler.py --help

# List available metrics
./scripts/test_data_profiler.py --list-metrics
```

## Integration

### 1. With Data Validation
```python
# Combine validation and profiling
from test_data_validator import DataQualityValidator
validator = DataQualityValidator()
validation = validator.validate_dataset(data)
profile = profiler.profile_dataset(data)
```

### 2. With Monitoring
```python
# Monitor data quality
from data_quality_monitor import DataQualityMonitor
monitor = DataQualityMonitor()
monitor.add_profile_metrics(profile)
```

### 3. With Dashboard
```python
# Add profile to dashboard
from data_quality_dashboard import DataQualityDashboard
dashboard = DataQualityDashboard()
dashboard.add_profile_view(profile)
```
