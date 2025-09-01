# Interactive Test Dashboard Guide

## Launching the Dashboard
```bash
# Generate and launch dashboard
./scripts/test_dashboard.py

# Generate with specific data
./scripts/test_dashboard.py --data custom_results.json

# Update in real-time
./scripts/test_dashboard.py --live
```

## Dashboard Features

### 1. Summary Metrics
- Average Response Time
- Success Rate
- Total Tests Run
- Peak Memory Usage

### 2. Interactive Plots

#### Response Time Distribution
- Hover for exact values
- Zoom in/out
- Pan across distribution
- Filter ranges
- Export as PNG

#### Performance Metrics
- Toggle CPU/Memory lines
- Time range selection
- Tooltip with details
- Customizable view

#### Triangle Types
- Interactive pie chart
- Click to isolate segments
- Percentage/count toggle
- Drill-down capability

#### Concurrent Users
- Dual Y-axis plot
- Response time vs users
- Success rate overlay
- Interactive legend

#### Results Heatmap
- Color-coded results
- Zoom functionality
- Value tooltips
- Custom color scales

## Customization
```yaml
# dashboard_config.yml
appearance:
  theme: light  # or dark
  colors:
    primary: '#2196F3'
    success: '#4CAF50'
    error: '#F44336'
  
plots:
  response_times:
    bins: 50
    color: blue
    
  performance:
    update_interval: 5  # seconds
    history: 1000      # points
    
  heatmap:
    colorscale: 'RdYlGn'
    cell_height: 30
```

## Real-time Monitoring
```bash
# Start live monitoring
./scripts/test_dashboard.py --live --interval 5

# Monitor specific metrics
./scripts/test_dashboard.py --live --metrics cpu,memory
```

## Data Export
- Export plots as PNG/SVG/PDF
- Download raw data as CSV/JSON
- Share dashboard URL
- Schedule reports

## Keyboard Shortcuts
```
[Space]    Play/pause live updates
[R]        Reset view
[S]        Save current view
[F]        Toggle full screen
[1-5]      Switch between plots
[Esc]      Exit full screen
```

## Best Practices
1. **Performance**
   - Limit data points for smooth interaction
   - Use appropriate update intervals
   - Clear old data periodically

2. **Visualization**
   - Choose appropriate plot types
   - Use consistent color schemes
   - Add clear labels and titles

3. **Monitoring**
   - Set meaningful thresholds
   - Configure alerts
   - Archive historical data

4. **Sharing**
   - Use shareable URLs
   - Export reports regularly
   - Document custom views
