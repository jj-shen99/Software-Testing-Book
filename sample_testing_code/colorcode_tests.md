# ColorCode Function Test Cases

## Decision Table Tests
```java
class ColorCodeDecisionTests {
    @Test
    void testAllCombinations() {
        // Temperature >= 20, Sun = 1, Rain = 1
        assertEquals(1, ColorCode(20.0f, 1, 1));
        
        // Temperature >= 20, Sun = 1, Rain = 0
        assertEquals(2, ColorCode(25.0f, 1, 0));
        
        // Temperature < 20, Sun = 1, Rain = 1
        assertEquals(3, ColorCode(15.0f, 1, 1));
        
        // Temperature < 20, Sun = 1, Rain = 0
        assertEquals(4, ColorCode(18.0f, 1, 0));
        
        // Temperature >= 20, Sun = 0, Rain = 1
        assertEquals(5, ColorCode(22.0f, 0, 1));
        
        // Temperature >= 20, Sun = 0, Rain = 0
        assertEquals(6, ColorCode(21.0f, 0, 0));
        
        // Temperature < 20, Sun = 0, Rain = 1
        assertEquals(7, ColorCode(19.0f, 0, 1));
        
        // Temperature < 20, Sun = 0, Rain = 0
        assertEquals(4, ColorCode(15.0f, 0, 0));
    }
}

## Boundary Tests
```java
class ColorCodeBoundaryTests {
    @Test
    void testTemperatureBoundaries() {
        // At temperature boundary (20.0)
        assertEquals(1, ColorCode(20.0f, 1, 1));
        assertEquals(3, ColorCode(19.99f, 1, 1));
        
        // Extreme temperatures
        assertEquals(1, ColorCode(40.0f, 1, 1));
        assertEquals(3, ColorCode(-10.0f, 1, 1));
    }
    
    @Test
    void testInvalidInputs() {
        // Invalid sun values
        assertThrows(IllegalArgumentException.class, () -> 
            ColorCode(20.0f, 2, 1));
        assertThrows(IllegalArgumentException.class, () -> 
            ColorCode(20.0f, -1, 1));
            
        // Invalid rain values
        assertThrows(IllegalArgumentException.class, () -> 
            ColorCode(20.0f, 1, 2));
        assertThrows(IllegalArgumentException.class, () -> 
            ColorCode(20.0f, 1, -1));
    }
}

## Path Coverage Tests
```java
class ColorCodePathTests {
    @Test
    void testMainPathCoverage() {
        // Test all major decision paths
        
        // Path 1: sun=1 -> temp>=20 -> rain=1
        assertEquals(1, ColorCode(25.0f, 1, 1));
        
        // Path 2: sun=1 -> temp>=20 -> rain=0
        assertEquals(2, ColorCode(25.0f, 1, 0));
        
        // Path 3: sun=1 -> temp<20 -> rain=1
        assertEquals(3, ColorCode(15.0f, 1, 1));
        
        // Path 4: sun=1 -> temp<20 -> rain=0
        assertEquals(4, ColorCode(15.0f, 1, 0));
        
        // Path 5: sun=0 -> temp>=20 -> rain=1
        assertEquals(5, ColorCode(25.0f, 0, 1));
        
        // Path 6: sun=0 -> temp>=20 -> rain=0
        assertEquals(6, ColorCode(25.0f, 0, 0));
        
        // Path 7: sun=0 -> temp<20 -> rain=1
        assertEquals(7, ColorCode(15.0f, 0, 1));
        
        // Path 8: sun=0 -> temp<20 -> rain=0
        assertEquals(4, ColorCode(15.0f, 0, 0));
    }
}

## Integration Tests
```java
class ColorCodeIntegrationTests {
    @Test
    void testWithWeatherSystem() {
        WeatherStation station = new WeatherStation();
        
        // Test with real weather data
        float temp = station.getTemperature();
        int sun = station.isSunny() ? 1 : 0;
        int rain = station.isRaining() ? 1 : 0;
        
        int code = ColorCode(temp, sun, rain);
        assertTrue(code >= 1 && code <= 7);
        
        // Verify code matches weather conditions
        if (temp >= 20 && sun == 1 && rain == 1) {
            assertEquals(1, code);
        } else if (temp < 20 && sun == 0 && rain == 0) {
            assertEquals(4, code);
        }
    }
}
```
