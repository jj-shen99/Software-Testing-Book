#!/usr/bin/env python3

import os
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime

class TestDashboard:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.results_dir = os.path.join(self.base_dir, "sample_analysis_results")
        self.dashboard_dir = os.path.join(
            self.results_dir, 
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}", 
            "dashboard"
        )
        os.makedirs(self.dashboard_dir, exist_ok=True)

    def create_response_time_plot(self, data):
        """Create interactive response time plot"""
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=data['response_times'],
            name='Response Times',
            nbinsx=50,
            marker_color='blue'
        ))
        
        fig.update_layout(
            title='Response Time Distribution',
            xaxis_title='Response Time (ms)',
            yaxis_title='Count',
            showlegend=True
        )
        
        return fig

    def create_performance_plot(self, data):
        """Create interactive performance metrics plot"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('CPU Usage', 'Memory Usage')
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['timestamps'],
                y=data['cpu_usage'],
                name='CPU',
                line=dict(color='red')
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['timestamps'],
                y=data['memory_usage'],
                name='Memory',
                line=dict(color='green')
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=800,
            title='Performance Metrics',
            showlegend=True
        )
        
        return fig

    def create_triangle_types_plot(self, data):
        """Create interactive pie chart of triangle types"""
        fig = go.Figure(data=[go.Pie(
            labels=list(data['triangle_types'].keys()),
            values=list(data['triangle_types'].values())
        )])
        
        fig.update_layout(
            title='Triangle Types Distribution'
        )
        
        return fig

    def create_concurrent_users_plot(self, data):
        """Create interactive concurrent users plot"""
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=data['concurrent_users'],
                y=data['response_times'],
                name='Response Time',
                line=dict(color='blue')
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['concurrent_users'],
                y=data['success_rates'],
                name='Success Rate',
                line=dict(color='green')
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title='Performance Under Load',
            xaxis_title='Number of Concurrent Users'
        )
        
        fig.update_yaxes(
            title_text='Response Time (ms)', 
            secondary_y=False
        )
        fig.update_yaxes(
            title_text='Success Rate (%)', 
            secondary_y=True
        )
        
        return fig

    def create_results_heatmap(self, data):
        """Create interactive results heatmap"""
        fig = go.Figure(data=go.Heatmap(
            z=data['result_matrix'],
            colorscale='RdYlGn'
        ))
        
        fig.update_layout(
            title='Test Results Heatmap',
            xaxis_title='Test Cases',
            yaxis_title='Test Runs'
        )
        
        return fig

    def generate_dashboard(self, data):
        """Generate interactive HTML dashboard"""
        plots = {
            'response_times': self.create_response_time_plot(data),
            'performance': self.create_performance_plot(data),
            'triangle_types': self.create_triangle_types_plot(data),
            'concurrent_users': self.create_concurrent_users_plot(data),
            'results_heatmap': self.create_results_heatmap(data)
        }
        
        dashboard_path = os.path.join(self.dashboard_dir, 'dashboard.html')
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Results Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .dashboard-header {{
                    text-align: center;
                    padding: 20px;
                    background-color: #fff;
                    margin-bottom: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .plot-container {{
                    background-color: #fff;
                    padding: 20px;
                    margin-bottom: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .summary {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 20px;
                }}
                .metric-card {{
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    text-align: center;
                }}
                .metric-value {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #2196F3;
                }}
            </style>
        </head>
        <body>
            <div class="dashboard-header">
                <h1>Test Results Dashboard</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <div class="metric-card">
                    <h3>Average Response Time</h3>
                    <div class="metric-value">{data['avg_response_time']:.2f}ms</div>
                </div>
                <div class="metric-card">
                    <h3>Success Rate</h3>
                    <div class="metric-value">{data['success_rate']:.1f}%</div>
                </div>
                <div class="metric-card">
                    <h3>Total Tests</h3>
                    <div class="metric-value">{data['total_tests']}</div>
                </div>
                <div class="metric-card">
                    <h3>Peak Memory</h3>
                    <div class="metric-value">{data['peak_memory']}MB</div>
                </div>
            </div>
        """
        
        for name, plot in plots.items():
            html_content += f"""
            <div class="plot-container">
                <div id="{name}"></div>
            </div>
            <script>
                var plotData = {plot.to_json()};
                Plotly.newPlot('{name}', plotData.data, plotData.layout);
            </script>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        with open(dashboard_path, 'w') as f:
            f.write(html_content)
            
        print(f"Dashboard generated at {dashboard_path}")

def main():
    dashboard = TestDashboard()
    
    # Load test results
    results_file = os.path.join(dashboard.results_dir, 'test_data/performance_dataset.json')
    with open(results_file) as f:
        data = json.load(f)
    
    # Generate dashboard
    dashboard.generate_dashboard(data)

if __name__ == "__main__":
    main()
