#!/usr/bin/env python3

import json
import os
import math
from typing import List, Tuple, Dict, Any

class TestDataValidator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, "sample_analysis_results/test_data")

    def validate_triangle(self, sides: Tuple[int, int, int]) -> Dict[str, Any]:
        """Validate a triangle test case"""
        a, b, c = sides
        result = {
            'valid': True,
            'type': None,
            'issues': []
        }

        # Check range
        if any(side < 1 or side > 100 for side in sides):
            result['valid'] = False
            result['issues'].append('sides_out_of_range')
            return result

        # Check triangle inequality
        if a >= b + c or b >= a + c or c >= a + b:
            result['valid'] = False
            result['issues'].append('triangle_inequality_violated')
            return result

        # Determine triangle type
        if a == b == c:
            result['type'] = 'equilateral'
        elif a == b or b == c or a == c:
            result['type'] = 'isosceles'
        else:
            # Check if right triangle (using Pythagorean theorem)
            sides_squared = sorted([x*x for x in sides])
            if abs(sides_squared[0] + sides_squared[1] - sides_squared[2]) < 0.0001:
                result['type'] = 'right'
            else:
                result['type'] = 'scalene'

        return result

    def validate_dataset(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a complete test dataset"""
        validation_result = {
            'timestamp': data.get('timestamp'),
            'total_cases': len(data.get('test_cases', [])),
            'valid_cases': 0,
            'invalid_cases': 0,
            'triangle_types': {
                'equilateral': 0,
                'isosceles': 0,
                'right': 0,
                'scalene': 0
            },
            'issues': []
        }

        for case in data.get('test_cases', []):
            result = self.validate_triangle(case)
            if result['valid']:
                validation_result['valid_cases'] += 1
                validation_result['triangle_types'][result['type']] += 1
            else:
                validation_result['invalid_cases'] += 1
                validation_result['issues'].extend(result['issues'])

        return validation_result

    def validate_file(self, filename: str) -> Dict[str, Any]:
        """Validate a test data file"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return self.validate_dataset(data)
        except Exception as e:
            return {
                'error': str(e),
                'valid': False
            }

    def validate_all(self) -> Dict[str, Dict[str, Any]]:
        """Validate all test data files"""
        results = {}
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                results[filename] = self.validate_file(filename)
        return results

    def generate_report(self, validation_results: Dict[str, Dict[str, Any]]) -> None:
        """Generate validation report"""
        report_path = os.path.join(self.data_dir, 'validation_report.md')
        
        with open(report_path, 'w') as f:
            f.write("# Test Data Validation Report\n\n")
            
            for filename, result in validation_results.items():
                f.write(f"## {filename}\n")
                if 'error' in result:
                    f.write(f"Error: {result['error']}\n\n")
                    continue
                    
                f.write(f"- Total Test Cases: {result['total_cases']}\n")
                f.write(f"- Valid Cases: {result['valid_cases']}\n")
                f.write(f"- Invalid Cases: {result['invalid_cases']}\n\n")
                
                f.write("### Triangle Types\n")
                for type_name, count in result['triangle_types'].items():
                    f.write(f"- {type_name.title()}: {count}\n")
                
                if result['issues']:
                    f.write("\n### Issues\n")
                    for issue in set(result['issues']):
                        count = result['issues'].count(issue)
                        f.write(f"- {issue}: {count} occurrences\n")
                f.write("\n")

def main():
    validator = TestDataValidator()
    results = validator.validate_all()
    validator.generate_report(results)
    print(f"Validation report generated in {validator.data_dir}/validation_report.md")

if __name__ == "__main__":
    main()
