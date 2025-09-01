# Test Organization and Tagging Examples

## Test Suite Structure
```java
@RunWith(Suite.class)
@Suite.SuiteClasses({
    FunctionalTests.class,
    PerformanceTests.class,
    SecurityTests.class
})
public class MasterTestSuite {
    @BeforeClass
    public static void suiteSetUp() {
        // Global setup
    }
}

@Tag("functional")
class FunctionalTests {
    @Test
    @Tag("critical")
    @Tag("P0")
    void testCriticalPath() {
        // Critical functionality test
    }

    @Test
    @Tag("regression")
    void testRegression() {
        // Regression test
    }
}

@Tag("performance")
class PerformanceTests {
    @Test
    @Tag("load")
    void testLoadHandling() {
        // Load test
    }

    @Test
    @Tag("stress")
    void testStressConditions() {
        // Stress test
    }
}
```

## Category-Based Organization
```java
@Category(IntegrationTests.class)
public class PaymentIntegrationTests {
    @Test
    @Tag("smoke")
    void testBasicPaymentFlow() {
        // Basic payment test
    }

    @Test
    @Tag("end-to-end")
    void testCompletePaymentCycle() {
        // Complete cycle test
    }
}

@Category(SecurityTests.class)
public class PaymentSecurityTests {
    @Test
    @Tag("validation")
    void testInputValidation() {
        // Security validation test
    }

    @Test
    @Tag("encryption")
    void testDataEncryption() {
        // Encryption test
    }
}
```

## Priority-Based Organization
```java
public class PriorityBasedTests {
    @Test
    @Tag("P0")
    @Tag("smoke")
    void testCriticalFunctionality() {
        // P0 test case
    }

    @Test
    @Tag("P1")
    @Tag("regression")
    void testCoreFunctionality() {
        // P1 test case
    }

    @Test
    @Tag("P2")
    void testSecondaryFeatures() {
        // P2 test case
    }
}
```

## Feature-Based Organization
```java
@Tag("payment-module")
class PaymentModuleTests {
    @Test
    @Tag("calculation")
    void testPaymentCalculation() {
        // Payment calculation test
    }

    @Test
    @Tag("validation")
    void testPaymentValidation() {
        // Payment validation test
    }
}

@Tag("filter-module")
class FilterModuleTests {
    @Test
    @Tag("operators")
    void testFilterOperators() {
        // Filter operators test
    }

    @Test
    @Tag("performance")
    void testFilterPerformance() {
        // Filter performance test
    }
}
```

## Test Configuration
```java
@Configuration
public class TestConfig {
    @Bean
    public TestExecutionListener performanceListener() {
        return new PerformanceTestListener();
    }

    @Bean
    public TestExecutionListener securityListener() {
        return new SecurityTestListener();
    }
}

class CustomTestExecutor {
    public void executeTests(String[] tags) {
        LauncherDiscoveryRequest request = LauncherDiscoveryRequestBuilder
            .request()
            .selectors(selectPackage("com.example.tests"))
            .filters(TagFilter.includeTags(tags))
            .build();
            
        Launcher launcher = LauncherFactory.create();
        launcher.execute(request);
    }
}
```
