# Triangle Area Test Cases

## Unit Tests
```java
@DisplayName("Triangle Area Tests")
class TriangleAreaTests {
    private static final double DELTA = 0.001;

    @Test
    @DisplayName("Valid Triangle Cases")
    void testValidTriangles() {
        assertAll("Valid Triangle Tests",
            () -> assertEquals(6.0, TriangleAreas(3, 4, 5), DELTA),
            () -> assertEquals(43.301, TriangleAreas(10, 10, 10), DELTA),
            () -> assertEquals(12.0, TriangleAreas(5, 5, 6), DELTA)
        );
    }

    @Test
    @DisplayName("Invalid Triangle Cases")
    void testInvalidTriangles() {
        assertAll("Invalid Triangle Tests",
            () -> assertEquals(-1.0, TriangleAreas(1, 1, 3)),
            () -> assertEquals(-1.0, TriangleAreas(0, 4, 5)),
            () -> assertEquals(-1.0, TriangleAreas(101, 50, 50))
        );
    }

    @ParameterizedTest
    @CsvSource({
        "3, 4, 5, 6.0",      // Right triangle
        "5, 5, 5, 10.825",   // Equilateral triangle
        "5, 5, 6, 12.0",     // Isosceles triangle
        "7, 8, 9, 26.833"    // Scalene triangle
    })
    @DisplayName("Triangle Types")
    void testTriangleTypes(int a, int b, int c, double expected) {
        assertEquals(expected, TriangleAreas(a, b, c), DELTA);
    }

    @Test
    @DisplayName("Boundary Value Tests")
    void testBoundaryValues() {
        assertAll("Boundary Tests",
            // Minimum valid values
            () -> assertEquals(0.433, TriangleAreas(1, 1, 1), DELTA),
            
            // Maximum valid values
            () -> assertTrue(TriangleAreas(99, 99, 99) > 0),
            
            // Just outside boundaries
            () -> assertEquals(-1.0, TriangleAreas(101, 50, 50)),
            () -> assertEquals(-1.0, TriangleAreas(0, 50, 50))
        );
    }
}

## Integration Tests
```java
@DisplayName("Triangle Integration Tests")
class TriangleIntegrationTests {
    private GeometryCalculator calculator;
    private ValidationService validator;

    @BeforeEach
    void setUp() {
        calculator = new GeometryCalculator();
        validator = new ValidationService();
    }

    @Test
    @DisplayName("Triangle Area Calculation Flow")
    void testTriangleCalculationFlow() {
        // Input validation
        assertTrue(validator.isValidInput(3, 4, 5));
        assertFalse(validator.isValidInput(0, 4, 5));

        // Area calculation
        double area = calculator.calculateTriangleArea(3, 4, 5);
        assertEquals(6.0, area, 0.001);

        // Result validation
        assertTrue(validator.isValidArea(area));
    }

    @Test
    @DisplayName("Error Handling Flow")
    void testErrorHandlingFlow() {
        // Invalid input handling
        assertThrows(IllegalArgumentException.class, () ->
            calculator.calculateTriangleArea(0, 4, 5));

        // Edge case handling
        assertThrows(IllegalArgumentException.class, () ->
            calculator.calculateTriangleArea(1, 1, 3));
    }
}

## Performance Tests
```java
@DisplayName("Triangle Performance Tests")
class TrianglePerformanceTests {
    private static final int ITERATIONS = 1000000;
    private static final long TIMEOUT_MS = 1000;

    @Test
    @DisplayName("Performance Under Load")
    void testPerformanceUnderLoad() {
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < ITERATIONS; i++) {
            TriangleAreas(3, 4, 5);
        }
        
        long endTime = System.currentTimeMillis();
        long duration = endTime - startTime;
        
        assertTrue(duration < TIMEOUT_MS,
            "Performance test exceeded " + TIMEOUT_MS + "ms");
    }

    @Test
    @DisplayName("Concurrent Execution")
    void testConcurrentExecution() {
        int numThreads = 10;
        CountDownLatch latch = new CountDownLatch(numThreads);
        AtomicInteger successCount = new AtomicInteger(0);
        
        for (int i = 0; i < numThreads; i++) {
            new Thread(() -> {
                try {
                    TriangleAreas(3, 4, 5);
                    successCount.incrementAndGet();
                } finally {
                    latch.countDown();
                }
            }).start();
        }
        
        assertTrue(latch.await(5, TimeUnit.SECONDS));
        assertEquals(numThreads, successCount.get());
    }
}
```
