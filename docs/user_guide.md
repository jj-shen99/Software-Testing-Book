# Test Automation Monitoring System - User Guide

## Installation

1. Clone the repository and install dependencies:
```bash
git clone <repository_url>
cd SoftwareTesting-1
pip3 install -r requirements.txt
```

2. Required Python packages:
- dash
- plotly
- pandas
- numpy
- prometheus_client

## Quick Start

1. Generate sample test data:
```bash
./scripts/generate_test_data.py
```

2. Start the dashboard:
```bash
./scripts/start_dashboard.py
```

3. Access the dashboard at http://localhost:8051

## Dashboard Features

### 1. Performance Metrics
- Response time trends
- Throughput monitoring
- Error rate tracking
- System resource usage (CPU, Memory)

### 2. Quality Metrics
- Code completeness
- Test consistency
- Data validity
- Real-time quality gauges

### 3. Test Results
- Pass/Fail distribution
- Test execution trends
- Success rate analysis
- Skip rate monitoring

### 4. Trend Analysis
- Historical performance data
- Quality metrics over time
- Test success rate trends
- Response time comparisons

## Using the Dashboard

### Time Range Selection
- Last Hour (1h): Most recent metrics
- Last Day (1d): 24-hour trends
- Last Week (1w): Weekly patterns

### Interacting with Graphs
- Hover over data points for details
- Click legend items to show/hide metrics
- Use zoom and pan controls for detailed views
- Export graph data as PNG or CSV

### Real-time Updates
- Dashboard auto-refreshes every 30 seconds
- Manual refresh available
- Historical data preserved

## Configuration

### Dashboard Settings
Edit `workflows/yaml_workflows/dashboard_config.yml` to customize:
- Refresh intervals
- Panel layouts
- Color schemes
- Default views

### Metrics Collection
Modify `scripts/metrics_collector.py` to adjust:
- Collection frequency
- Metric types
- Storage locations
- Data retention

## Troubleshooting

### Common Issues
1. Port already in use:
   ```bash
   lsof -i :8051 | grep LISTEN | awk '{print $2}' | xargs kill
   ```

2. Missing metrics data:
   - Check metrics directory exists
   - Verify test data generation
   - Ensure proper permissions

3. Dashboard not updating:
   - Check network connectivity
   - Verify metrics collection
   - Restart dashboard server

### Support
For additional support:
1. Check logs in `sample_analysis_results/test_results_*/metrics/metrics.log`
2. Review error messages in browser console
3. Contact system administrator
