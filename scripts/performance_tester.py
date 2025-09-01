#!/usr/bin/env python3

import time
import threading
import argparse
import os
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import numpy as np

class PerformanceTester:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.results_dir = os.path.join(self.base_dir, "sample_analysis_results")
        
    def run_load_test(self, users=100, duration=60):
        """Run load test with specified number of concurrent users"""
        start_time = time.time()
        results = {
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'errors': []
        }
        
        def user_session():
            try:
                session_start = time.time()
                # Simulate user operations
                self._execute_test_scenario()
                response_time = time.time() - session_start
                
                with threading.Lock():
                    results['successful_requests'] += 1
                    results['response_times'].append(response_time)
            except Exception as e:
                with threading.Lock():
                    results['failed_requests'] += 1
                    results['errors'].append(str(e))
        
        # Execute concurrent user sessions
        with ThreadPoolExecutor(max_workers=users) as executor:
            while time.time() - start_time < duration:
                executor.submit(user_session)
                time.sleep(0.1)  # Prevent overwhelming the system
                
        return self._analyze_results(results)
    
    def run_stress_test(self, start_users=100, max_users=1000, step=100):
        """Run stress test with increasing user load"""
        stress_results = []
        
        for num_users in range(start_users, max_users + 1, step):
            print(f"Testing with {num_users} users...")
            result = self.run_load_test(users=num_users, duration=30)
            result['num_users'] = num_users
            stress_results.append(result)
            
            # Check for performance degradation
            if self._check_degradation(result):
                print(f"Performance degradation detected at {num_users} users")
                break
                
        return stress_results
    
    def run_endurance_test(self, users=100, duration=3600):
        """Run endurance test for extended period"""
        start_time = time.time()
        interval_results = []
        
        while time.time() - start_time < duration:
            result = self.run_load_test(users=users, duration=300)  # 5-minute intervals
            interval_results.append(result)
            
            if self._check_degradation(result):
                print("Performance degradation detected during endurance test")
                break
                
        return interval_results
    
    def _execute_test_scenario(self):
        """Execute a single test scenario"""
        # Simulate typical user operations
        operations = [
            self._simulate_database_query,
            self._simulate_computation,
            self._simulate_io_operation
        ]
        
        for op in operations:
            op()
    
    def _simulate_database_query(self):
        """Simulate database operation"""
        time.sleep(np.random.normal(0.1, 0.02))  # Mean 100ms, SD 20ms
    
    def _simulate_computation(self):
        """Simulate CPU-intensive computation"""
        time.sleep(np.random.normal(0.05, 0.01))  # Mean 50ms, SD 10ms
    
    def _simulate_io_operation(self):
        """Simulate I/O operation"""
        time.sleep(np.random.normal(0.15, 0.03))  # Mean 150ms, SD 30ms
    
    def _analyze_results(self, results):
        """Analyze test results"""
        if not results['response_times']:
            return None
            
        analysis = {
            'total_requests': results['successful_requests'] + results['failed_requests'],
            'success_rate': results['successful_requests'] / (results['successful_requests'] + results['failed_requests']) * 100,
            'avg_response_time': np.mean(results['response_times']),
            'p95_response_time': np.percentile(results['response_times'], 95),
            'max_response_time': max(results['response_times']),
            'min_response_time': min(results['response_times']),
            'error_count': len(results['errors'])
        }
        
        # Save results
        self._save_results(analysis)
        return analysis
    
    def _check_degradation(self, result):
        """Check for performance degradation"""
        if result['avg_response_time'] > 1.0:  # More than 1 second average
            return True
        if result['success_rate'] < 95:  # Less than 95% success rate
            return True
        return False
    
    def _save_results(self, results):
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        results_path = os.path.join(self.results_dir, 
                                  datetime.now().strftime("%Y_%m_%d"),
                                  "performance")
        os.makedirs(results_path, exist_ok=True)
        
        with open(os.path.join(results_path, f"perf_results_{timestamp}.json"), 'w') as f:
            json.dump(results, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Run performance tests")
    parser.add_argument("--type", choices=['load', 'stress', 'endurance'], 
                      required=True, help="Type of performance test")
    parser.add_argument("--users", type=int, default=100,
                      help="Number of concurrent users")
    parser.add_argument("--duration", type=int, default=60,
                      help="Test duration in seconds")
    
    args = parser.parse_args()
    tester = PerformanceTester()
    
    if args.type == 'load':
        results = tester.run_load_test(users=args.users, duration=args.duration)
    elif args.type == 'stress':
        results = tester.run_stress_test(start_users=args.users)
    else:
        results = tester.run_endurance_test(users=args.users, duration=args.duration)
        
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
