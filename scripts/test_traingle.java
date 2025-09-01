import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Comprehensive test suite for the isRightTriangle method
 * Using multiple testing techniques from JJ Shen's Software Testing book
 */
public class RightTriangleTest {
    
    // The method under test
    public static boolean isRightTriangle(int a, int b, int c) {
        if ((a <= 0) || (b <= 0) || (c <= 0)) {
            System.out.println("All sides are positive numbers.");
            return false;
        }
        return (Math.pow(a, 2) + Math.pow(b, 2) == Math.pow(c, 2)) ||
               (Math.pow(a, 2) + Math.pow(c, 2) == Math.pow(b, 2)) ||
               (Math.pow(c, 2) + Math.pow(b, 2) == Math.pow(a, 2));
    }

    // =================================================================
    // EQUIVALENCE PARTITIONING TEST CASES
    // =================================================================
    
    @Test
    @DisplayName("EP1: Valid right triangle - Classic 3-4-5")
    public void testValidRightTriangle_3_4_5() {
        assertTrue(isRightTriangle(3, 4, 5));
        assertTrue(isRightTriangle(4, 3, 5));
        assertTrue(isRightTriangle(5, 3, 4));
    }
    
    @Test
    @DisplayName("EP2: Valid right triangle - Scaled Pythagorean triple")
    public void testValidRightTriangle_6_8_10() {
        assertTrue(isRightTriangle(6, 8, 10));
        assertTrue(isRightTriangle(8, 6, 10));
        assertTrue(isRightTriangle(10, 6, 8));
    }
    
    @Test
    @DisplayName("EP3: Valid right triangle - 5-12-13")
    public void testValidRightTriangle_5_12_13() {
        assertTrue(isRightTriangle(5, 12, 13));
        assertTrue(isRightTriangle(12, 5, 13));
        assertTrue(isRightTriangle(13, 5, 12));
    }
    
    @Test
    @DisplayName("EP4: Invalid triangle - Not a right triangle")
    public void testInvalidRightTriangle() {
        assertFalse(isRightTriangle(2, 3, 4));
        assertFalse(isRightTriangle(1, 2, 3));
        assertFalse(isRightTriangle(7, 8, 9));
    }
    
    @Test
    @DisplayName("EP5: Invalid input - Negative sides")
    public void testNegativeSides() {
        assertFalse(isRightTriangle(-3, 4, 5));
        assertFalse(isRightTriangle(3, -4, 5));
        assertFalse(isRightTriangle(3, 4, -5));
        assertFalse(isRightTriangle(-3, -4, -5));
    }
    
    @Test
    @DisplayName("EP6: Invalid input - Zero sides")
    public void testZeroSides() {
        assertFalse(isRightTriangle(0, 4, 5));
        assertFalse(isRightTriangle(3, 0, 5));
        assertFalse(isRightTriangle(3, 4, 0));
        assertFalse(isRightTriangle(0, 0, 0));
    }

    // =================================================================
    // BOUNDARY VALUE ANALYSIS TEST CASES
    // =================================================================
    
    @Test
    @DisplayName("BVA1: Minimum valid values")
    public void testMinimumValidValues() {
        // Smallest Pythagorean triple with positive integers
        assertFalse(isRightTriangle(1, 1, 1)); // Not a right triangle
        assertTrue(isRightTriangle(3, 4, 5));   // Smallest right triangle
    }
    
    @Test
    @DisplayName("BVA2: Boundary around zero")
    public void testBoundaryAroundZero() {
        assertFalse(isRightTriangle(0, 1, 1));   // Zero boundary
        assertFalse(isRightTriangle(1, 0, 1));   // Zero boundary
        assertFalse(isRightTriangle(1, 1, 0));   // Zero boundary
        assertFalse(isRightTriangle(-1, 1, 1));  // Just below zero
        assertFalse(isRightTriangle(1, -1, 1));  // Just below zero
        assertFalse(isRightTriangle(1, 1, -1));  // Just below zero
    }
    
    @Test
    @DisplayName("BVA3: Large values")
    public void testLargeValues() {
        // Test with larger Pythagorean triples to check for overflow issues
        assertTrue(isRightTriangle(20, 21, 29));  // 20² + 21² = 29²
        assertTrue(isRightTriangle(119, 120, 169)); // 119² + 120² = 169²
    }

    // =================================================================
    // DECISION TABLE TESTING
    // =================================================================
    
    @Test
    @DisplayName("DT1: All conditions for right triangle validation")
    public void testDecisionTableCombinations() {
        // Condition 1: All sides positive
        // Condition 2: Pythagorean theorem satisfied
        
        // C1=T, C2=T: Valid right triangle
        assertTrue(isRightTriangle(3, 4, 5));
        
        // C1=T, C2=F: Valid sides but not right triangle
        assertFalse(isRightTriangle(2, 3, 4));
        
        // C1=F, C2=*: Invalid sides (negative or zero)
        assertFalse(isRightTriangle(-3, 4, 5));
        assertFalse(isRightTriangle(0, 4, 5));
    }

