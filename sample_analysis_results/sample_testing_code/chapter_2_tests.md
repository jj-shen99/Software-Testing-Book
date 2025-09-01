# Chapter 2: Testing Fundamentals

## Boundary Value Analysis
```java
@DisplayName("Boundary Value Tests")
class BoundaryValueTests {
    @Test
    void testTriangleAreaBoundaries() {
        // Test minimum valid values
        assertEquals(0.433, TriangleAreas(1, 1, 1), 0.001);
        
        // Test maximum valid values
        assertEquals(-1.0, TriangleAreas(100, 100, 100));
        
        // Test just inside boundaries
        assertEquals(6.0, TriangleAreas(99, 99, 99), 0.1);
        
        // Test just outside boundaries
        assertEquals(-1.0, TriangleAreas(101, 50, 50));
        assertEquals(-1.0, TriangleAreas(0, 50, 50));
    }
}

## Equivalence Partitioning
```java
@DisplayName("Equivalence Partition Tests")
class EquivalencePartitionTests {
    @ParameterizedTest
    @CsvSource({
        "5, 5, 5, 10.825",    // Equilateral triangle
        "3, 4, 5, 6.0",       // Right triangle
        "5, 5, 8, 12.0",      // Isosceles triangle
        "0, 5, 5, -1.0",      // Invalid - zero side
        "101, 5, 5, -1.0",    // Invalid - exceeds max
        "2, 2, 5, -1.0"       // Invalid - not a triangle
    })
    void testTriangleAreaPartitions(int a, int b, int c, double expected) {
        assertEquals(expected, TriangleAreas(a, b, c), 0.001);
    }
}

## Decision Table Testing
```java
@DisplayName("Decision Table Tests")
class DecisionTableTests {
    @Test
    void testColorCodeDecisions() {
        // Test all combinations of conditions
        assertEquals(1, ColorCode(25.0f, 1, 1));  // Hot, sunny, rainy
        assertEquals(2, ColorCode(25.0f, 1, 0));  // Hot, sunny, dry
        assertEquals(3, ColorCode(15.0f, 1, 1));  // Cool, sunny, rainy
        assertEquals(4, ColorCode(15.0f, 1, 0));  // Cool, sunny, dry
        assertEquals(5, ColorCode(25.0f, 0, 1));  // Hot, cloudy, rainy
        assertEquals(6, ColorCode(25.0f, 0, 0));  // Hot, cloudy, dry
        assertEquals(7, ColorCode(15.0f, 0, 1));  // Cool, cloudy, rainy
        assertEquals(4, ColorCode(15.0f, 0, 0));  // Cool, cloudy, dry
    }
}

## State Transition Testing
```java
@DisplayName("State Transition Tests")
class StateTransitionTests {
    @Test
    void testPaymentSystemStates() {
        PaymentSystem system = new PaymentSystem();
        
        // Initial state
        assertEquals(PaymentStatus.INIT, system.getStatus());
        
        // Transition to HOURS_SET
        system.setWorkedHours(40.0f);
        assertEquals(PaymentStatus.HOURS_SET, system.getStatus());
        
        // Transition to CALCULATED
        system.calculatePayment(1, 2025L, 1);
        assertEquals(PaymentStatus.CALCULATED, system.getStatus());
        
        // Transition to ERROR
        system.setWorkedHours(-1.0f);
        assertEquals(PaymentStatus.ERROR, system.getStatus());
        
        // Recovery transition
        system.reset();
        assertEquals(PaymentStatus.INIT, system.getStatus());
    }
}

## Error Guessing
```java
@DisplayName("Error Guessing Tests")
class ErrorGuessingTests {
    @Test
    void testCommonErrors() {
        // Null input
        assertThrows(NullPointerException.class, () -> 
            characterCount(null, "test"));
        
        // Empty string
        assertEquals(0, characterCount("x", ""));
        
        // Special characters
        assertEquals(1, characterCount("$", "te$t"));
        
        // Case sensitivity
        assertEquals(1, characterCount("A", "abc"));
        assertEquals(0, characterCount("a", "ABC"));
    }
}

## Path Testing
```java
@DisplayName("Path Testing Examples")
class PathTestingExamples {
    @Test
    void testNumberReturnPaths() {
        // Test different execution paths
        assertEquals(45, numberReturn(9));    // n < 10 path
        assertEquals(120, numberReturn(11));  // n > 10 path
        assertEquals(0, numberReturn(0));     // boundary path
        assertEquals(1, numberReturn(1));     // minimal path
    }
}
```
