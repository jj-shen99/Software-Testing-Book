# Error Recovery Test Scenarios

## Arithmetic Error Recovery
```java
class ArithmeticErrorTests {
    @Test
    void testDivisionByZeroRecovery() {
        Calculator calc = new Calculator();
        
        try {
            calc.divideNumbers(10, 0);
            fail("Expected ArithmeticException");
        } catch (ArithmeticException e) {
            // Verify error state
            assertEquals("Division by zero!", e.getMessage());
            
            // Test recovery
            double result = calc.divideNumbers(10, 2);
            assertEquals(5.0, result, 0.001);
        }
    }
    
    @Test
    void testOverflowRecovery() {
        // Based on IntegerAdd example
        try {
            int result = Math.addExact(Integer.MAX_VALUE, 1);
            fail("Expected ArithmeticException");
        } catch (ArithmeticException e) {
            // Use BigInteger for recovery
            BigInteger b1 = BigInteger.valueOf(Integer.MAX_VALUE);
            BigInteger b2 = BigInteger.valueOf(1);
            BigInteger sum = b1.add(b2);
            assertTrue(sum.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0);
        }
    }
}

## Input Validation Recovery
```java
class InputValidationTests {
    @Test
    void testTriangleInputRecovery() {
        // Based on TriangleAreas function
        double area;
        
        // Test invalid input recovery
        area = TriangleAreas(0, 5, 5);
        assertEquals(-1.0, area);
        
        // Recovery with valid input
        area = TriangleAreas(3, 4, 5);
        assertEquals(6.0, area, 0.001);
        
        // Test triangle inequality violation recovery
        area = TriangleAreas(1, 1, 3);
        assertEquals(-1.0, area);
        
        // Recovery with valid triangle
        area = TriangleAreas(5, 5, 5);
        assertTrue(area > 0);
    }
}

## Null Reference Recovery
```java
class NullReferenceTests {
    @Test
    void testArrayProcessingRecovery() {
        // Based on AverageArray function
        try {
            AverageArray(null);
            fail("Expected NullPointerException");
        } catch (NullPointerException e) {
            // Recovery with valid array
            int[] validArray = {1, 2, 3, 4, 5};
            int result = AverageArray(validArray);
            assertEquals(3, result);
        }
    }
    
    @Test
    void testStringProcessingRecovery() {
        // Based on characterCount function
        try {
            characterCount(null, "test");
            fail("Expected NullPointerException");
        } catch (NullPointerException e) {
            // Recovery with valid input
            int count = characterCount("t", "test");
            assertEquals(2, count);
        }
    }
}

## System State Recovery
```java
class SystemStateTests {
    @Test
    void testPaymentSystemRecovery() {
        // Based on payment calculation system
        PaymentSystem system = new PaymentSystem();
        
        try {
            // Invalid state
            system.setWorkedHours(-1.0f);
            system.calculatePayment(1, 2025L, 1);
            fail("Expected IllegalStateException");
        } catch (IllegalStateException e) {
            // Verify error state
            assertEquals(PaymentStatus.ERROR, system.getStatus());
            
            // Recovery
            system.reset();
            assertEquals(PaymentStatus.INIT, system.getStatus());
            
            // Valid operation after recovery
            system.setWorkedHours(40.0f);
            float payment = system.calculatePayment(1, 2025L, 1);
            assertTrue(payment > 0);
            assertEquals(PaymentStatus.CALCULATED, system.getStatus());
        }
    }
}

## Resource Cleanup Recovery
```java
class ResourceCleanupTests {
    @Test
    void testResourceCleanupRecovery() {
        Resource resource = new Resource();
        
        try {
            resource.processData(null);
            fail("Expected IllegalArgumentException");
        } catch (IllegalArgumentException e) {
            // Verify resource state
            assertTrue(resource.isInErrorState());
            
            // Cleanup and recovery
            resource.cleanup();
            assertFalse(resource.isInErrorState());
            
            // Valid operation after cleanup
            assertTrue(resource.processData("valid data"));
        } finally {
            resource.close();
        }
    }
}
```
