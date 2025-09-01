# Security, Mobile, and DevOps Testing (Chapters 9-11)

## Chapter 9: Security Testing
```java
@DisplayName("Security Testing Examples")
class SecurityTests {
    @Test
    void testInputSanitization() {
        SecurityValidator validator = new SecurityValidator();
        
        // SQL Injection tests
        assertAll("SQL Injection Prevention",
            () -> assertFalse(validator.isValidInput("' OR '1'='1")),
            () -> assertFalse(validator.isValidInput("; DROP TABLE users;")),
            () -> assertFalse(validator.isValidInput("UNION SELECT * FROM passwords"))
        );
        
        // XSS Prevention tests
        assertAll("XSS Prevention",
            () -> assertFalse(validator.isValidInput("<script>alert('xss')</script>")),
            () -> assertFalse(validator.isValidInput("javascript:alert(1)")),
            () -> assertTrue(validator.isValidInput(
                validator.sanitize("<script>alert('xss')</script>")
            ))
        );
    }

    @Test
    void testAuthenticationSecurity() {
        AuthenticationService auth = new AuthenticationService();
        
        // Password security
        assertAll("Password Security",
            () -> assertFalse(auth.isPasswordValid("password")),
            () -> assertFalse(auth.isPasswordValid("12345678")),
            () -> assertTrue(auth.isPasswordValid("P@ssw0rd123!"))
        );
        
        // Brute force prevention
        for (int i = 0; i < 5; i++) {
            auth.login("user", "wrong_password");
        }
        assertThrows(AccountLockedException.class, () ->
            auth.login("user", "correct_password"));
    }
}

## Chapter 10: Mobile Testing
```java
@DisplayName("Mobile Testing Examples")
class MobileTests {
    @Test
    void testResponsiveDesign() {
        MobileTestDriver driver = new MobileTestDriver();
        
        // Test different screen sizes
        assertAll("Responsive Design",
            () -> assertTrue(driver.isResponsive("iPhone X")),
            () -> assertTrue(driver.isResponsive("Pixel 6")),
            () -> assertTrue(driver.isResponsive("Samsung Galaxy Tab"))
        );
    }

    @Test
    void testOfflineCapability() {
        MobileApp app = new MobileApp();
        NetworkSimulator network = new NetworkSimulator();
        
        // Test offline mode
        app.performActions();
        network.setOffline(true);
        
        assertAll("Offline Capability",
            () -> assertTrue(app.isOperational()),
            () -> assertTrue(app.hasOfflineData()),
            () -> assertEquals(5, app.getPendingSync())
        );
        
        // Test sync after reconnection
        network.setOffline(false);
        app.sync();
        assertEquals(0, app.getPendingSync());
    }
}

## Chapter 11: DevOps Testing
```java
@DisplayName("DevOps Testing Examples")
class DevOpsTests {
    @Test
    void testContinuousIntegration() {
        DeploymentPipeline pipeline = new DeploymentPipeline();
        
        // Test build stage
        BuildResult build = pipeline.build();
        assertAll("Build Stage",
            () -> assertTrue(build.isSuccessful()),
            () -> assertTrue(build.getTestsPassed() > 0),
            () -> assertTrue(build.getCodeCoverage() > 80.0)
        );
        
        // Test deployment
        DeploymentResult deploy = pipeline.deploy("staging");
        assertAll("Deployment Stage",
            () -> assertEquals(DeploymentStatus.SUCCESS, deploy.getStatus()),
            () -> assertTrue(deploy.isHealthy()),
            () -> assertTrue(deploy.getUptime() > 0)
        );
    }

    @Test
    void testAutomatedRollback() {
        DeploymentManager manager = new DeploymentManager();
        
        // Deploy with intentional error
        manager.deploy(new DeploymentConfig().withError());
        
        // Verify automatic rollback
        assertAll("Rollback Verification",
            () -> assertEquals(DeploymentStatus.ROLLED_BACK, 
                             manager.getStatus()),
            () -> assertTrue(manager.isRunning()),
            () -> assertEquals(manager.getPreviousVersion(), 
                             manager.getCurrentVersion())
        );
    }

    @Test
    void testMonitoring() {
        MonitoringSystem monitor = new MonitoringSystem();
        
        // Test metrics collection
        MetricsSnapshot metrics = monitor.collectMetrics();
        assertAll("System Metrics",
            () -> assertTrue(metrics.getCPUUsage() < 80),
            () -> assertTrue(metrics.getMemoryUsage() < 90),
            () -> assertTrue(metrics.getDiskSpace() > 20)
        );
        
        // Test alerting
        AlertConfig config = new AlertConfig()
            .setCPUThreshold(90)
            .setMemoryThreshold(85);
        
        monitor.setAlertConfig(config);
        monitor.simulateHighLoad();
        
        assertTrue(monitor.hasActiveAlerts());
    }
}

## Integration Testing in CI/CD
```java
@DisplayName("CI/CD Integration Tests")
class CICDIntegrationTests {
    @Test
    void testDeploymentPipeline() {
        CICDPipeline pipeline = new CICDPipeline();
        
        // Test entire pipeline
        PipelineResult result = pipeline.execute(new PipelineConfig()
            .withStage("build")
            .withStage("test")
            .withStage("deploy")
            .withStage("monitor"));
            
        assertAll("Pipeline Execution",
            () -> assertTrue(result.isSuccessful()),
            () -> assertEquals(4, result.getCompletedStages()),
            () -> assertTrue(result.getDuration() < Duration.ofMinutes(30))
        );
    }
}
```
