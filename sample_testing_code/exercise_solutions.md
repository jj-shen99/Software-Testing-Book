# Software Testing Exercise Solutions

## Chapter 1: Introduction
### Exercise 1: Basic Function Testing
```java
@Test
void testTriangleArea() {
    // Based on TriangleAreas function
    assertEquals(6.0, TriangleAreas(3, 4, 5), 0.01);
    assertEquals(-1.0, TriangleAreas(1, 1, 3)); // Invalid triangle
    assertEquals(-1.0, TriangleAreas(0, 4, 5)); // Out of range
}
```

## Chapter 2: Testing Fundamentals
### Exercise 1: Boundary Testing
```java
@Test
void testMonthValidation() {
    // Based on MonthNumber function
    assertEquals(1, MonthNumber(1));  // Lower bound
    assertEquals(12, MonthNumber(12)); // Upper bound
    assertEquals(-1, MonthNumber(13)); // Invalid
    assertEquals(-1, MonthNumber(0));  // Invalid
}
```

## Chapter 3: Testing Methodologies
### Exercise 1: Integration Testing
```java
@Test
void testColorCodeIntegration() {
    // Based on ColorCode function
    assertEquals(1, ColorCode(20.0f, 1, 1)); // Sunny, warm, rainy
    assertEquals(4, ColorCode(15.0f, 1, 0)); // Sunny, cool, dry
    assertEquals(7, ColorCode(15.0f, 0, 1)); // Cloudy, cool, rainy
}
```

## Chapter 4: Test Design
### Exercise 1: Exception Handling
```java
@Test
void testIntegerAddOverflow() {
    // Based on IntegerAdd function
    assertEquals(5, IntegerAdd(2, 3));
    
    // Test overflow conditions
    int maxInt = Integer.MAX_VALUE;
    assertThrows(ArithmeticException.class, () -> {
        IntegerAdd(maxInt, 1);
    });
}
```

## Chapter 5: Test Implementation
### Exercise 1: Array Processing
```java
@Test
void testArrayAverage() {
    // Based on AverageArray function
    int[] validArray = {1, 2, 3, 4, 5};
    assertEquals(3, AverageArray(validArray));
    
    assertThrows(IllegalArgumentException.class, () -> {
        AverageArray(null);
    });
}
```

## Chapter 6: Advanced Testing
### Exercise 1: String Manipulation
```java
@Test
void testCharacterCount() {
    // Based on characterCount function
    assertEquals(2, characterCount("t", "test"));
    assertEquals(0, characterCount("x", "test"));
    assertEquals(1, characterCount("e", "test"));
}
```

## Chapter 7: Test Automation
### Exercise 1: Test Suite Organization
```java
@RunWith(Suite.class)
@Suite.SuiteClasses({
    FiltersOperatorsOnIT.class,
    FiltersOperatorsIsNotOneOfIT.class
})
public class AutomatedTestSuite {
    @BeforeClass
    public static void setUp() {
        // Suite initialization
    }
}
```

## Chapter 8: Performance Testing
### Exercise 1: Time-based Testing
```java
@Test
void testPerformance() {
    long startTime = System.currentTimeMillis();
    numberReturn(50); // From example code
    long endTime = System.currentTimeMillis();
    assertTrue("Performance threshold exceeded", 
        (endTime - startTime) < 500);
}
```

## Chapter 9: Security Testing
### Exercise 1: Input Validation
```java
@Test
void testSecureInputValidation() {
    // Based on provided validation patterns
    assertFalse(isValidInput("' OR '1'='1")); // SQL injection
    assertFalse(isValidInput("<script>alert(1)</script>")); // XSS
    assertTrue(isValidInput("normalInput123"));
}
```

## Chapter 10-11: Mobile & DevOps Testing
### Exercise 1: Payment System Testing
```java
@Test
void testPaymentCalculation() {
    // Based on CallGraphExampleForPayment
    float payment = payment(8.0f, 3, 2025L, 1);
    assertTrue(payment > 0);
    assertTrue(daysInAMonth(2, 2025L) == 28);
    assertTrue(isLeap(2024L));
}
```

## Exception Handling Test Cases

### Exercise 1: Number Format Exceptions
```java
@Test
void testNumberFormatExceptions() {
    assertThrows(NumberFormatException.class, () -> {
        Integer.parseInt("XYZ");
    }, "Should throw NumberFormatException");
    
    assertThrows(IllegalArgumentException.class, () -> {
        Integer.parseInt("One");
    });
}
```

