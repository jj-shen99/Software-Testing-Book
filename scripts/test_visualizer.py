#!/usr/bin/env python3

import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime

class TestVisualizer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.results_dir = os.path.join(self.base_dir, "sample_analysis_results")
        self.plots_dir = os.path.join(self.results_dir, "test_results_" + 
                                    datetime.now().strftime("%Y_%m_%d"), "plots")
        os.makedirs(self.plots_dir, exist_ok=True)

    def plot_response_times(self, data):
        """Plot response time distribution"""
        plt.figure(figsize=(10, 6))
        sns.histplot(data=data['response_times'], bins=50)
        plt.title('Response Time Distribution')
        plt.xlabel('Response Time (ms)')
        plt.ylabel('Count')
        plt.savefig(os.path.join(self.plots_dir, 'response_times.png'))
        plt.close()

    def plot_error_rates(self, data):
        """Plot error rates over time"""
        plt.figure(figsize=(10, 6))
        error_rates = pd.Series(data['error_rates'])
        error_rates.plot()
        plt.title('Error Rate Over Time')
        plt.xlabel('Test Run')
        plt.ylabel('Error Rate (%)')
        plt.savefig(os.path.join(self.plots_dir, 'error_rates.png'))
        plt.close()

    def plot_triangle_types(self, data):
        """Plot distribution of triangle types"""
        plt.figure(figsize=(10, 6))
        types = data['triangle_types']
        plt.pie(types.values(), labels=types.keys(), autopct='%1.1f%%')
        plt.title('Distribution of Triangle Types')
        plt.savefig(os.path.join(self.plots_dir, 'triangle_types.png'))
        plt.close()

    def plot_performance_metrics(self, data):
        """Plot performance metrics"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
        
        # CPU Usage
        ax1.plot(data['timestamps'], data['cpu_usage'], label='CPU')
        ax1.set_title('CPU Usage Over Time')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('CPU Usage (%)')
        ax1.grid(True)
        
        # Memory Usage
        ax2.plot(data['timestamps'], data['memory_usage'], label='Memory', color='green')
        ax2.set_title('Memory Usage Over Time')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Memory Usage (MB)')
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, 'performance_metrics.png'))
        plt.close()

    def create_heatmap(self, data):
        """Create heatmap of test results"""
        plt.figure(figsize=(12, 8))
        sns.heatmap(data['result_matrix'], annot=True, cmap='YlOrRd')
        plt.title('Test Results Heatmap')
        plt.xlabel('Test Cases')
        plt.ylabel('Test Runs')
        plt.savefig(os.path.join(self.plots_dir, 'results_heatmap.png'))
        plt.close()

    def plot_concurrent_users(self, data):
        """Plot concurrent user performance"""
        plt.figure(figsize=(10, 6))
        
        users = data['concurrent_users']
        response_times = data['concurrent_response_times']
        success_rates = data['success_rates']
        
        fig, ax1 = plt.subplots()
        
        color = 'tab:blue'
        ax1.set_xlabel('Number of Concurrent Users')
        ax1.set_ylabel('Response Time (ms)', color=color)
        line1 = ax1.plot(users, response_times, color=color, label='Response Time')
        ax1.tick_params(axis='y', labelcolor=color)
        
        ax2 = ax1.twinx()
        color = 'tab:orange'
        ax2.set_ylabel('Success Rate (%)', color=color)
        line2 = ax2.plot(users, success_rates, color=color, label='Success Rate')
        ax2.tick_params(axis='y', labelcolor=color)
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left')
        
        plt.title('Performance Under Load')
        plt.savefig(os.path.join(self.plots_dir, 'concurrent_users.png'))
        plt.close()

    def generate_report(self, data):
        """Generate HTML report with all visualizations"""
        report_path = os.path.join(self.plots_dir, 'visualization_report.html')
        
        html_content = f"""
        <html>
        <head>
            <title>Test Results Visualization</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .plot {{ margin: 20px 0; text-align: center; }}
                img {{ max-width: 100%; }}
            </style>
        </head>
        <body>
            <h1>Test Results Visualization</h1>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="plot">
                <h2>Response Time Distribution</h2>
                <img src="response_times.png" alt="Response Times">
            </div>
            
            <div class="plot">
                <h2>Error Rates</h2>
                <img src="error_rates.png" alt="Error Rates">
            </div>
            
            <div class="plot">
                <h2>Triangle Types Distribution</h2>
                <img src="triangle_types.png" alt="Triangle Types">
            </div>
            
            <div class="plot">
                <h2>Performance Metrics</h2>
                <img src="performance_metrics.png" alt="Performance Metrics">
            </div>
            
            <div class="plot">
                <h2>Results Heatmap</h2>
                <img src="results_heatmap.png" alt="Results Heatmap">
            </div>
            
            <div class="plot">
                <h2>Concurrent User Performance</h2>
                <img src="concurrent_users.png" alt="Concurrent Users">
            </div>
        </body>
        </html>
        """
        
        with open(report_path, 'w') as f:
            f.write(html_content)

def main():
    visualizer = TestVisualizer()
    
    # Load test results
    results_file = os.path.join(visualizer.results_dir, 'test_data/performance_dataset.json')
    with open(results_file) as f:
        data = json.load(f)
    
    # Generate all visualizations
    visualizer.plot_response_times(data)
    visualizer.plot_error_rates(data)
    visualizer.plot_triangle_types(data)
    visualizer.plot_performance_metrics(data)
    visualizer.create_heatmap(data)
    visualizer.plot_concurrent_users(data)
    
    # Generate HTML report
    visualizer.generate_report(data)
    print(f"Visualization report generated in {visualizer.plots_dir}")

if __name__ == "__main__":
    main()
