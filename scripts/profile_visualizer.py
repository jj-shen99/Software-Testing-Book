#!/usr/bin/env python3

import os
import json
import yaml
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
from typing import Dict, Any, List

class ProfileVisualizer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(self.base_dir, "scripts/profiling_config.yml")
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

    def create_distribution_plots(self, df: pd.DataFrame) -> go.Figure:
        """Create distribution plots for numeric columns"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Side Lengths Distribution',
                'Area Distribution',
                'Side Ratios',
                'Triangle Types'
            )
        )

        # Side lengths distribution
        for col in ['side_a', 'side_b', 'side_c']:
            fig.add_trace(
                go.Histogram(
                    x=df[col],
                    name=col,
                    opacity=0.7,
                    nbinsx=30
                ),
                row=1, col=1
            )

        # Area distribution
        fig.add_trace(
            go.Histogram(
                x=df['area'],
                name='Area',
                opacity=0.7,
                nbinsx=30,
                marker_color=self.config['colors']['qualitative'][1]
            ),
            row=1, col=2
        )

        # Side ratios
        fig.add_trace(
            go.Box(
                y=df['side_ratio'],
                name='Side Ratio',
                marker_color=self.config['colors']['qualitative'][2]
            ),
            row=2, col=1
        )

        # Triangle types
        type_counts = df['type'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=type_counts.index,
                values=type_counts.values,
                marker_colors=self.config['colors']['qualitative']
            ),
            row=2, col=2
        )

        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Triangle Data Distributions"
        )

        return fig

    def create_correlation_plot(self, df: pd.DataFrame) -> go.Figure:
        """Create correlation matrix plot"""
        numeric_cols = ['side_a', 'side_b', 'side_c', 'area', 'side_ratio']
        corr_matrix = df[numeric_cols].corr()

        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=numeric_cols,
            y=numeric_cols,
            colorscale=self.config['colors']['diverging'],
            zmin=-1,
            zmax=1
        ))

        fig.update_layout(
            title='Feature Correlations',
            height=600,
            width=800
        )

        return fig

    def create_quality_metrics_plot(self, metrics: Dict[str, float]) -> go.Figure:
        """Create quality metrics visualization"""
        fig = go.Figure()

        for metric, value in metrics.items():
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=value * 100,
                title={'text': metric.capitalize()},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': self.config['colors']['qualitative'][0]},
                    'steps': [
                        {'range': [0, 60], 'color': "#EF5350"},
                        {'range': [60, 80], 'color': "#FFEE58"},
                        {'range': [80, 100], 'color': "#66BB6A"}
                    ]
                }
            ))

        fig.update_layout(
            grid={'rows': 1, 'columns': len(metrics)},
            title='Data Quality Metrics'
        )

        return fig

    def create_time_series_plot(self, history: List[Dict[str, Any]]) -> go.Figure:
        """Create time series plot of profile metrics"""
        df = pd.DataFrame(history)
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Quality Metrics Over Time', 'Distribution Metrics Over Time')
        )

        # Quality metrics
        for metric in ['completeness', 'validity', 'consistency']:
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df[metric],
                    name=metric.capitalize(),
                    mode='lines+markers'
                ),
                row=1, col=1
            )

        # Distribution metrics
        for metric in ['mean_area', 'mean_ratio']:
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df[metric],
                    name=metric.replace('_', ' ').title(),
                    mode='lines+markers'
                ),
                row=2, col=1
            )

        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Profile Metrics Over Time"
        )

        return fig

    def create_interactive_dashboard(self, df: pd.DataFrame, metrics: Dict[str, float],
                                  history: List[Dict[str, Any]]) -> str:
        """Create interactive HTML dashboard"""
        # Create all plots
        dist_fig = self.create_distribution_plots(df)
        corr_fig = self.create_correlation_plot(df)
        quality_fig = self.create_quality_metrics_plot(metrics)
        time_fig = self.create_time_series_plot(history)

        # Generate HTML
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        dashboard_path = os.path.join(self.viz_dir, f'profile_dashboard_{timestamp}.html')

        with open(dashboard_path, 'w') as f:
            f.write(f"""
            <html>
            <head>
                <title>Data Profile Dashboard</title>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        background-color: #f5f5f5;
                    }}
                    .dashboard-container {{
                        max-width: 1200px;
                        margin: 0 auto;
                    }}
                    .plot-container {{
                        background-color: white;
                        padding: 20px;
                        margin-bottom: 20px;
                        border-radius: 5px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }}
                </style>
            </head>
            <body>
                <div class="dashboard-container">
                    <h1>Data Profile Dashboard</h1>
                    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    
                    <div class="plot-container">
                        <div id="distributions"></div>
                    </div>
                    
                    <div class="plot-container">
                        <div id="correlations"></div>
                    </div>
                    
                    <div class="plot-container">
                        <div id="quality"></div>
                    </div>
                    
                    <div class="plot-container">
                        <div id="history"></div>
                    </div>
                </div>
                
                <script>
                    var distributions = {dist_fig.to_json()};
                    var correlations = {corr_fig.to_json()};
                    var quality = {quality_fig.to_json()};
                    var history = {time_fig.to_json()};
                    
                    Plotly.newPlot('distributions', distributions.data, distributions.layout);
                    Plotly.newPlot('correlations', correlations.data, correlations.layout);
                    Plotly.newPlot('quality', quality.data, quality.layout);
                    Plotly.newPlot('history', history.data, history.layout);
                </script>
            </body>
            </html>
            """)

        return dashboard_path

    def save_plot(self, fig: go.Figure, name: str) -> str:
        """Save plot to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plot_path = os.path.join(self.viz_dir, f'{name}_{timestamp}.html')
        fig.write_html(plot_path)
        return plot_path

def main():
    visualizer = ProfileVisualizer()
    
    # Example usage with sample data
    df = pd.DataFrame({
        'side_a': [3, 4, 5, 5, 5],
        'side_b': [4, 5, 5, 5, 5],
        'side_c': [5, 6, 5, 5, 5],
        'area': [6.0, 9.0, 10.825, 10.825, 10.825],
        'side_ratio': [1.67, 1.5, 1.0, 1.0, 1.0],
        'type': ['right', 'isosceles', 'equilateral', 'equilateral', 'equilateral']
    })
    
    metrics = {
        'completeness': 1.0,
        'validity': 0.95,
        'consistency': 0.98
    }
    
    history = [
        {
            'timestamp': '2025-09-01T12:00:00',
            'completeness': 1.0,
            'validity': 0.95,
            'consistency': 0.98,
            'mean_area': 9.5,
            'mean_ratio': 1.23
        }
    ]
    
    dashboard_path = visualizer.create_interactive_dashboard(df, metrics, history)
    print(f"Dashboard generated at: {dashboard_path}")

if __name__ == "__main__":
    main()