    // =================================================================
    // PAIRWISE TESTING
    // =================================================================
    
    @Test
    @DisplayName("PW1: Parameter ordering combinations")
    public void testParameterOrderingCombinations() {
        // Test all permutations of the same right triangle
        int[] sides = {3, 4, 5};
        
        // All 6 permutations should return true
        assertTrue(isRightTriangle(3, 4, 5));
        assertTrue(isRightTriangle(3, 5, 4));
        assertTrue(isRightTriangle(4, 3, 5));
        assertTrue(isRightTriangle(4, 5, 3));
        assertTrue(isRightTriangle(5, 3, 4));
        assertTrue(isRightTriangle(5, 4, 3));
    }

    // =================================================================
    // SPECIAL CASES AND EDGE CASES
    // =================================================================
    
    @Test
    @DisplayName("SC1: Equal sides (not right triangles)")
    public void testEqualSides() {
        assertFalse(isRightTriangle(1, 1, 1));
        assertFalse(isRightTriangle(5, 5, 5));
        assertFalse(isRightTriangle(10, 10, 10));
    }
    
    @Test
    @DisplayName("SC2: Two equal sides")
    public void testTwoEqualSides() {
        // Isosceles right triangle (45-45-90)
        assertFalse(isRightTriangle(1, 1, 2)); // Close but not exact due to sqrt(2)
        
        // Other isosceles triangles
        assertFalse(isRightTriangle(5, 5, 7));
        assertFalse(isRightTriangle(3, 8, 8));
    }
    
    @Test
    @DisplayName("SC3: Degenerate cases")
    public void testDegenerateCases() {
        // Triangle inequality violations
        assertFalse(isRightTriangle(1, 2, 10)); // Sum of two sides < third side
        assertFalse(isRightTriangle(1, 1, 3));  // Sum of two sides < third side
    }

    // =================================================================
    // PRECISION AND FLOATING-POINT ISSUES
    // =================================================================
    
    @Test
    @DisplayName("FP1: Integer precision test")
    public void testIntegerPrecision() {
        // These should work fine with integers
        assertTrue(isRightTriangle(8, 15, 17));   // 8² + 15² = 17²
        assertTrue(isRightTriangle(7, 24, 25));   // 7² + 24² = 25²
        assertTrue(isRightTriangle(9, 40, 41));   // 9² + 40² = 41²
    }
    
    @Test
    @DisplayName("FP2: Near-miss cases")
    public void testNearMissCases() {
        // These are close to right triangles but not exact
        assertFalse(isRightTriangle(3, 4, 6));   // Close but not 5
        assertFalse(isRightTriangle(5, 12, 14)); // Close but not 13
    }

    // =================================================================
    // REGRESSION TESTS
    // =================================================================
    
    @Test
    @DisplayName("REG1: Known Pythagorean triples")
    public void testKnownPythagoreanTriples() {
        // Primitive Pythagorean triples
        assertTrue(isRightTriangle(3, 4, 5));
        assertTrue(isRightTriangle(5, 12, 13));
        assertTrue(isRightTriangle(8, 15, 17));
        assertTrue(isRightTriangle(7, 24, 25));
        assertTrue(isRightTriangle(20, 21, 29));
        assertTrue(isRightTriangle(12, 35, 37));
        assertTrue(isRightTriangle(9, 40, 41));
        assertTrue(isRightTriangle(28, 45, 53));
        assertTrue(isRightTriangle(11, 60, 61));
        assertTrue(isRightTriangle(16, 63, 65));
    }
    
    @Test
    @DisplayName("REG2: Scaled Pythagorean triples")
    public void testScaledPythagoreanTriples() {
        // Multiples of primitive triples
        assertTrue(isRightTriangle(6, 8, 10));    // 2 * (3,4,5)
        assertTrue(isRightTriangle(9, 12, 15));   // 3 * (3,4,5)
        assertTrue(isRightTriangle(15, 20, 25));  // 5 * (3,4,5)
        assertTrue(isRightTriangle(10, 24, 26));  // 2 * (5,12,13)
    }

    // =================================================================
    // ERROR CONDITION TESTS
    // =================================================================
    
    @Test
    @DisplayName("ERR1: Multiple invalid conditions")
    public void testMultipleInvalidConditions() {
        // Multiple negative values
        assertFalse(isRightTriangle(-3, -4, 5));
        assertFalse(isRightTriangle(-3, 4, -5));
        assertFalse(isRightTriangle(-3, -4, -5));
        
        // Mix of zero and negative
        assertFalse(isRightTriangle(0, -4, 5));
        assertFalse(isRightTriangle(-3, 0, 5));
    }
    
    // =================================================================
    // PERFORMANCE AND STRESS TESTS
    // =================================================================
    
    @Test
    @DisplayName("PERF1: Large number stress test")
    public void testLargeNumbers() {
        // Test with large integers to check for potential overflow
        assertTrue(isRightTriangle(300, 400, 500));   // Large 3-4-5 triangle
        assertTrue(isRightTriangle(500, 1200, 1300)); // Large 5-12-13 triangle
    }
}
