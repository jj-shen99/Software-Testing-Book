#!/usr/bin/env python3

import os
import json
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class TestAnalyzer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.results_dir = os.path.join(self.base_dir, "sample_analysis_results")

    def analyze_results(self, test_name):
        """Analyze test results and generate metrics"""
        results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'execution_time': [],
            'error_types': {}
        }
        
        # Find latest results directory
        latest_dir = self._get_latest_results_dir()
        if not latest_dir:
            return None
            
        result_file = os.path.join(latest_dir, f"{test_name}_results.txt")
        if not os.path.exists(result_file):
            return None
            
        with open(result_file, 'r') as f:
            for line in f:
                if 'PASSED' in line:
                    results['passed'] += 1
                elif 'FAILED' in line:
                    results['failed'] += 1
                    error_type = self._extract_error_type(line)
                    results['error_types'][error_type] = results['error_types'].get(error_type, 0) + 1
                    
                if 'Time:' in line:
                    time = self._extract_time(line)
                    if time:
                        results['execution_time'].append(time)
                        
        results['total_tests'] = results['passed'] + results['failed']
        return results

    def generate_report(self, test_name):
        """Generate comprehensive test report"""
        results = self.analyze_results(test_name)
        if not results:
            print(f"No results found for {test_name}")
            return
            
        report_dir = os.path.join(self.results_dir, 
                                datetime.now().strftime("%Y_%m_%d"),
                                "reports")
        os.makedirs(report_dir, exist_ok=True)
        
        # Generate report file
        report_file = os.path.join(report_dir, f"{test_name}_report.md")
        with open(report_file, 'w') as f:
            f.write(f"# Test Analysis Report: {test_name}\n\n")
            f.write(f"## Summary\n")
            f.write(f"- Total Tests: {results['total_tests']}\n")
            f.write(f"- Passed: {results['passed']}\n")
            f.write(f"- Failed: {results['failed']}\n")
            
            if results['execution_time']:
                avg_time = sum(results['execution_time']) / len(results['execution_time'])
                f.write(f"\n## Performance\n")
                f.write(f"- Average Execution Time: {avg_time:.2f}s\n")
                
            if results['error_types']:
                f.write(f"\n## Error Analysis\n")
                for error_type, count in results['error_types'].items():
                    f.write(f"- {error_type}: {count}\n")
                    
        # Generate visualizations
        self._generate_visualizations(results, report_dir, test_name)
        
        return report_file

    def _get_latest_results_dir(self):
        """Get most recent results directory"""
        dirs = [d for d in os.listdir(self.results_dir) 
               if os.path.isdir(os.path.join(self.results_dir, d))
               and d.startswith("test_results_")]
        return os.path.join(self.results_dir, max(dirs)) if dirs else None

    def _extract_error_type(self, line):
        """Extract error type from failure message"""
        if 'AssertionError' in line:
            return 'Assertion Error'
        elif 'NullPointerException' in line:
            return 'Null Pointer'
        elif 'TimeoutException' in line:
            return 'Timeout'
        return 'Other'

    def _extract_time(self, line):
        """Extract execution time from result line"""
        try:
            return float(line.split('Time:')[1].strip().split()[0])
        except:
            return None

    def _generate_visualizations(self, results, report_dir, test_name):
        """Generate visualization plots"""
        # Test results pie chart
        plt.figure(figsize=(8, 8))
        plt.pie([results['passed'], results['failed']], 
                labels=['Passed', 'Failed'],
                colors=['green', 'red'],
                autopct='%1.1f%%')
        plt.title('Test Results Distribution')
        plt.savefig(os.path.join(report_dir, f"{test_name}_results_pie.png"))
        plt.close()
        
        # Execution time histogram
        if results['execution_time']:
            plt.figure(figsize=(10, 6))
            plt.hist(results['execution_time'], bins=20)
            plt.title('Test Execution Time Distribution')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency')
            plt.savefig(os.path.join(report_dir, f"{test_name}_time_hist.png"))
            plt.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_analyzer.py <test_name>")
        sys.exit(1)
        
    analyzer = TestAnalyzer()
    report_file = analyzer.generate_report(sys.argv[1])
    
    if report_file:
        print(f"Report generated: {report_file}")
    else:
        print("Failed to generate report")
        sys.exit(1)

if __name__ == "__main__":
    main()