### Exercise 2: Arithmetic Exceptions
```java
@Test
void testArithmeticExceptions() {
    // Based on divideNumbers function
    assertThrows(ArithmeticException.class, () -> {
        divideNumbers(10, 0);
    }, "Division by zero should throw exception");
    
    // Test overflow conditions
    assertThrows(ArithmeticException.class, () -> {
        int result = Math.addExact(Integer.MAX_VALUE, 1);
    });
}
```

### Exercise 3: Null Pointer Handling
```java
@Test
void testNullPointerHandling() {
    String test = null;
    assertThrows(NullPointerException.class, () -> {
        test.length();
    });
    
    // Test array handling
    assertThrows(NullPointerException.class, () -> {
        AverageArray(null);
    });
}
```

## Additional Practice Problems
1. **Test Data Generation**
   - Generate test data for boundary value analysis
   - Create equivalence partitions
   - Design decision table test cases

2. **Boundary Value Analysis**

### Exercise 1: Integer Boundaries
```java
@Test
void testIntegerBoundaries() {
    // Based on AverageOfTwoNumbers examples
    double DELTA = 0.01;
    int INTMAX = Integer.MAX_VALUE;
    int INTMIN = Integer.MIN_VALUE;
    
    assertEquals(1073741823.5, AverageOfTwoNumbers(INTMAX, 0), DELTA);
    assertEquals(-1073741824.0, AverageOfTwoNumbers(INTMIN, 0), DELTA);
    assertThrows(ArithmeticException.class, () -> {
        AverageOfTwoNumbers(INTMAX, INTMAX);
    });
}
```

### Exercise 2: Range Validation
```java
@Test
void testRangeValidation() {
    // Based on TriangleAreas function
    assertEquals(-1.0, TriangleAreas(0, 5, 5));    // Below min
    assertEquals(-1.0, TriangleAreas(101, 5, 5));  // Above max
    assertEquals(-1.0, TriangleAreas(5, 5, 11));   // Invalid triangle
    assertTrue(TriangleAreas(3, 4, 5) > 0);       // Valid triangle
}
```

### Exercise 3: Date Boundaries
```java
@Test
void testDateBoundaries() {
    // Based on daysInAMonth function
    assertEquals(31, daysInAMonth(1, 2025L));  // January
    assertEquals(28, daysInAMonth(2, 2025L));  // Non-leap February
    assertEquals(29, daysInAMonth(2, 2024L));  // Leap February
    assertEquals(30, daysInAMonth(4, 2025L));  // April
}
```

## Performance Test Scenarios

### Exercise 1: Response Time Testing
```java
@Test
void testResponseTime() {
    // Based on numberReturn function
    long startTime = System.currentTimeMillis();
    int result = numberReturn(1000);
    long endTime = System.currentTimeMillis();
    
    assertTrue("Response time exceeds threshold",
        (endTime - startTime) < 100); // 100ms threshold
    assertTrue(result > 0);
}
```

### Exercise 2: Concurrent User Testing
```java
@Test
void testConcurrentExecution() {
    int numThreads = 100;
    CountDownLatch latch = new CountDownLatch(numThreads);
    AtomicInteger successCount = new AtomicInteger(0);
    
    for (int i = 0; i < numThreads; i++) {
        new Thread(() -> {
            try {
                numberReturn(10);
                successCount.incrementAndGet();
            } finally {
                latch.countDown();
            }
        }).start();
    }
    
    assertTrue(latch.await(5, TimeUnit.SECONDS));
    assertEquals(numThreads, successCount.get());
}
```

### Exercise 3: Memory Usage Testing
```java
@Test
void testMemoryUsage() {
    Runtime runtime = Runtime.getRuntime();
    long usedMemoryBefore = runtime.totalMemory() - runtime.freeMemory();
    
    // Execute memory-intensive operation
    int[] result = new int[1000000];
    for (int i = 0; i < result.length; i++) {
        result[i] = numberReturn(i % 100);
    }
    
    long usedMemoryAfter = runtime.totalMemory() - runtime.freeMemory();
    long memoryIncrease = usedMemoryAfter - usedMemoryBefore;
    
    assertTrue("Memory usage exceeds threshold",
        memoryIncrease < 10 * 1024 * 1024); // 10MB threshold
}
```

## Integration Test Scenarios

### Exercise 1: Component Integration
```java
@Test
void testPaymentSystemIntegration() {
    // Based on CallGraphExampleForPayment
    float workedHours = 40.0f;
    int month = 3;
    long year = 2025L;
    int titleCode = 1;
    
    float payment = payment(workedHours, month, year, titleCode);
    assertTrue(payment > 0);
    
    int daysInMonth = daysInAMonth(month, year);
    assertEquals(31, daysInMonth);
    
    float factor = findFactor(titleCode, month, year);
    assertTrue(factor >= 1.0);
}
```
