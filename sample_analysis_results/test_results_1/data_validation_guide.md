# Data Validation Guide

## Quick Start
```bash
# Validate test data
./scripts/data_quality_validator.py

# Validate specific dataset
./scripts/data_quality_validator.py --file custom_data.json

# Generate validation report
./scripts/data_quality_validator.py --report
```

## Validation Rules

### Triangle Properties
```yaml
# Triangle validation rules
sides:
  min_value: 1
  max_value: 100
  type: integer

inequalities:
  - "a + b > c"
  - "b + c > a"
  - "a + c > b"
```

### Dataset Requirements
```yaml
dataset:
  size:
    small: 10-20 cases
    medium: 100-200 cases
    large: 1000-2000 cases
    
  distribution:
    valid_ratio: 60-80%
    triangle_types:
      equilateral: 25%
      isosceles: 25%
      right: 25%
      scalene: 25%
```

## Data Quality Checks

### 1. Completeness
- Required fields present
- No missing values
- Valid data types

### 2. Consistency
- Triangle inequalities
- Area calculations
- Type classifications

### 3. Distribution
- Size ranges
- Type ratios
- Valid/invalid ratios

### 4. Accuracy
- Integer sides
- Precise calculations
- Correct classifications

## Validation Reports

### Summary Metrics
```json
{
    "total_cases": 1000,
    "valid_cases": 950,
    "invalid_cases": 50,
    "validation_rate": 95.0,
    "triangle_types": {
        "equilateral": 237,
        "isosceles": 238,
        "right": 237,
        "scalene": 238
    }
}
```

### Error Categories
1. **Critical Errors**
   - Invalid triangle dimensions
   - Missing required fields
   - Data type mismatches

2. **Warnings**
   - Distribution skew
   - High duplicates
   - Unusual dimensions

3. **Info Messages**
   - Rare triangle types
   - Edge case scenarios

## Best Practices

### 1. Data Generation
```python
# Generate balanced datasets
generator = TriangleTestDataGenerator()
data = generator.generate_dataset(
    size=1000,
    distribution={
        'equilateral': 0.25,
        'isosceles': 0.25,
        'right': 0.25,
        'scalene': 0.25
    }
)
```

### 2. Data Validation
```python
# Validate with custom rules
validator = DataQualityValidator()
results = validator.validate_dataset(
    data,
    rules={
        'valid_ratio': 0.95,
        'max_duplicates': 0.01
    }
)
```

### 3. Report Generation
```python
# Generate detailed report
validator.generate_report(
    results,
    format='markdown',
    include_metrics=True,
    save_path='validation_reports/'
)
```

## Troubleshooting

### Common Issues
1. **Invalid Data Format**
   ```bash
   # Check data format
   ./scripts/data_quality_validator.py --check-format
   ```

2. **Distribution Issues**
   ```bash
   # Analyze distribution
   ./scripts/data_quality_validator.py --analyze-dist
   ```

3. **Quality Issues**
   ```bash
   # Check data quality
   ./scripts/data_quality_validator.py --quality-check
   ```

### Getting Help
```bash
# Show validation help
./scripts/data_quality_validator.py --help

# List available rules
./scripts/data_quality_validator.py --list-rules
```
