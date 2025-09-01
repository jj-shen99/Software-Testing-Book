#!/usr/bin/env python3

import os
import yaml
import json
import logging
import subprocess
from datetime import datetime
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor

class TestWorkflowRunner:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(
            self.base_dir,
            "workflows/yaml_workflows/test_workflow_config.yml"
        )
        self.results_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}"
        )
        os.makedirs(self.results_dir, exist_ok=True)
        self.setup_logging()
        self.load_config()

    def setup_logging(self):
        """Configure logging"""
        log_file = os.path.join(self.results_dir, 'workflow.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self):
        """Load workflow configuration"""
        with open(self.config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def setup_environment(self):
        """Set up test environment"""
        self.logger.info("Setting up test environment...")
        for step in self.config['environment']['setup']:
            try:
                getattr(self, f"_setup_{step}")()
            except Exception as e:
                self.logger.error(f"Error in setup step {step}: {str(e)}")
                raise

    def _setup_clean_workspace(self):
        """Clean workspace before testing"""
        self.logger.info("Cleaning workspace...")
        for dir_name in ['unit', 'integration', 'performance']:
            dir_path = os.path.join(self.results_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)

    def _setup_init_database(self):
        """Initialize test database"""
        self.logger.info("Initializing test database...")
        # Implementation specific to your database needs

    def _setup_load_test_data(self):
        """Load test data"""
        self.logger.info("Loading test data...")
        subprocess.run(
            ["python3", "scripts/test_data_generator.py"],
            cwd=self.base_dir,
            check=True
        )

    def run_tests(self, category: str = None):
        """Run tests by category"""
        if category and category not in self.config['categories']:
            raise ValueError(f"Invalid test category: {category}")

        categories = [category] if category else self.config['categories'].keys()
        results = {}

        for cat in categories:
            self.logger.info(f"Running {cat} tests...")
            cat_config = self.config['categories'][cat]

            if cat_config['parallel']:
                results[cat] = self._run_parallel_tests(cat)
            else:
                results[cat] = self._run_sequential_tests(cat)

        return results

    def _run_parallel_tests(self, category: str) -> Dict[str, Any]:
        """Run tests in parallel"""
        max_workers = self.config['execution']['max_workers']
        timeout = self.config['categories'][category]['timeout']

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for test_file in self._get_test_files(category):
                futures.append(
                    executor.submit(self._run_single_test, test_file, timeout)
                )

        return {
            'total': len(futures),
            'results': [f.result() for f in futures]
        }

    def _run_sequential_tests(self, category: str) -> Dict[str, Any]:
        """Run tests sequentially"""
        results = []
        timeout = self.config['categories'][category]['timeout']

        for test_file in self._get_test_files(category):
            results.append(self._run_single_test(test_file, timeout))

        return {
            'total': len(results),
            'results': results
        }

    def _run_single_test(self, test_file: str, timeout: int) -> Dict[str, Any]:
        """Run a single test"""
        try:
            start_time = datetime.now()
            result = subprocess.run(
                ["python3", test_file],
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            duration = (datetime.now() - start_time).total_seconds()

            return {
                'file': test_file,
                'status': 'pass' if result.returncode == 0 else 'fail',
                'duration': duration,
                'output': result.stdout,
                'error': result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                'file': test_file,
                'status': 'timeout',
                'duration': timeout,
                'output': '',
                'error': f'Test exceeded timeout of {timeout} seconds'
            }
        except Exception as e:
            return {
                'file': test_file,
                'status': 'error',
                'duration': 0,
                'output': '',
                'error': str(e)
            }

    def _get_test_files(self, category: str) -> List[str]:
        """Get test files for category"""
        test_dir = os.path.join(self.base_dir, 'sample_analysis_results/test_data')
        pattern = f"*_{category}_*.py"
        
        test_files = []
        for root, _, files in os.walk(test_dir):
            for file in files:
                if file.endswith('.py') and category in file:
                    test_files.append(os.path.join(root, file))
                    
        return test_files

    def analyze_results(self, results: Dict[str, Any]):
        """Analyze test results"""
        self.logger.info("Analyzing test results...")
        
        analysis = {
            'summary': {
                'total_tests': sum(r['total'] for r in results.values()),
                'passed': 0,
                'failed': 0,
                'errors': 0,
                'timeouts': 0
            },
            'categories': {}
        }

        for category, result in results.items():
            cat_analysis = {
                'total': result['total'],
                'passed': 0,
                'failed': 0,
                'errors': 0,
                'timeouts': 0,
                'duration': 0
            }

            for test in result['results']:
                if test['status'] == 'pass':
                    cat_analysis['passed'] += 1
                elif test['status'] == 'fail':
                    cat_analysis['failed'] += 1
                elif test['status'] == 'error':
                    cat_analysis['errors'] += 1
                elif test['status'] == 'timeout':
                    cat_analysis['timeouts'] += 1

                cat_analysis['duration'] += test['duration']

            analysis['categories'][category] = cat_analysis
            analysis['summary']['passed'] += cat_analysis['passed']
            analysis['summary']['failed'] += cat_analysis['failed']
            analysis['summary']['errors'] += cat_analysis['errors']
            analysis['summary']['timeouts'] += cat_analysis['timeouts']

        return analysis

    def generate_report(self, results: Dict[str, Any], analysis: Dict[str, Any]):
        """Generate test report"""
        self.logger.info("Generating test report...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(self.results_dir, f'test_report_{timestamp}.md')

        with open(report_file, 'w') as f:
            f.write("# Test Execution Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Summary\n")
            summary = analysis['summary']
            f.write(f"- Total Tests: {summary['total_tests']}\n")
            f.write(f"- Passed: {summary['passed']}\n")
            f.write(f"- Failed: {summary['failed']}\n")
            f.write(f"- Errors: {summary['errors']}\n")
            f.write(f"- Timeouts: {summary['timeouts']}\n\n")

            for category, cat_analysis in analysis['categories'].items():
                f.write(f"## {category.title()} Tests\n")
                f.write(f"- Total: {cat_analysis['total']}\n")
                f.write(f"- Passed: {cat_analysis['passed']}\n")
                f.write(f"- Failed: {cat_analysis['failed']}\n")
                f.write(f"- Errors: {cat_analysis['errors']}\n")
                f.write(f"- Timeouts: {cat_analysis['timeouts']}\n")
                f.write(f"- Duration: {cat_analysis['duration']:.2f}s\n\n")

                f.write("### Failed Tests\n")
                for test in results[category]['results']:
                    if test['status'] != 'pass':
                        f.write(f"#### {os.path.basename(test['file'])}\n")
                        f.write(f"- Status: {test['status']}\n")
                        f.write(f"- Duration: {test['duration']:.2f}s\n")
                        if test['error']:
                            f.write("```\n")
                            f.write(test['error'])
                            f.write("\n```\n")
                        f.write("\n")

        return report_file

    def cleanup_environment(self):
        """Clean up test environment"""
        self.logger.info("Cleaning up test environment...")
        for step in self.config['environment']['teardown']:
            try:
                getattr(self, f"_cleanup_{step}")()
            except Exception as e:
                self.logger.error(f"Error in cleanup step {step}: {str(e)}")

    def _cleanup_cleanup_data(self):
        """Clean up test data"""
        pass  # Implementation specific to your needs

    def _cleanup_reset_state(self):
        """Reset system state"""
        pass  # Implementation specific to your needs

    def _cleanup_archive_results(self):
        """Archive test results"""
        self.logger.info("Archiving test results...")
        # Implementation specific to your archival needs

def main():
    runner = TestWorkflowRunner()

    try:
        # Setup
        runner.setup_environment()

        # Run tests
        results = runner.run_tests()

        # Analyze results
        analysis = runner.analyze_results(results)

        # Generate report
        report_file = runner.generate_report(results, analysis)
        print(f"Test report generated: {report_file}")

    except Exception as e:
        runner.logger.error(f"Error in test workflow: {str(e)}")
        raise
    finally:
        runner.cleanup_environment()

if __name__ == "__main__":
    main()
