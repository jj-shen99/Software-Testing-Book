# Chapter 3: Testing Methodologies

## Black Box Testing
```java
@DisplayName("Black Box Testing Examples")
class BlackBoxTests {
    @Test
    void testTriangleClassification() {
        // Testing without knowledge of implementation
        Triangle triangle = new Triangle(3, 4, 5);
        assertEquals(TriangleType.RIGHT, triangle.getType());
        
        triangle = new Triangle(5, 5, 5);
        assertEquals(TriangleType.EQUILATERAL, triangle.getType());
        
        triangle = new Triangle(5, 5, 8);
        assertEquals(TriangleType.ISOSCELES, triangle.getType());
        
        assertThrows(IllegalArgumentException.class, () ->
            new Triangle(1, 1, 3));
    }
    
    @ParameterizedTest
    @CsvSource({
        "2025, 2, 28",  // Non-leap year February
        "2024, 2, 29",  // Leap year February
        "2025, 4, 30",  // 30-day month
        "2025, 7, 31"   // 31-day month
    })
    void testDaysInMonth(int year, int month, int expectedDays) {
        assertEquals(expectedDays, daysInAMonth(month, year));
    }
}

## White Box Testing
```java
@DisplayName("White Box Testing Examples")
class WhiteBoxTests {
    @Test
    void testNumberReturnImplementation() {
        // Testing with knowledge of implementation
        int n = 5;
        int result = numberReturn(n);
        
        // Verify internal calculation steps
        int expectedSum = 0;
        for (int i = 1; i <= n; i++) {
            if (n < 10) {
                expectedSum += i;
            }
        }
        assertEquals(expectedSum, result);
    }
    
    @Test
    void testColorCodeBranches() {
        // Testing all code branches
        float temp = 25.0f;
        int sun = 1;
        int rain = 1;
        
        // Test branch: sun == 1 && temp >= 20 && rain == 1
        assertEquals(1, ColorCode(temp, sun, rain));
        
        // Test branch: sun == 1 && temp >= 20 && rain == 0
        assertEquals(2, ColorCode(temp, sun, 0));
        
        // Test all other branches...
    }
}

## Integration Testing
```java
@DisplayName("Integration Testing Examples")
class IntegrationTests {
    @Test
    void testPaymentSystemIntegration() {
        // Test integration between components
        PaymentSystem paymentSystem = new PaymentSystem();
        TimeTracker timeTracker = new TimeTracker();
        PayrollCalculator calculator = new PayrollCalculator();
        
        // Record worked hours
        timeTracker.recordHours(40.0f);
        
        // Calculate payment
        float payment = calculator.calculate(
            timeTracker.getHours(),
            paymentSystem.getTitleCode(),
            paymentSystem.getMonth(),
            paymentSystem.getYear()
        );
        
        assertTrue(payment > 0);
        assertEquals(PaymentStatus.CALCULATED, paymentSystem.getStatus());
    }
}

## System Testing
```java
@DisplayName("System Testing Examples")
class SystemTests {
    @Test
    void testCompleteWorkflow() {
        // Test complete system workflow
        UserSystem userSystem = new UserSystem();
        PaymentSystem paymentSystem = new PaymentSystem();
        ReportingSystem reportSystem = new ReportingSystem();
        
        // User login
        assertTrue(userSystem.login("test_user", "password"));
        
        // Record time
        assertTrue(paymentSystem.recordTime(40.0f));
        
        // Generate report
        Report report = reportSystem.generateReport(
            userSystem.getCurrentUser(),
            paymentSystem.getPaymentDetails()
        );
        
        assertNotNull(report);
        assertEquals("test_user", report.getUserId());
        assertTrue(report.getTotalPayment() > 0);
    }
}

## Performance Testing
```java
@DisplayName("Performance Testing Examples")
class PerformanceTests {
    @Test
    void testResponseTime() {
        PaymentCalculator calculator = new PaymentCalculator();
        
        long startTime = System.currentTimeMillis();
        calculator.calculateBatchPayments(1000); // Calculate for 1000 employees
        long endTime = System.currentTimeMillis();
        
        assertTrue((endTime - startTime) < 5000); // Should complete within 5 seconds
    }
    
    @Test
    void testConcurrentUsers() {
        int numUsers = 100;
        CountDownLatch latch = new CountDownLatch(numUsers);
        AtomicInteger successCount = new AtomicInteger(0);
        
        // Simulate multiple users
        for (int i = 0; i < numUsers; i++) {
            new Thread(() -> {
                try {
                    PaymentSystem system = new PaymentSystem();
                    system.processPayment();
                    successCount.incrementAndGet();
                } finally {
                    latch.countDown();
                }
            }).start();
        }
        
        assertTrue(latch.await(30, TimeUnit.SECONDS));
        assertEquals(numUsers, successCount.get());
    }
}
```
