# Advanced Testing Techniques (Chapters 6-8)

## Chapter 6: Advanced Testing Patterns
```java
@DisplayName("Advanced Testing Patterns")
class AdvancedPatternTests {
    @Test
    void testTransactionRollback() {
        TransactionManager txManager = new TransactionManager();
        
        txManager.begin();
        try {
            performOperations();
            txManager.commit();
        } catch (Exception e) {
            txManager.rollback();
            throw e;
        }
        
        assertFalse(txManager.isActive());
    }

    @Test
    void testCircuitBreaker() {
        CircuitBreaker breaker = new CircuitBreaker(3, 1000);
        RemoteService service = new RemoteService(breaker);
        
        // Test circuit open after failures
        for (int i = 0; i < 3; i++) {
            assertThrows(ServiceException.class, () -> 
                service.call());
        }
        assertEquals(CircuitState.OPEN, breaker.getState());
        
        // Test circuit half-open after timeout
        Thread.sleep(1100);
        assertEquals(CircuitState.HALF_OPEN, breaker.getState());
    }
}

## Chapter 7: Testing Frameworks
```java
@DisplayName("Testing Framework Examples")
class FrameworkTests {
    @Test
    void testCustomTestRunner() {
        TestSuite suite = new TestSuite();
        suite.addTest(new PaymentTest());
        suite.addTest(new ValidationTest());
        
        TestRunner runner = new TestRunner();
        TestResult result = runner.run(suite);
        
        assertTrue(result.wasSuccessful());
        assertEquals(0, result.getFailureCount());
    }

    @Test
    void testCustomAssertions() {
        Payment payment = new Payment(100.0f);
        
        assertThat(payment)
            .hasAmount(100.0f)
            .isProcessed()
            .hasNoErrors();
    }
}

## Chapter 8: Performance Testing
```java
@DisplayName("Performance Testing")
class PerformanceTests {
    @Test
    void testLoadHandling() {
        LoadGenerator generator = new LoadGenerator();
        MetricsCollector metrics = new MetricsCollector();
        
        // Generate load
        generator.generateLoad(100, 60); // 100 users for 60 seconds
        
        PerformanceMetrics results = metrics.getResults();
        assertAll("Performance Metrics",
            () -> assertTrue(results.getAverageResponseTime() < 500),
            () -> assertTrue(results.get95thPercentileTime() < 1000),
            () -> assertTrue(results.getErrorRate() < 0.01)
        );
    }

    @Test
    void testResourceUtilization() {
        ResourceMonitor monitor = new ResourceMonitor();
        PaymentProcessor processor = new PaymentProcessor();
        
        monitor.start();
        processor.processBatch(1000);
        ResourceMetrics metrics = monitor.stop();
        
        assertAll("Resource Utilization",
            () -> assertTrue(metrics.getCpuUsage() < 80),
            () -> assertTrue(metrics.getMemoryUsage() < 512 * 1024 * 1024),
            () -> assertTrue(metrics.getDiskIO() < 1000)
        );
    }

    @Test
    void testScalability() {
        ScalabilityTester tester = new ScalabilityTester();
        
        // Test with increasing load
        Map<Integer, PerformanceMetrics> results = new HashMap<>();
        for (int users = 100; users <= 1000; users += 100) {
            results.put(users, tester.test(users));
        }
        
        // Verify linear scalability
        results.forEach((users, metrics) -> {
            assertTrue(metrics.getThroughput() >= users * 10);
            assertTrue(metrics.getResponseTime() < 1000);
        });
    }
}

## Advanced Monitoring
```java
@DisplayName("Advanced Monitoring Tests")
class MonitoringTests {
    @Test
    void testMetricsCollection() {
        MetricsRegistry registry = new MetricsRegistry();
        
        Timer timer = registry.timer("request.latency");
        Counter requests = registry.counter("request.count");
        Histogram responseSize = registry.histogram("response.size");
        
        // Record metrics
        Timer.Context context = timer.time();
        try {
            requests.inc();
            performRequest();
            responseSize.update(getResponseSize());
        } finally {
            context.stop();
        }
        
        // Verify metrics
        assertAll("Metrics Verification",
            () -> assertTrue(timer.getCount() > 0),
            () -> assertEquals(1, requests.getCount()),
            () -> assertTrue(responseSize.getCount() > 0)
        );
    }
}

## Stress Testing
```java
@DisplayName("Stress Testing Examples")
class StressTests {
    @Test
    void testSystemUnderStress() {
        StressTestRunner runner = new StressTestRunner();
        
        StressTestConfig config = StressTestConfig.builder()
            .setInitialUsers(100)
            .setMaxUsers(1000)
            .setStepSize(100)
            .setStepDuration(Duration.ofMinutes(5))
            .setTargetRPS(1000)
            .build();
            
        StressTestResult result = runner.runTest(config);
        
        assertAll("Stress Test Results",
            () -> assertTrue(result.getMaxThroughput() > 500),
            () -> assertTrue(result.getErrorRate() < 0.05),
            () -> assertTrue(result.getP99ResponseTime() < 2000)
        );
    }
}
```
