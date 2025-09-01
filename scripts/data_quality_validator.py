#!/usr/bin/env python3

import os
import json
import yaml
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple

class DataQualityValidator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.rules_file = os.path.join(self.base_dir, "scripts/test_data_validator_rules.yml")
        self.results_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "validation"
        )
        os.makedirs(self.results_dir, exist_ok=True)
        self.load_rules()

    def load_rules(self):
        """Load validation rules from YAML"""
        with open(self.rules_file, 'r') as f:
            self.rules = yaml.safe_load(f)

    def validate_triangle(self, sides: Tuple[int, int, int]) -> Dict[str, Any]:
        """Validate a single triangle"""
        a, b, c = sides
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'type': None,
            'metrics': {}
        }

        # Range validation
        rules = self.rules['triangle']['sides']
        if not all(rules['min_value'] <= side <= rules['max_value'] for side in sides):
            result['valid'] = False
            result['errors'].append('sides_out_of_range')

        # Triangle inequality
        if not (a + b > c and b + c > a and a + c > b):
            result['valid'] = False
            result['errors'].append('triangle_inequality_violated')

        # Triangle type
        if result['valid']:
            if a == b == c:
                result['type'] = 'equilateral'
            elif a == b or b == c or a == c:
                result['type'] = 'isosceles'
            elif self._is_right_triangle(a, b, c):
                result['type'] = 'right'
            else:
                result['type'] = 'scalene'

        # Calculate metrics
        result['metrics'] = {
            'perimeter': sum(sides),
            'area': self._calculate_area(a, b, c),
            'size_ratio': max(sides) / min(sides) if min(sides) > 0 else float('inf')
        }

        return result

    def validate_dataset(self, data: List[Tuple[int, int, int]]) -> Dict[str, Any]:
        """Validate entire dataset"""
        results = {
            'total_cases': len(data),
            'valid_cases': 0,
            'invalid_cases': 0,
            'triangle_types': {
                'equilateral': 0,
                'isosceles': 0,
                'right': 0,
                'scalene': 0
            },
            'errors': [],
            'warnings': [],
            'metrics': {
                'size_distribution': [],
                'area_distribution': [],
                'perimeter_distribution': []
            }
        }

        for triangle in data:
            validation = self.validate_triangle(triangle)
            
            if validation['valid']:
                results['valid_cases'] += 1
                results['triangle_types'][validation['type']] += 1
                results['metrics']['size_distribution'].extend(triangle)
                results['metrics']['area_distribution'].append(validation['metrics']['area'])
                results['metrics']['perimeter_distribution'].append(validation['metrics']['perimeter'])
            else:
                results['invalid_cases'] += 1
                results['errors'].extend(validation['errors'])

        # Dataset-level validation
        self._validate_distribution(results)
        self._validate_quality_metrics(results)

        return results

    def _is_right_triangle(self, a: int, b: int, c: int) -> bool:
        """Check if triangle is right-angled"""
        sides = sorted([a, b, c])
        return abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 0.0001

    def _calculate_area(self, a: int, b: int, c: int) -> float:
        """Calculate triangle area using Heron's formula"""
        s = (a + b + c) / 2
        area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
        return area

    def _validate_distribution(self, results: Dict[str, Any]):
        """Validate dataset distribution"""
        rules = self.rules['dataset']['distribution']
        
        # Check triangle type distribution
        total_valid = results['valid_cases']
        if total_valid > 0:
            for triangle_type, expected_ratio in rules['triangle_types'].items():
                actual_ratio = results['triangle_types'][triangle_type] / total_valid
                if abs(actual_ratio - expected_ratio) > 0.1:
                    results['warnings'].append(
                        f"{triangle_type}_distribution_skewed:"
                        f" {actual_ratio:.2f} vs expected {expected_ratio:.2f}"
                    )

        # Check valid/invalid ratio
        valid_ratio = results['valid_cases'] / results['total_cases']
        if not rules['valid_ratio']['min'] <= valid_ratio <= rules['valid_ratio']['max']:
            results['warnings'].append(
                f"valid_ratio_outside_range: {valid_ratio:.2f}"
            )

    def _validate_quality_metrics(self, results: Dict[str, Any]):
        """Validate data quality metrics"""
        quality_rules = self.rules['quality']
        
        # Check completeness
        missing_rate = results['invalid_cases'] / results['total_cases']
        if missing_rate > quality_rules['completeness']['missing_threshold']:
            results['warnings'].append(
                f"high_missing_rate: {missing_rate:.2f}"
            )

        # Check distribution metrics
        for metric in ['size_distribution', 'area_distribution', 'perimeter_distribution']:
            if results['metrics'][metric]:
                mean = np.mean(results['metrics'][metric])
                std = np.std(results['metrics'][metric])
                results['metrics'][f"{metric}_stats"] = {
                    'mean': mean,
                    'std': std,
                    'min': min(results['metrics'][metric]),
                    'max': max(results['metrics'][metric]),
                    'p25': np.percentile(results['metrics'][metric], 25),
                    'p50': np.percentile(results['metrics'][metric], 50),
                    'p75': np.percentile(results['metrics'][metric], 75)
                }

    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate validation report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(self.results_dir, f'validation_report_{timestamp}.md')
        
        with open(report_file, 'w') as f:
            f.write("# Data Validation Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Summary\n")
            f.write(f"- Total Cases: {results['total_cases']}\n")
            f.write(f"- Valid Cases: {results['valid_cases']}\n")
            f.write(f"- Invalid Cases: {results['invalid_cases']}\n")
            f.write(f"- Validation Rate: {(results['valid_cases']/results['total_cases']*100):.1f}%\n\n")
            
            f.write("## Triangle Types\n")
            for type_name, count in results['triangle_types'].items():
                if results['valid_cases'] > 0:
                    percentage = (count / results['valid_cases']) * 100
                    f.write(f"- {type_name.title()}: {count} ({percentage:.1f}%)\n")
            
            if results['errors']:
                f.write("\n## Errors\n")
                for error in set(results['errors']):
                    count = results['errors'].count(error)
                    f.write(f"- {error}: {count} occurrences\n")
            
            if results['warnings']:
                f.write("\n## Warnings\n")
                for warning in set(results['warnings']):
                    f.write(f"- {warning}\n")
            
            f.write("\n## Distribution Metrics\n")
            for metric, stats in results['metrics'].items():
                if isinstance(stats, dict) and metric.endswith('_stats'):
                    f.write(f"\n### {metric.replace('_stats', '').title()}\n")
                    for stat_name, value in stats.items():
                        f.write(f"- {stat_name}: {value:.2f}\n")
        
        return report_file

def main():
    validator = DataQualityValidator()
    
    # Example usage
    test_data = [
        (3, 4, 5),      # Right triangle
        (5, 5, 5),      # Equilateral
        (5, 5, 6),      # Isosceles
        (0, 4, 5),      # Invalid
        (101, 5, 5)     # Invalid
    ]
    
    results = validator.validate_dataset(test_data)
    report_file = validator.generate_report(results)
    print(f"Validation report generated: {report_file}")

if __name__ == "__main__":
    main()
