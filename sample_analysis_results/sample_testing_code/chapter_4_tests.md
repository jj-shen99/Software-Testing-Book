# Chapter 4: Test Design

## Data-Driven Testing
```java
@DisplayName("Data-Driven Tests")
class DataDrivenTests {
    @ParameterizedTest
    @CsvSource({
        "40.0, 1, 2025, 1, 2666.67",  // Full time, title 1
        "20.0, 2, 2025, 2, 1000.0",   // Part time, title 2
        "30.0, 4, 2025, 3, 1000.0",   // Regular hours, title 3
        "0.0, 12, 2025, 1, 0.0"       // Zero hours
    })
    void testPaymentCalculations(float hours, int month, 
                               long year, int title, float expected) {
        assertEquals(expected, payment(hours, month, year, title), 0.01);
    }
}

## Combinatorial Testing
```java
@DisplayName("Combinatorial Testing")
class CombinatorialTests {
    @Test
    void testColorCodeCombinations() {
        // Test all combinations of input parameters
        float[] temperatures = {15.0f, 25.0f};
        int[] sunValues = {0, 1};
        int[] rainValues = {0, 1};
        
        Map<String, Integer> expectedResults = Map.of(
            "15.0,0,0", 4,  // Cool, cloudy, dry
            "15.0,0,1", 7,  // Cool, cloudy, rainy
            "15.0,1,0", 4,  // Cool, sunny, dry
            "15.0,1,1", 3,  // Cool, sunny, rainy
            "25.0,0,0", 6,  // Hot, cloudy, dry
            "25.0,0,1", 5,  // Hot, cloudy, rainy
            "25.0,1,0", 2,  // Hot, sunny, dry
            "25.0,1,1", 1   // Hot, sunny, rainy
        );
        
        for (float temp : temperatures) {
            for (int sun : sunValues) {
                for (int rain : rainValues) {
                    String key = String.format("%.1f,%d,%d", temp, sun, rain);
                    assertEquals(expectedResults.get(key), 
                               ColorCode(temp, sun, rain));
                }
            }
        }
    }
}

## State-Based Testing
```java
@DisplayName("State-Based Testing")
class StateBasedTests {
    @Test
    void testPaymentSystemStates() {
        PaymentSystem system = new PaymentSystem();
        
        // Test state transitions
        assertAll(
            () -> assertEquals(PaymentStatus.INIT, system.getStatus()),
            
            () -> {
                system.setWorkedHours(40.0f);
                assertEquals(PaymentStatus.HOURS_SET, system.getStatus());
            },
            
            () -> {
                system.calculatePayment(1, 2025L, 1);
                assertEquals(PaymentStatus.CALCULATED, system.getStatus());
            },
            
            () -> {
                system.processPayment();
                assertEquals(PaymentStatus.PROCESSED, system.getStatus());
            },
            
            () -> {
                system.reset();
                assertEquals(PaymentStatus.INIT, system.getStatus());
            }
        );
    }
}

## Error Recovery Testing
```java
@DisplayName("Error Recovery Testing")
class ErrorRecoveryTests {
    @Test
    void testSystemRecovery() {
        PaymentSystem system = new PaymentSystem();
        
        // Test recovery from invalid input
        assertAll(
            () -> {
                system.setWorkedHours(-1.0f);
                assertEquals(PaymentStatus.ERROR, system.getStatus());
                system.reset();
                assertEquals(PaymentStatus.INIT, system.getStatus());
            },
            
            () -> {
                system.setWorkedHours(168.1f); // More than week hours
                assertEquals(PaymentStatus.ERROR, system.getStatus());
                system.reset();
                assertEquals(PaymentStatus.INIT, system.getStatus());
            }
        );
    }
    
    @Test
    void testDatabaseRecovery() {
        DatabaseService db = new DatabaseService();
        
        // Test transaction rollback
        assertDoesNotThrow(() -> {
            db.beginTransaction();
            try {
                db.executeUpdate("invalid sql");
                fail("Should throw exception");
            } catch (SQLException e) {
                db.rollback();
            }
        });
        
        // Verify system state after recovery
        assertTrue(db.isAvailable());
        assertFalse(db.hasActiveTransaction());
    }
}

## Security Testing
```java
@DisplayName("Security Testing")
class SecurityTests {
    @Test
    void testInputValidation() {
        SecurityValidator validator = new SecurityValidator();
        
        // Test SQL injection prevention
        assertAll(
            () -> assertFalse(validator.isValidInput("' OR '1'='1")),
            () -> assertFalse(validator.isValidInput("; DROP TABLE users;")),
            () -> assertFalse(validator.isValidInput("UNION SELECT * FROM passwords"))
        );
        
        // Test XSS prevention
        assertAll(
            () -> assertFalse(validator.isValidInput("<script>alert('xss')</script>")),
            () -> assertFalse(validator.isValidInput("javascript:alert(1)")),
            () -> assertFalse(validator.isValidInput("<img src=x onerror=alert('xss')>"))
        );
        
        // Test valid inputs
        assertAll(
            () -> assertTrue(validator.isValidInput("John Doe")),
            () -> assertTrue(validator.isValidInput("user@example.com")),
            () -> assertTrue(validator.isValidInput("123-456-7890"))
        );
    }
}
```
