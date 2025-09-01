# Equivalence Partitioning Tests

## Triangle Area Partitions
```java
class TriangleAreaTests {
    @Test
    void testValidEquilateralTriangle() {
        // Partition: All sides equal
        assertEquals(43.30, TriangleAreas(10, 10, 10), 0.01);
    }

    @Test
    void testValidIsoscelesTriangle() {
        // Partition: Two sides equal
        assertEquals(12.0, TriangleAreas(5, 5, 6), 0.01);
    }

    @Test
    void testValidScaleneTriangle() {
        // Partition: No sides equal
        assertEquals(6.0, TriangleAreas(3, 4, 5), 0.01);
    }

    @Test
    void testInvalidSizeBelowRange() {
        // Partition: Size < 1
        assertEquals(-1.0, TriangleAreas(0, 4, 5));
    }

    @Test
    void testInvalidSizeAboveRange() {
        // Partition: Size > 100
        assertEquals(-1.0, TriangleAreas(101, 50, 50));
    }

    @Test
    void testInvalidTriangleInequality() {
        // Partition: Violates triangle inequality
        assertEquals(-1.0, TriangleAreas(2, 2, 5));
    }
}
```

## Color Code Partitions
```java
class ColorCodeTests {
    @Test
    void testHighTemperatureSunnyRainy() {
        // Partition: temp >= 20, sun=1, rain=1
        assertEquals(1, ColorCode(25.0f, 1, 1));
    }

    @Test
    void testHighTemperatureSunnyDry() {
        // Partition: temp >= 20, sun=1, rain=0
        assertEquals(2, ColorCode(25.0f, 1, 0));
    }

    @Test
    void testLowTemperatureSunnyRainy() {
        // Partition: temp < 20, sun=1, rain=1
        assertEquals(3, ColorCode(15.0f, 1, 1));
    }

    @Test
    void testHighTemperatureCloudyRainy() {
        // Partition: temp >= 20, sun=0, rain=1
        assertEquals(5, ColorCode(25.0f, 0, 1));
    }

    @Test
    void testLowTemperatureCloudyDry() {
        // Partition: temp < 20, sun=0, rain=0
        assertEquals(4, ColorCode(15.0f, 0, 0));
    }
}
```

## Payment System Partitions
```java
class PaymentSystemTests {
    @Test
    void testFullTimeHighTitleRegularMonth() {
        // Partition: Full hours, Title=1, 31-day month
        float payment = payment(40.0f, 1, 2025L, 1);
        assertTrue(payment > 2500 && payment < 3000);
    }

    @Test
    void testPartTimeMidTitleShortMonth() {
        // Partition: Part hours, Title=2, 30-day month
        float payment = payment(20.0f, 4, 2025L, 2);
        assertTrue(payment > 1000 && payment < 1500);
    }

    @Test
    void testZeroHoursLowTitleFebruary() {
        // Partition: Zero hours, Title=3, February
        float payment = payment(0.0f, 2, 2025L, 3);
        assertEquals(0.0f, payment, 0.01);
    }

    @Test
    void testOvertimeMidTitleLeapYear() {
        // Partition: Overtime hours, Title=2, Leap year February
        float payment = payment(50.0f, 2, 2024L, 2);
        assertTrue(payment > 3000);
    }
}
```
