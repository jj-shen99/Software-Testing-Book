#!/usr/bin/env python3

import argparse
import subprocess
import os
import sys
from datetime import datetime

class TestRunner:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.results_dir = os.path.join(self.base_dir, "sample_analysis_results")
        
    def setup_results_directory(self):
        """Create results directory with timestamp"""
        timestamp = datetime.now().strftime("%Y_%m_%d")
        results_path = os.path.join(self.results_dir, f"test_results_{timestamp}")
        os.makedirs(results_path, exist_ok=True)
        return results_path
        
    def run_chapter_tests(self, chapter):
        """Run tests for specific chapter"""
        results_path = self.setup_results_directory()
        test_file = f"Chapter{chapter}Test.java"
        
        try:
            # Compile and run tests
            subprocess.run(["javac", test_file], check=True)
            result = subprocess.run(
                ["java", "-cp", ".", f"Chapter{chapter}Test"],
                capture_output=True,
                text=True
            )
            
            # Save results
            with open(os.path.join(results_path, f"chapter_{chapter}_results.txt"), "w") as f:
                f.write(result.stdout)
            
            return result.returncode == 0
            
        except subprocess.CalledProcessError as e:
            print(f"Error running tests for chapter {chapter}: {e}")
            return False
            
    def run_category_tests(self, category):
        """Run tests by category (e.g., performance, security)"""
        results_path = self.setup_results_directory()
        
        try:
            result = subprocess.run(
                ["python3", "-m", "pytest", f"--category={category}"],
                capture_output=True,
                text=True
            )
            
            # Save results
            with open(os.path.join(results_path, f"{category}_results.txt"), "w") as f:
                f.write(result.stdout)
            
            return result.returncode == 0
            
        except subprocess.CalledProcessError as e:
            print(f"Error running {category} tests: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Run software testing examples")
    parser.add_argument("--chapter", type=int, help="Run tests for specific chapter")
    parser.add_argument("--category", type=str, help="Run tests by category")
    
    args = parser.parse_args()
    runner = TestRunner()
    
    if args.chapter:
        success = runner.run_chapter_tests(args.chapter)
    elif args.category:
        success = runner.run_category_tests(args.category)
    else:
        print("Please specify either --chapter or --category")
        sys.exit(1)
        
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
