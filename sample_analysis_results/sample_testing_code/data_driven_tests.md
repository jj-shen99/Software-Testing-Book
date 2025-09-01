# Data-Driven Test Examples

## Triangle Area Tests
```java
@ParameterizedTest
@CsvSource({
    "3, 4, 5, 6.0",      // Common right triangle
    "5, 5, 5, 10.825",   // Equilateral triangle
    "8, 15, 17, 60.0",   // Large triangle
    "1, 1, 1, 0.433"     // Minimum valid triangle
})
void testValidTriangles(int a, int b, int c, double expectedArea) {
    assertEquals(expectedArea, TriangleAreas(a, b, c), 0.001);
}

@ParameterizedTest
@CsvSource({
    "0, 4, 5",     // Below minimum
    "101, 5, 5",   // Above maximum
    "2, 2, 5",     // Invalid triangle (sum rule)
    "1, 10, 3"     // Invalid triangle (inequality)
})
void testInvalidTriangles(int a, int b, int c) {
    assertEquals(-1.0, TriangleAreas(a, b, c));
}
```

## Color Code Tests
```java
@ParameterizedTest
@CsvSource({
    "25.0, 1, 1, 1",  // Hot, sunny, rainy
    "25.0, 1, 0, 2",  // Hot, sunny, dry
    "15.0, 1, 1, 3",  // Cool, sunny, rainy
    "15.0, 1, 0, 4",  // Cool, sunny, dry
    "25.0, 0, 1, 5",  // Hot, cloudy, rainy
    "25.0, 0, 0, 6",  // Hot, cloudy, dry
    "15.0, 0, 1, 7",  // Cool, cloudy, rainy
    "15.0, 0, 0, 4"   // Cool, cloudy, dry
})
void testColorCodeCombinations(float temp, int sun, int rain, int expectedCode) {
    assertEquals(expectedCode, ColorCode(temp, sun, rain));
}
```

## Month Days Tests
```java
@ParameterizedTest
@CsvSource({
    "1, 2025, 31",   // January
    "2, 2025, 28",   // February non-leap
    "2, 2024, 29",   // February leap
    "4, 2025, 30",   // April
    "6, 2025, 30",   // June
    "7, 2025, 31",   // July
    "9, 2025, 30"    // September
})
void testDaysInMonth(int month, long year, int expectedDays) {
    assertEquals(expectedDays, daysInAMonth(month, year));
}
```

## Payment Calculation Tests
```java
@ParameterizedTest
@CsvSource({
    "40.0, 1, 2025, 1, 2666.67",  // Full time, title 1, January
    "20.0, 2, 2025, 2, 1000.0",   // Part time, title 2, February
    "30.0, 4, 2025, 3, 1000.0",   // Regular hours, title 3, April
    "0.0, 12, 2025, 1, 0.0"       // Zero hours
})
void testPaymentCalculations(float hours, int month, long year, int title, float expected) {
    assertEquals(expected, payment(hours, month, year, title), 0.01);
}
```

## Integer Operations Tests
```java
@ParameterizedTest
@CsvSource({
    "5, 3, 4",        // Small numbers
    "-5, -3, -4",     // Negative numbers
    "0, 0, 0",        // Zero
    "10, -10, 0",     // Mixed signs
    "1000, 2000, 1500" // Large numbers
})
void testAverageCalculations(int x, int y, double expected) {
    assertEquals(expected, Average(x, y), 0.01);
}
```

## Character Count Tests
```java
@ParameterizedTest
@CsvSource({
    "t, test, 2",
    "e, test, 1",
    "x, test, 0",
    "s, tests, 2",
    " , test test, 1"
})
void testCharacterCounts(String c, String s, int expected) {
    assertEquals(expected, characterCount(c, s));
}
```
