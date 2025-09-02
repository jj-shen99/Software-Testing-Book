# Test Results Visualization Guide

## Running Visualizations
```bash
# Generate all visualizations
./scripts/test_visualizer.py

# Generate specific plots
./scripts/test_visualizer.py --type response_times
./scripts/test_visualizer.py --type performance
```

## Available Visualizations

### 1. Response Time Distribution
```python
visualizer.plot_response_times(data)
```
- Histogram of response times
- Shows performance distribution
- Identifies outliers

### 2. Error Rate Trends
```python
visualizer.plot_error_rates(data)
```
- Error rates over time
- Trend analysis
- Failure patterns

### 3. Triangle Type Distribution
```python
visualizer.plot_triangle_types(data)
```
- Pie chart of triangle types
- Test case coverage
- Data distribution

### 4. Performance Metrics
```python
visualizer.plot_performance_metrics(data)
```
- CPU usage over time
- Memory consumption
- Resource utilization

### 5. Results Heatmap
```python
visualizer.create_heatmap(data)
```
- Test case success/failure
- Pattern identification
- Coverage analysis

### 6. Concurrent User Performance
```python
visualizer.plot_concurrent_users(data)
```
- Response time vs users
- Success rate vs load
- System scalability

## Output Formats
- PNG images in `/plots` directory
- HTML report with all visualizations
- Raw data in JSON format

## Customization
```python
# Custom plot settings
plt.figure(figsize=(12, 8))
plt.title('Custom Title')
plt.xlabel('X Label')
plt.ylabel('Y Label')

# Color schemes
sns.set_palette('husl')
plt.cm.viridis

# Output options
plt.savefig('custom_plot.png', dpi=300)
```

## Best Practices
1. **Data Preparation**
   - Clean data before plotting
   - Handle missing values
   - Normalize if needed

2. **Plot Clarity**
   - Clear labels and titles
   - Appropriate scales
   - Color-blind friendly

3. **Performance**
   - Close plot figures
   - Manage memory usage
   - Batch processing

4. **Report Generation**
   - Include all relevant plots
   - Add descriptions
   - Link to raw data
