# State-Based Testing Examples

## Number Processing State Tests
```java
class NumberProcessingTests {
    @Test
    void testNumberReturnStates() {
        // Based on numberReturn function states
        NumberProcessor processor = new NumberProcessor();
        
        // Initial state
        assertEquals(0, processor.getResult());
        
        // State after processing n < 10
        assertEquals(45, processor.numberReturn(9));
        
        // State after processing n > 10
        assertEquals(120, processor.numberReturn(11));
        
        // State transition test
        processor.reset();
        assertEquals(0, processor.getResult());
    }
}
```

## Thread State Tests
```java
class ThreadStateTests {
    @Test
    void testConcurrentStates() {
        // Based on Thread A/B example
        StateManager manager = new StateManager();
        
        // Initial state
        assertEquals(0, manager.getX());
        assertEquals(0, manager.getY());
        
        // State after Thread A execution
        manager.executeThreadA();
        assertEquals(2, manager.getX());
        
        // State after Thread B execution
        manager.executeThreadB();
        assertEquals(2, manager.getY());
        
        // Reset state
        manager.reset();
        assertEquals(0, manager.getX());
        assertEquals(0, manager.getY());
    }
}
```

## Payment System State Tests
```java
class PaymentSystemStateTests {
    @Test
    void testPaymentSystemStates() {
        PaymentSystem system = new PaymentSystem();
        
        // Initial state
        assertEquals(PaymentStatus.INIT, system.getStatus());
        
        // State after setting hours
        system.setWorkedHours(40.0f);
        assertEquals(PaymentStatus.HOURS_SET, system.getStatus());
        
        // State after calculation
        float payment = system.calculatePayment(3, 2025L, 1);
        assertEquals(PaymentStatus.CALCULATED, system.getStatus());
        assertTrue(payment > 0);
        
        // Error state
        system.setWorkedHours(-1.0f);
        assertEquals(PaymentStatus.ERROR, system.getStatus());
    }
}
```

## Filter System State Tests
```java
class FilterSystemStateTests {
    @Test
    void testFilterStates() {
        // Based on FiltersOperatorsOnIT
        FilterSystem filter = new FilterSystem();
        
        // Initial state
        assertTrue(filter.isEmpty());
        
        // State after adding filter
        filter.addFilter("opened_atONToday");
        assertFalse(filter.isEmpty());
        
        // State after applying filter
        List<Record> results = filter.apply();
        assertEquals(FilterStatus.APPLIED, filter.getStatus());
        
        // State after clearing
        filter.clear();
        assertTrue(filter.isEmpty());
        assertEquals(FilterStatus.INIT, filter.getStatus());
    }
}
```

## Error Recovery State Tests
```java
class ErrorRecoveryTests {
    @Test
    void testErrorRecoveryStates() {
        ErrorHandler handler = new ErrorHandler();
        
        // Initial state
        assertEquals(ErrorState.READY, handler.getState());
        
        // Error state
        handler.processError(new ArithmeticException());
        assertEquals(ErrorState.ERROR, handler.getState());
        
        // Recovery state
        handler.recover();
        assertEquals(ErrorState.RECOVERED, handler.getState());
        
        // Reset state
        handler.reset();
        assertEquals(ErrorState.READY, handler.getState());
    }
}
```
