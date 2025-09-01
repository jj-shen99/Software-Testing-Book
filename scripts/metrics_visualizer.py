#!/usr/bin/env python3

import os
import json
import yaml
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Dict, Any, List

class MetricsVisualizer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(
            self.base_dir,
            "workflows/yaml_workflows/monitoring_config.yml"
        )
        self.viz_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "visualizations"
        )
        os.makedirs(self.viz_dir, exist_ok=True)
        self.load_config()

    def load_config(self):
        """Load visualization configuration"""
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f)['visualization']

    def load_metrics(self, days: int = 7) -> pd.DataFrame:
        """Load metrics from files"""
        metrics = []
        start_date = datetime.now() - timedelta(days=days)
        
        for root, _, files in os.walk(self.base_dir):
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
                            metrics.append(data)
                            
        return pd.DataFrame(metrics)

    def create_performance_dashboard(self, df: pd.DataFrame) -> go.Figure:
        """Create performance metrics dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Response Time Distribution',
                'CPU Usage Over Time',
                'Memory Usage Over Time',
                'Error Rate Trend'
            )
        )

        # Response time distribution
        fig.add_trace(
            go.Histogram(
                x=df['response_time'],
                name='Response Time',
                nbinsx=30,
                marker_color=self.config['colors']['primary']
            ),
            row=1, col=1
        )

        # CPU usage
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['cpu_usage'],
                name='CPU Usage',
                mode='lines+markers',
                marker_color=self.config['colors']['secondary']
            ),
            row=1, col=2
        )

        # Memory usage
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['memory_usage'],
                name='Memory Usage',
                mode='lines+markers',
                marker_color=self.config['colors']['tertiary']
            ),
            row=2, col=1
        )

        # Error rate
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['error_rate'],
                name='Error Rate',
                mode='lines+markers',
                marker_color=self.config['colors']['error']
            ),
            row=2, col=2
        )

        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Performance Metrics Dashboard"
        )

        return fig

    def create_test_metrics_dashboard(self, df: pd.DataFrame) -> go.Figure:
        """Create test metrics dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Test Results Distribution',
                'Test Duration Trend',
                'Coverage Trend',
                'Test Types Distribution'
            )
        )

        # Test results distribution
        results = df['test_status'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=results.index,
                values=results.values,
                name='Test Results',
                marker_colors=[
                    self.config['colors']['success'],
                    self.config['colors']['error'],
                    self.config['colors']['warning']
                ]
            ),
            row=1, col=1
        )

        # Test duration trend
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['test_duration'],
                name='Duration',
                mode='lines+markers',
                marker_color=self.config['colors']['primary']
            ),
            row=1, col=2
        )

        # Coverage trend
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['coverage'],
                name='Coverage',
                mode='lines+markers',
                marker_color=self.config['colors']['secondary']
            ),
            row=2, col=1
        )

        # Test types distribution
        types = df['test_type'].value_counts()
        fig.add_trace(
            go.Bar(
                x=types.index,
                y=types.values,
                name='Test Types',
                marker_color=self.config['colors']['tertiary']
            ),
            row=2, col=2
        )

        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Test Metrics Dashboard"
        )

        return fig

    def create_quality_metrics_dashboard(self, df: pd.DataFrame) -> go.Figure:
        """Create quality metrics dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Quality Score Trend',
                'Issue Distribution',
                'Resolution Time Trend',
                'Quality Metrics Comparison'
            )
        )

        # Quality score trend
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['quality_score'],
                name='Quality Score',
                mode='lines+markers',
                marker_color=self.config['colors']['primary']
            ),
            row=1, col=1
        )

        # Issue distribution
        issues = df['issue_type'].value_counts()
        fig.add_trace(
            go.Bar(
                x=issues.index,
                y=issues.values,
                name='Issues',
                marker_color=self.config['colors']['error']
            ),
            row=1, col=2
        )

        # Resolution time trend
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['resolution_time'],
                name='Resolution Time',
                mode='lines+markers',
                marker_color=self.config['colors']['secondary']
            ),
            row=2, col=1
        )

        # Quality metrics comparison
        metrics = ['completeness', 'consistency', 'validity']
        for metric in metrics:
            fig.add_trace(
                go.Box(
                    y=df[metric],
                    name=metric.capitalize(),
                    boxpoints='outliers'
                ),
                row=2, col=2
            )

        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Quality Metrics Dashboard"
        )

        return fig

    def save_dashboard(self, fig: go.Figure, name: str) -> str:
        """Save dashboard to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(self.viz_dir, f'{name}_{timestamp}.html')
        
        fig.write_html(file_path)
        return file_path

    def create_metrics_report(self, df: pd.DataFrame) -> str:
        """Create comprehensive metrics report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(self.viz_dir, f'metrics_report_{timestamp}.md')
        
        with open(report_path, 'w') as f:
            f.write("# Metrics Analysis Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Performance Metrics\n")
            f.write(f"- Average Response Time: {df['response_time'].mean():.2f}ms\n")
            f.write(f"- 95th Percentile: {df['response_time'].quantile(0.95):.2f}ms\n")
            f.write(f"- Average CPU Usage: {df['cpu_usage'].mean():.2f}%\n")
            f.write(f"- Average Memory Usage: {df['memory_usage'].mean():.2f}MB\n")
            f.write(f"- Error Rate: {df['error_rate'].mean():.2f}%\n\n")
            
            f.write("## Test Metrics\n")
            f.write(f"- Total Tests: {len(df)}\n")
            f.write(f"- Pass Rate: {(df['test_status'] == 'pass').mean():.2%}\n")
            f.write(f"- Average Duration: {df['test_duration'].mean():.2f}s\n")
            f.write(f"- Coverage: {df['coverage'].mean():.2f}%\n\n")
            
            f.write("## Quality Metrics\n")
            f.write(f"- Quality Score: {df['quality_score'].mean():.2f}\n")
            f.write(f"- Completeness: {df['completeness'].mean():.2f}\n")
            f.write(f"- Consistency: {df['consistency'].mean():.2f}\n")
            f.write(f"- Validity: {df['validity'].mean():.2f}\n")
            
        return report_path

def main():
    visualizer = MetricsVisualizer()
    
    # Load metrics
    df = visualizer.load_metrics()
    
    # Create dashboards
    perf_dashboard = visualizer.create_performance_dashboard(df)
    test_dashboard = visualizer.create_test_metrics_dashboard(df)
    quality_dashboard = visualizer.create_quality_metrics_dashboard(df)
    
    # Save dashboards
    visualizer.save_dashboard(perf_dashboard, 'performance')
    visualizer.save_dashboard(test_dashboard, 'test_metrics')
    visualizer.save_dashboard(quality_dashboard, 'quality_metrics')
    
    # Generate report
    report_path = visualizer.create_metrics_report(df)
    print(f"Metrics report generated: {report_path}")

if __name__ == "__main__":
    main()
