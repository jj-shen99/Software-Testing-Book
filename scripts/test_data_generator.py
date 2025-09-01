#!/usr/bin/env python3

import random
import json
import os
from datetime import datetime
import numpy as np

class TriangleTestDataGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, "sample_analysis_results/test_data")
        os.makedirs(self.data_dir, exist_ok=True)

    def generate_valid_triangles(self, count=100):
        """Generate valid triangle test cases"""
        triangles = []
        
        # Right triangles
        for _ in range(count // 4):
            a = random.randint(3, 50)
            b = random.randint(3, 50)
            c = int((a*a + b*b) ** 0.5)
            if c <= 100:
                triangles.append((a, b, c))
                
        # Equilateral triangles
        for _ in range(count // 4):
            side = random.randint(1, 33)  # Max 33 to ensure area < 100
            triangles.append((side, side, side))
            
        # Isosceles triangles
        for _ in range(count // 4):
            equal_side = random.randint(2, 50)
            base = random.randint(1, equal_side * 2 - 1)
            if base + equal_side > equal_side:  # Triangle inequality
                triangles.append((equal_side, equal_side, base))
                
        # Scalene triangles
        while len(triangles) < count:
            a = random.randint(2, 50)
            b = random.randint(2, 50)
            c = random.randint(max(abs(a-b)+1, 2), min(a+b-1, 100))
            if c < a + b and a < b + c and b < a + c:
                triangles.append((a, b, c))
                
        return triangles

    def generate_invalid_triangles(self, count=50):
        """Generate invalid triangle test cases"""
        triangles = []
        
        # Out of range values
        for _ in range(count // 3):
            case = random.choice([
                (0, random.randint(1, 100), random.randint(1, 100)),
                (random.randint(1, 100), 0, random.randint(1, 100)),
                (random.randint(1, 100), random.randint(1, 100), 0),
                (101, random.randint(1, 100), random.randint(1, 100)),
                (random.randint(1, 100), 101, random.randint(1, 100)),
                (random.randint(1, 100), random.randint(1, 100), 101)
            ])
            triangles.append(case)
            
        # Violate triangle inequality
        while len(triangles) < count:
            a = random.randint(1, 50)
            b = random.randint(1, 50)
            c = random.randint(a + b, a + b + 10)
            if c <= 100:
                triangles.append((a, b, c))
                
        return triangles

    def generate_performance_data(self, size=1000):
        """Generate performance test data"""
        valid = self.generate_valid_triangles(size // 2)
        invalid = self.generate_invalid_triangles(size // 2)
        
        # Mix and shuffle test cases
        test_cases = valid + invalid
        random.shuffle(test_cases)
        
        return test_cases

    def save_test_data(self, filename, data):
        """Save test data to file"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'count': len(data),
                'test_cases': data
            }, f, indent=2)

    def generate_all(self):
        """Generate all test datasets"""
        # Generate different sizes of test data
        datasets = {
            'small': {
                'valid': self.generate_valid_triangles(10),
                'invalid': self.generate_invalid_triangles(5)
            },
            'medium': {
                'valid': self.generate_valid_triangles(100),
                'invalid': self.generate_invalid_triangles(50)
            },
            'large': {
                'valid': self.generate_valid_triangles(1000),
                'invalid': self.generate_invalid_triangles(500)
            },
            'performance': self.generate_performance_data(10000)
        }
        
        # Save each dataset
        for name, data in datasets.items():
            self.save_test_data(f'{name}_dataset.json', data)
            
        return datasets

def main():
    generator = TriangleTestDataGenerator()
    generator.generate_all()
    print(f"Test data generated in {generator.data_dir}")

if __name__ == "__main__":
    main()
