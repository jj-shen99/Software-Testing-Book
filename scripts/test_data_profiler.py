#!/usr/bin/env python3

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_profiling import ProfileReport

class TestDataProfiler:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, "sample_analysis_results/test_data")
        self.profile_dir = os.path.join(
            self.base_dir,
            "sample_analysis_results",
            f"test_results_{datetime.now().strftime('%Y_%m_%d')}",
            "profiles"
        )
        os.makedirs(self.profile_dir, exist_ok=True)

    def load_test_data(self, file_path: str) -> pd.DataFrame:
        """Load test data into DataFrame"""
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Convert test cases to DataFrame
        records = []
        for case in data.get('test_cases', []):
            if isinstance(case, (list, tuple)):
                record = {
                    'side_a': case[0],
                    'side_b': case[1],
                    'side_c': case[2]
                }
                record.update(self._calculate_triangle_properties(case))
                records.append(record)
                
        return pd.DataFrame(records)

    def _calculate_triangle_properties(self, sides: List[int]) -> Dict[str, Any]:
        """Calculate triangle properties"""
        a, b, c = sides
        properties = {
            'perimeter': sum(sides),
            'max_side': max(sides),
            'min_side': min(sides),
            'side_ratio': max(sides) / min(sides) if min(sides) > 0 else float('inf')
        }
        
        # Calculate area using Heron's formula
        s = properties['perimeter'] / 2
        try:
            area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
            properties['area'] = area
        except:
            properties['area'] = 0
            
        # Determine triangle type
        if a == b == c:
            properties['type'] = 'equilateral'
        elif a == b or b == c or a == c:
            properties['type'] = 'isosceles'
        elif self._is_right_triangle(a, b, c):
            properties['type'] = 'right'
        else:
            properties['type'] = 'scalene'
            
        # Validate triangle
        properties['is_valid'] = (
            all(side > 0 and side <= 100 for side in sides) and
            a + b > c and b + c > a and a + c > b
        )
        
        return properties

    def _is_right_triangle(self, a: int, b: int, c: int) -> bool:
        """Check if triangle is right-angled"""
        sides = sorted([a, b, c])
        return abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 0.0001

    def generate_profile(self, df: pd.DataFrame, title: str) -> None:
        """Generate pandas profiling report"""
        profile = ProfileReport(
            df,
            title=title,
            explorative=True,
            minimal=False
        )
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(self.profile_dir, f'profile_{timestamp}.html')
        profile.to_file(report_path)
        
        return report_path

    def analyze_distributions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data distributions"""
        analysis = {
            'triangle_types': df['type'].value_counts().to_dict(),
            'validity_ratio': df['is_valid'].mean(),
            'size_stats': {
                'mean': df[['side_a', 'side_b', 'side_c']].mean().to_dict(),
                'std': df[['side_a', 'side_b', 'side_c']].std().to_dict(),
                'min': df[['side_a', 'side_b', 'side_c']].min().to_dict(),
                'max': df[['side_a', 'side_b', 'side_c']].max().to_dict()
            },
            'area_stats': {
                'mean': df['area'].mean(),
                'std': df['area'].std(),
                'min': df['area'].min(),
                'max': df['area'].max()
            }
        }
        
        return analysis

    def plot_distributions(self, df: pd.DataFrame) -> None:
        """Create distribution plots"""
        # Set up the plotting style
        plt.style.use('seaborn')
        
        # Create figure with subplots
        fig = plt.figure(figsize=(15, 10))
        
        # Triangle types distribution
        plt.subplot(2, 2, 1)
        sns.countplot(data=df, x='type')
        plt.title('Triangle Types Distribution')
        plt.xticks(rotation=45)
        
        # Side lengths distribution
        plt.subplot(2, 2, 2)
        df[['side_a', 'side_b', 'side_c']].boxplot()
        plt.title('Side Lengths Distribution')
        
        # Area distribution
        plt.subplot(2, 2, 3)
        sns.histplot(data=df, x='area', bins=30)
        plt.title('Area Distribution')
        
        # Side ratios distribution
        plt.subplot(2, 2, 4)
        sns.histplot(data=df, x='side_ratio', bins=30)
        plt.title('Side Ratios Distribution')
        
        plt.tight_layout()
        
        # Save plot
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plot_path = os.path.join(self.profile_dir, f'distributions_{timestamp}.png')
        plt.savefig(plot_path)
        plt.close()
        
        return plot_path

    def generate_report(self, df: pd.DataFrame, analysis: Dict[str, Any]) -> str:
        """Generate analysis report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(self.profile_dir, f'analysis_{timestamp}.md')
        
        with open(report_path, 'w') as f:
            f.write("# Test Data Analysis Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Dataset Overview\n")
            f.write(f"- Total Cases: {len(df)}\n")
            f.write(f"- Valid Cases: {int(df['is_valid'].sum())}\n")
            f.write(f"- Validity Ratio: {analysis['validity_ratio']:.2%}\n\n")
            
            f.write("## Triangle Types\n")
            for type_name, count in analysis['triangle_types'].items():
                f.write(f"- {type_name.title()}: {count} ({count/len(df):.2%})\n")
            f.write("\n")
            
            f.write("## Size Statistics\n")
            for side, stats in analysis['size_stats'].items():
                f.write(f"### {side.replace('side_', 'Side ')}\n")
                for stat_name, value in stats.items():
                    f.write(f"- {stat_name.title()}: {value:.2f}\n")
                f.write("\n")
            
            f.write("## Area Statistics\n")
            for stat_name, value in analysis['area_stats'].items():
                f.write(f"- {stat_name.title()}: {value:.2f}\n")
            
        return report_path

    def profile_dataset(self, file_path: str) -> Dict[str, str]:
        """Profile a test dataset"""
        # Load and process data
        df = self.load_test_data(file_path)
        
        # Generate analysis
        analysis = self.analyze_distributions(df)
        
        # Create outputs
        results = {
            'profile': self.generate_profile(df, "Test Data Profile"),
            'plots': self.plot_distributions(df),
            'report': self.generate_report(df, analysis)
        }
        
        return results

def main():
    profiler = TestDataProfiler()
    
    # Profile all datasets
    for file in os.listdir(profiler.data_dir):
        if file.endswith('.json'):
            print(f"Profiling {file}...")
            file_path = os.path.join(profiler.data_dir, file)
            results = profiler.profile_dataset(file_path)
            
            print(f"Generated outputs:")
            for output_type, path in results.items():
                print(f"- {output_type}: {path}")
            print()

if __name__ == "__main__":
    main()
