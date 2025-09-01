#!/usr/bin/env python3

import os
import sys
import time
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import numpy as np

class TriangleTestRunner:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.results_dir = os.path.join(self.base_dir, "sample_analysis_results")
        
    def run_tests(self):
        """Run all triangle tests and generate reports"""
        timestamp = datetime.now().strftime("%Y_%m_%d")
        results_path = os.path.join(self.results_dir, f"test_results_{timestamp}")
        
        # Run different test categories
        unit_results = self.run_unit_tests()
        perf_results = self.run_performance_tests()
        
        # Generate reports
        self.generate_report(results_path, unit_results, perf_results)
        
    def run_unit_tests(self):
        """Run unit tests for triangle area calculation"""
        results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0
        }
        
        test_cases = [
            (3, 4, 5, 6.0),      # Right triangle
            (5, 5, 5, 10.825),   # Equilateral
            (5, 5, 6, 12.0),     # Isosceles
            (0, 4, 5, -1.0),     # Invalid
            (101, 5, 5, -1.0)    # Out of range
        ]
        
        for a, b, c, expected in test_cases:
            results['total'] += 1
            try:
                result = self.triangle_area(a, b, c)
                if abs(result - expected) < 0.001:
                    results['passed'] += 1
                else:
                    results['failed'] += 1
            except Exception as e:
                results['failed'] += 1
                
        return results
    
    def run_performance_tests(self):
        """Run performance tests"""
        results = {
            'response_times': [],
            'errors': 0,
            'throughput': 0
        }
        
        # Single thread performance
        start_time = time.time()
        iterations = 1000000
        
        for _ in range(iterations):
            try:
                t0 = time.time()
                self.triangle_area(3, 4, 5)
                results['response_times'].append((time.time() - t0) * 1000)
            except Exception:
                results['errors'] += 1
                
        total_time = time.time() - start_time
        results['throughput'] = iterations / total_time
        
        # Concurrent performance
        with ThreadPoolExecutor(max_workers=10) as executor:
            start_time = time.time()
            futures = []
            
            for _ in range(100):
                futures.append(executor.submit(self.triangle_area, 3, 4, 5))
                
            for future in futures:
                try:
                    future.result()
                except Exception:
                    results['errors'] += 1
                    
        results['concurrent_time'] = time.time() - start_time
        
        return results
    
    def generate_report(self, results_path, unit_results, perf_results):
        """Generate test execution report"""
        os.makedirs(results_path, exist_ok=True)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'unit_tests': unit_results,
            'performance': {
                'avg_response_time': np.mean(perf_results['response_times']),
                'p95_response_time': np.percentile(perf_results['response_times'], 95),
                'throughput': perf_results['throughput'],
                'errors': perf_results['errors']
            }
        }
        
        report_file = os.path.join(results_path, 'triangle_test_report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
    def triangle_area(self, a, b, c):
        """Calculate triangle area"""
        if a < 1 or a > 100 or b < 1 or b > 100 or c < 1 or c > 100:
            return -1.0
        if (a >= b + c) or (b >= a + c) or (c >= a + b):
            return -1.0
            
        s = (a + b + c) / 2.0
        area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
        return area

def main():
    runner = TriangleTestRunner()
    runner.run_tests()

if __name__ == "__main__":
    main()
