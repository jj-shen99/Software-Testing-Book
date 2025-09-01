# Test Data Generation and Validation Guide

## Generating Test Data
```bash
# Generate all test datasets
./scripts/test_data_generator.py

# Generate specific dataset
./scripts/test_data_generator.py --type performance
./scripts/test_data_generator.py --size 1000
```

## Test Data Structure
```json
{
    "timestamp": "2025-09-01T12:00:00",
    "count": 100,
    "test_cases": [
        [3, 4, 5],     // Right triangle
        [5, 5, 5],     // Equilateral
        [5, 5, 6],     // Isosceles
        [0, 4, 5],     // Invalid: zero side
        [101, 5, 5]    // Invalid: out of range
    ]
}
```

## Available Datasets
1. **Small Dataset** (15 cases)
   - 10 valid triangles
   - 5 invalid triangles
   - Use for quick tests

2. **Medium Dataset** (150 cases)
   - 100 valid triangles
   - 50 invalid triangles
   - Use for regular testing

3. **Large Dataset** (1500 cases)
   - 1000 valid triangles
   - 500 invalid triangles
   - Use for thorough testing

4. **Performance Dataset** (10000 cases)
   - Mixed valid and invalid cases
   - Use for performance testing

## Data Validation
```bash
# Validate all datasets
./scripts/test_data_validator.py

# Validate specific file
./scripts/test_data_validator.py --file large_dataset.json
```

## Validation Rules
1. **Range Check**
   - All sides must be between 1 and 100
   - Values outside range marked invalid

2. **Triangle Inequality**
   - Sum of any two sides > third side
   - Violations marked invalid

3. **Triangle Types**
   - Equilateral: all sides equal
   - Isosceles: two sides equal
   - Right: follows Pythagorean theorem
   - Scalene: all sides different

## Validation Report
```markdown
# Test Data Validation Report

## large_dataset.json
- Total Test Cases: 1500
- Valid Cases: 1000
- Invalid Cases: 500

### Triangle Types
- Equilateral: 250
- Isosceles: 250
- Right: 250
- Scalene: 250

### Issues
- sides_out_of_range: 250
- triangle_inequality_violated: 250
```

## Best Practices
1. **Data Generation**
   - Use appropriate dataset size
   - Include edge cases
   - Maintain data distribution
   - Version control datasets

2. **Validation**
   - Validate before testing
   - Check data integrity
   - Monitor distributions
   - Track validation history

3. **Usage**
   - Load appropriate dataset
   - Cache when possible
   - Monitor memory usage
   - Clean up after tests
