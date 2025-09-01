# Chapter 1: Introduction to Software Testing

## Basic Test Cases
```java
public class IntroductionTests {
    @Test
    void testAverageCalculation() {
        // Testing the Average function
        assertEquals(2.5, Average(2, 3), 0.01);
        assertEquals(-1.0, Average(11, 3)); // Out of range
        assertEquals(-1.0, Average(-11, 3)); // Out of range
    }

    @Test
    void testMonthValidation() {
        // Testing month number validation
        assertEquals(3, MonthNumber(3));  // Valid month
        assertEquals(-1, MonthNumber(13)); // Invalid month
        assertEquals(-1, MonthNumber(0));  // Invalid month
    }
}
```

## Test Case Design Examples
```java
public class TestDesignExamples {
    @Test
    @DisplayName("Triangle Area Calculation")
    void testTriangleArea() {
        // Valid triangle cases
        assertEquals(6.0, TriangleAreas(3, 4, 5), 0.01);
        assertEquals(43.30, TriangleAreas(10, 10, 10), 0.01);
        
        // Invalid cases
        assertEquals(-1.0, TriangleAreas(1, 1, 3));    // Not a triangle
        assertEquals(-1.0, TriangleAreas(0, 4, 5));    // Invalid side
        assertEquals(-1.0, TriangleAreas(101, 4, 5));  // Out of range
    }

    @Test
    @DisplayName("Integer Addition with Overflow Check")
    void testIntegerAddition() {
        // Normal cases
        assertEquals(5, IntegerAdd(2, 3));
        assertEquals(-5, IntegerAdd(-2, -3));
        
        // Overflow cases
        int maxInt = Integer.MAX_VALUE;
        assertThrows(ArithmeticException.class, () -> 
            IntegerAdd(maxInt, 1));
    }
}
```

## Test Documentation Examples
```java
/**
 * Test Suite for Basic Calculator Functions
 * Demonstrates proper test documentation practices
 */
@DisplayName("Calculator Function Tests")
public class CalculatorTests {
    /**
     * Tests basic arithmetic operations
     * Covers: Addition, Subtraction, Division
     * Includes boundary cases and error conditions
     */
    @Test
    @Tag("basic")
    void testBasicOperations() {
        Calculator calc = new Calculator();
        
        // Addition
        assertEquals(5, calc.add(2, 3));
        
        // Division
        assertEquals(2.0, calc.divide(6, 3), 0.01);
        assertThrows(ArithmeticException.class, () ->
            calc.divide(5, 0));
    }

    /**
     * Tests input validation for calculator functions
     * Verifies proper handling of invalid inputs
     */
    @Test
    @Tag("validation")
    void testInputValidation() {
        Calculator calc = new Calculator();
        
        assertThrows(IllegalArgumentException.class, () ->
            calc.add(Integer.MAX_VALUE, Integer.MAX_VALUE));
    }
}
```

## Test Organization Examples
```java
@Tag("introduction")
public class OrganizationExamples {
    @Nested
    @DisplayName("Input Validation Tests")
    class InputValidationTests {
        @Test
        void testValidInputs() {
            assertTrue(isValidInput("123"));
            assertTrue(isValidInput("abc"));
        }

        @Test
        void testInvalidInputs() {
            assertFalse(isValidInput(""));
            assertFalse(isValidInput(null));
        }
    }

    @Nested
    @DisplayName("Error Handling Tests")
    class ErrorHandlingTests {
        @Test
        void testExceptionHandling() {
            Exception ex = assertThrows(IllegalArgumentException.class,
                () -> processInput(null));
            assertEquals("Input cannot be null", ex.getMessage());
        }
    }
}
```

## Test Execution Examples
```java
public class TestExecutionDemo {
    @BeforeEach
    void setUp() {
        // Initialize test environment
    }

    @Test
    @Order(1)
    void testFirstStep() {
        // First test step
    }

    @Test
    @Order(2)
    void testSecondStep() {
        // Second test step
    }

    @AfterEach
    void tearDown() {
        // Clean up after each test
    }
}
```
