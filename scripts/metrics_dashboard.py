#!/usr/bin/env python3

import os
import json
import yaml
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List

class MetricsDashboard:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.layout_file = os.path.join(self.base_dir, "scripts/dashboard_layout.yml")
        self.metrics_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "metrics"
        )
        self.load_layout()
        self.app = dash.Dash(__name__)
        self.setup_layout()

    def load_layout(self):
        """Load dashboard layout configuration"""
        with open(self.layout_file, 'r') as f:
            self.layout_config = yaml.safe_load(f)

    def load_metrics(self, days: int = 7) -> Dict[str, pd.DataFrame]:
        """Load metrics data"""
        metrics = {
            'performance': [],
            'test': [],
            'quality': []
        }
        
        start_date = datetime.now() - timedelta(days=days)
        
        for root, _, files in os.walk(self.metrics_dir):
            for file in files:
                if file.startswith('ci_metrics_') and file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    file_date = datetime.strptime(
                        file[11:19],
                        '%Y%m%d'
                    )
                    
                    if file_date >= start_date:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            for category in metrics:
                                if category in data:
                                    metrics[category].append(data[category])
                                    
        return {
            category: pd.DataFrame(data)
            for category, data in metrics.items()
        }

    def setup_layout(self):
        """Setup dashboard layout"""
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1('Test Metrics Dashboard'),
                html.P(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"),
                dcc.Interval(
                    id='interval-component',
                    interval=self.layout_config['layout']['refresh_interval'] * 1000,
                    n_intervals=0
                )
            ], className='header'),
            
            # Filters
            html.Div([
                html.Label('Time Range:'),
                dcc.Dropdown(
                    id='time-range',
                    options=[
                        {'label': 'Last 24 Hours', 'value': '1'},
                        {'label': 'Last 7 Days', 'value': '7'},
                        {'label': 'Last 30 Days', 'value': '30'}
                    ],
                    value='7'
                )
            ], className='filters'),
            
            # Performance Metrics
            html.Div([
                html.H2('Performance Metrics'),
                html.Div([
                    dcc.Graph(id='response-time-graph'),
                    dcc.Graph(id='cpu-usage-gauge'),
                    dcc.Graph(id='memory-usage-gauge')
                ], className='metrics-row')
            ], className='section'),
            
            # Test Metrics
            html.Div([
                html.H2('Test Metrics'),
                html.Div([
                    dcc.Graph(id='test-results-pie'),
                    dcc.Graph(id='test-duration-graph')
                ], className='metrics-row')
            ], className='section'),
            
            # Quality Metrics
            html.Div([
                html.H2('Quality Metrics'),
                html.Div([
                    dcc.Graph(id='quality-score-stat'),
                    dcc.Graph(id='coverage-gauge'),
                    dcc.Graph(id='error-rate-graph')
                ], className='metrics-row')
            ], className='section')
        ])
        
        self.setup_callbacks()

    def setup_callbacks(self):
        """Setup dashboard callbacks"""
        @self.app.callback(
            [Output('response-time-graph', 'figure'),
             Output('cpu-usage-gauge', 'figure'),
             Output('memory-usage-gauge', 'figure'),
             Output('test-results-pie', 'figure'),
             Output('test-duration-graph', 'figure'),
             Output('quality-score-stat', 'figure'),
             Output('coverage-gauge', 'figure'),
             Output('error-rate-graph', 'figure')],
            [Input('interval-component', 'n_intervals'),
             Input('time-range', 'value')]
        )
        def update_graphs(n, time_range):
            metrics = self.load_metrics(int(time_range))
            
            return (
                self.create_response_time_graph(metrics['performance']),
                self.create_cpu_gauge(metrics['performance']),
                self.create_memory_gauge(metrics['performance']),
                self.create_test_results_pie(metrics['test']),
                self.create_test_duration_graph(metrics['test']),
                self.create_quality_score_stat(metrics['quality']),
                self.create_coverage_gauge(metrics['quality']),
                self.create_error_rate_graph(metrics['performance'])
            )

    def create_response_time_graph(self, df: pd.DataFrame) -> go.Figure:
        """Create response time graph"""
        return go.Figure(
            data=[
                go.Scatter(
                    x=df['timestamp'],
                    y=df['avg_response_time'],
                    name='Average',
                    line=dict(color=self.layout_config['visualization']['colors']['primary'])
                ),
                go.Scatter(
                    x=df['timestamp'],
                    y=df['p95_response_time'],
                    name='95th Percentile',
                    line=dict(color=self.layout_config['visualization']['colors']['secondary'])
                )
            ],
            layout=go.Layout(
                title='Response Time',
                xaxis_title='Time',
                yaxis_title='Response Time (ms)'
            )
        )

    def create_cpu_gauge(self, df: pd.DataFrame) -> go.Figure:
        """Create CPU usage gauge"""
        return go.Figure(
            data=[go.Indicator(
                mode="gauge+number",
                value=df['cpu_percent'].iloc[-1],
                title={'text': "CPU Usage"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': self.layout_config['visualization']['colors']['primary']},
                    'steps': [
                        {'range': [0, 70], 'color': "lightgray"},
                        {'range': [70, 85], 'color': "orange"},
                        {'range': [85, 100], 'color': "red"}
                    ]
                }
            )]
        )

    def create_memory_gauge(self, df: pd.DataFrame) -> go.Figure:
        """Create memory usage gauge"""
        return go.Figure(
            data=[go.Indicator(
                mode="gauge+number",
                value=df['memory_percent'].iloc[-1],
                title={'text': "Memory Usage"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': self.layout_config['visualization']['colors']['primary']},
                    'steps': [
                        {'range': [0, 75], 'color': "lightgray"},
                        {'range': [75, 90], 'color': "orange"},
                        {'range': [90, 100], 'color': "red"}
                    ]
                }
            )]
        )

    def create_test_results_pie(self, df: pd.DataFrame) -> go.Figure:
        """Create test results pie chart"""
        results = df['status'].value_counts()
        return go.Figure(
            data=[go.Pie(
                labels=results.index,
                values=results.values,
                marker=dict(
                    colors=[
                        self.layout_config['visualization']['colors']['success'],
                        self.layout_config['visualization']['colors']['error'],
                        self.layout_config['visualization']['colors']['warning']
                    ]
                )
            )],
            layout=go.Layout(
                title='Test Results'
            )
        )

    def create_test_duration_graph(self, df: pd.DataFrame) -> go.Figure:
        """Create test duration graph"""
        return go.Figure(
            data=[
                go.Scatter(
                    x=df['timestamp'],
                    y=df['avg_duration'],
                    name='Average Duration',
                    line=dict(color=self.layout_config['visualization']['colors']['primary'])
                )
            ],
            layout=go.Layout(
                title='Test Duration',
                xaxis_title='Time',
                yaxis_title='Duration (s)'
            )
        )

    def create_quality_score_stat(self, df: pd.DataFrame) -> go.Figure:
        """Create quality score statistic"""
        return go.Figure(
            data=[go.Indicator(
                mode="number+delta",
                value=df['quality_score'].iloc[-1],
                delta={'reference': df['quality_score'].iloc[-2]},
                title={'text': "Quality Score"}
            )]
        )

    def create_coverage_gauge(self, df: pd.DataFrame) -> go.Figure:
        """Create coverage gauge"""
        return go.Figure(
            data=[go.Indicator(
                mode="gauge+number",
                value=df['coverage_percent'].iloc[-1],
                title={'text': "Code Coverage"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': self.layout_config['visualization']['colors']['primary']},
                    'steps': [
                        {'range': [0, 70], 'color': "red"},
                        {'range': [70, 80], 'color': "orange"},
                        {'range': [80, 100], 'color': "lightgray"}
                    ]
                }
            )]
        )

    def create_error_rate_graph(self, df: pd.DataFrame) -> go.Figure:
        """Create error rate graph"""
        return go.Figure(
            data=[
                go.Scatter(
                    x=df['timestamp'],
                    y=df['error_rate'],
                    name='Error Rate',
                    line=dict(color=self.layout_config['visualization']['colors']['error'])
                )
            ],
            layout=go.Layout(
                title='Error Rate',
                xaxis_title='Time',
                yaxis_title='Error Rate (%)'
            )
        )

    def run(self, host: str = 'localhost', port: int = 8050):
        """Run dashboard"""
        self.app.run_server(host=host, port=port, debug=True)

def main():
    dashboard = MetricsDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
