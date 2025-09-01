import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PrimeNumberTest {

    // Invalid input tests
    @Test
    void testNegativeNumbers() {
        assertFalse(isPrimeNumber(-5));
        assertFalse(isPrimeNumber(-100));
    }
    
    @Test
    void testZero() {
        assertFalse(isPrimeNumber(0));
    }
    
    @Test
    void testOne() {
        assertFalse(isPrimeNumber(1));
    }
    
    // Prime number tests
    @Test
    void testEvenPrime() {
        assertTrue(isPrimeNumber(2));
    }
    
    @Test
    void testSmallOddPrimes() {
        assertTrue(isPrimeNumber(3));
        assertTrue(isPrimeNumber(7));
        assertTrue(isPrimeNumber(97));
    }
    
    @Test
    void testLargePrimes() {
        assertTrue(isPrimeNumber(101));
        assertTrue(isPrimeNumber(997));
        assertTrue(isPrimeNumber(2147483647)); // Integer.MAX_VALUE (prime)
    }
    
    // Composite number tests
    @Test
    void testSmallEvenComposites() {
        // Note: 4 will fail due to bug in implementation
        assertFalse(isPrimeNumber(6));
        assertFalse(isPrimeNumber(96));
    }
    
    @Test
    void testSmallOddComposites() {
        // Note: 9, 25, 49, 121 will fail due to bug in implementation
        assertFalse(isPrimeNumber(15));
        assertFalse(isPrimeNumber(95));
    }
    
    @Test
    void testLargeEvenComposites() {
        assertFalse(isPrimeNumber(100));
        assertFalse(isPrimeNumber(102));
    }
    
    @Test
    void testLargeOddComposites() {
        assertFalse(isPrimeNumber(105));
        assertFalse(isPrimeNumber(1001));
    }
    
    // Special test for perfect squares (will fail due to bug)
    @Test
    void testPerfectSquares() {
        // These tests will fail with current implementation
        // The bug: loop condition should be i <= Math.sqrt(n) instead of i < Math.sqrt(n)
        assertFalse(isPrimeNumber(4), "4 is not prime (2*2)");
        assertFalse(isPrimeNumber(9), "9 is not prime (3*3)");
        assertFalse(isPrimeNumber(25), "25 is not prime (5*5)");
        assertFalse(isPrimeNumber(49), "49 is not prime (7*7)");
        assertFalse(isPrimeNumber(121), "121 is not prime (11*11)");
    }
    
    // Additional test showing the bug explicitly
    @Test
    void testBugWithPerfectSquares() {
        // This test will fail, demonstrating the bug
        String errorMessage = "Bug detected: Perfect squares of primes are incorrectly identified as prime";
        assertAll("Perfect squares test",
            () -> assertFalse(isPrimeNumber(4), errorMessage),
            () -> assertFalse(isPrimeNumber(9), errorMessage),
            () -> assertFalse(isPrimeNumber(25), errorMessage)
        );
    }
    
    // Fixed implementation for reference (not part of the test)
    public static boolean isPrimeNumberFixed(int n) {
        if (n <= 1)
            return false;
        if (n == 2)
            return true;
        if (n % 2 == 0)
            return false;
        
        // Fix: i <= Math.sqrt(n) instead of i < Math.sqrt(n)
        for (int i = 3; i <= Math.sqrt(n); i += 2) {
            if (n % i == 0)
                return false;
        }
        return true;
    }
}
