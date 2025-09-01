# Concurrency Testing Examples

## Thread Synchronization Tests
```java
class ThreadSynchronizationTests {
    @Test
    void testParallelExecution() {
        // Based on Thread A/B example
        AtomicInteger x = new AtomicInteger(0);
        AtomicInteger y = new AtomicInteger(0);
        CountDownLatch latch = new CountDownLatch(2);
        
        // Thread A
        Thread threadA = new Thread(() -> {
            x.set(0);
            if (y.get() == 1) {
                x.incrementAndGet();
            }
            x.incrementAndGet();
            latch.countDown();
        });
        
        // Thread B
        Thread threadB = new Thread(() -> {
            y.set(0);
            if (x.get() == 1) {
                y.incrementAndGet();
            }
            y.incrementAndGet();
            latch.countDown();
        });
        
        threadA.start();
        threadB.start();
        
        latch.await(1, TimeUnit.SECONDS);
        assertTrue(x.get() >= 1 && x.get() <= 2);
        assertTrue(y.get() >= 1 && y.get() <= 2);
    }
}

## Resource Contention Tests
```java
class ResourceContentionTests {
    @Test
    void testConcurrentResourceAccess() {
        SharedResource resource = new SharedResource();
        int numThreads = 10;
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch endLatch = new CountDownLatch(numThreads);
        
        // Create multiple threads accessing the same resource
        for (int i = 0; i < numThreads; i++) {
            new Thread(() -> {
                try {
                    startLatch.await(); // Synchronize start
                    resource.increment();
                    endLatch.countDown();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }).start();
        }
        
        startLatch.countDown(); // Start all threads
        endLatch.await(2, TimeUnit.SECONDS);
        assertEquals(numThreads, resource.getValue());
    }
}

## Deadlock Detection Tests
```java
class DeadlockTests {
    @Test
    void testDeadlockPrevention() {
        Object resource1 = new Object();
        Object resource2 = new Object();
        DeadlockDetector detector = new DeadlockDetector();
        
        Thread thread1 = new Thread(() -> {
            synchronized(resource1) {
                sleep(100);
                synchronized(resource2) {
                    // Do work
                }
            }
        });
        
        Thread thread2 = new Thread(() -> {
            synchronized(resource2) {
                sleep(100);
                synchronized(resource1) {
                    // Do work
                }
            }
        });
        
        detector.monitor(thread1);
        detector.monitor(thread2);
        
        thread1.start();
        thread2.start();
        
        assertFalse(detector.isDeadlocked(1000));
    }
}

## Race Condition Tests
```java
class RaceConditionTests {
    @Test
    void testRaceConditionPrevention() {
        // Based on numberReturn function
        AtomicInteger result = new AtomicInteger(0);
        CountDownLatch latch = new CountDownLatch(2);
        
        Thread t1 = new Thread(() -> {
            result.addAndGet(numberReturn(5));
            latch.countDown();
        });
        
        Thread t2 = new Thread(() -> {
            result.addAndGet(numberReturn(5));
            latch.countDown();
        });
        
        t1.start();
        t2.start();
        
        latch.await(1, TimeUnit.SECONDS);
        assertEquals(30, result.get()); // Expected sum of both operations
    }
}

## Thread Pool Tests
```java
class ThreadPoolTests {
    @Test
    void testThreadPoolExecution() {
        ExecutorService executor = Executors.newFixedThreadPool(3);
        List<Future<Integer>> results = new ArrayList<>();
        
        // Submit multiple tasks
        for (int i = 0; i < 5; i++) {
            final int taskNum = i;
            results.add(executor.submit(() -> numberReturn(taskNum)));
        }
        
        // Verify all tasks completed
        List<Integer> completedResults = results.stream()
            .map(Future::get)
            .collect(Collectors.toList());
        
        assertEquals(5, completedResults.size());
        assertTrue(completedResults.stream().allMatch(r -> r >= 0));
        
        executor.shutdown();
        assertTrue(executor.awaitTermination(2, TimeUnit.SECONDS));
    }
}
```
