#!/usr/bin/env python3

import os
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

class DataQualityDashboard:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "monitoring"
        )
        self.app = dash.Dash(__name__)
        self.setup_layout()
        
    def load_metrics(self):
        """Load monitoring metrics"""
        metrics = {
            'timestamps': [],
            'completeness': [],
            'consistency': [],
            'validity': [],
            'errors': [],
            'warnings': []
        }
        
        for file in os.listdir(self.data_dir):
            if file.startswith('validation_') and file.endswith('.json'):
                with open(os.path.join(self.data_dir, file)) as f:
                    data = json.load(f)
                    metrics['timestamps'].append(data['timestamp'])
                    metrics['completeness'].append(data['metrics']['completeness_score'])
                    metrics['consistency'].append(data['metrics']['consistency_score'])
                    metrics['validity'].append(data['metrics']['validity_score'])
                    metrics['errors'].append(len(data['errors']))
                    metrics['warnings'].append(len(data['warnings']))
                    
        return pd.DataFrame(metrics)
        
    def setup_layout(self):
        """Setup dashboard layout"""
        self.app.layout = html.Div([
            html.H1('Data Quality Dashboard'),
            
            html.Div([
                html.Div([
                    html.H3('Quality Scores'),
                    dcc.Graph(id='quality-scores')
                ], className='six columns'),
                
                html.Div([
                    html.H3('Issues Over Time'),
                    dcc.Graph(id='issues-trend')
                ], className='six columns')
            ], className='row'),
            
            html.Div([
                html.H3('Data Quality Metrics'),
                dcc.Graph(id='quality-metrics')
            ]),
            
            dcc.Interval(
                id='interval-component',
                interval=30*1000,  # 30 seconds
                n_intervals=0
            )
        ])
        
        self.setup_callbacks()
        
    def setup_callbacks(self):
        """Setup dashboard callbacks"""
        @self.app.callback(
            [Output('quality-scores', 'figure'),
             Output('issues-trend', 'figure'),
             Output('quality-metrics', 'figure')],
            [Input('interval-component', 'n_intervals')]
        )
        def update_graphs(n):
            df = self.load_metrics()
            
            # Quality scores plot
            quality_fig = go.Figure()
            for metric in ['completeness', 'consistency', 'validity']:
                quality_fig.add_trace(go.Scatter(
                    x=df['timestamps'],
                    y=df[metric],
                    name=metric.capitalize(),
                    mode='lines+markers'
                ))
            quality_fig.update_layout(
                title='Quality Scores Over Time',
                yaxis_title='Score',
                yaxis_range=[0, 1]
            )
            
            # Issues trend plot
            issues_fig = go.Figure()
            issues_fig.add_trace(go.Bar(
                x=df['timestamps'],
                y=df['errors'],
                name='Errors',
                marker_color='red'
            ))
            issues_fig.add_trace(go.Bar(
                x=df['timestamps'],
                y=df['warnings'],
                name='Warnings',
                marker_color='orange'
            ))
            issues_fig.update_layout(
                title='Issues Over Time',
                yaxis_title='Count',
                barmode='stack'
            )
            
            # Quality metrics plot
            metrics_fig = go.Figure()
            metrics_fig.add_trace(go.Indicator(
                mode='gauge+number',
                value=df['completeness'].iloc[-1] if not df.empty else 0,
                title={'text': 'Completeness'},
                domain={'row': 0, 'column': 0},
                gauge={'axis': {'range': [0, 1]}}
            ))
            metrics_fig.add_trace(go.Indicator(
                mode='gauge+number',
                value=df['consistency'].iloc[-1] if not df.empty else 0,
                title={'text': 'Consistency'},
                domain={'row': 0, 'column': 1},
                gauge={'axis': {'range': [0, 1]}}
            ))
            metrics_fig.add_trace(go.Indicator(
                mode='gauge+number',
                value=df['validity'].iloc[-1] if not df.empty else 0,
                title={'text': 'Validity'},
                domain={'row': 0, 'column': 2},
                gauge={'axis': {'range': [0, 1]}}
            ))
            metrics_fig.update_layout(
                grid={'rows': 1, 'columns': 3},
                height=300
            )
            
            return quality_fig, issues_fig, metrics_fig
            
    def run(self, host='localhost', port=8050):
        """Run dashboard"""
        self.app.run_server(host=host, port=port, debug=True)

def main():
    dashboard = DataQualityDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
