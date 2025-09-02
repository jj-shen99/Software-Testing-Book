
public class testaaa {

public static void main (String args[])  {
    System.out.println(" result=: " + Aveage (2, 3) + "\n");
    assert (Aveage (2, 3) == 2.5);
}

public static double Aveage(int x, int y)
 {
    double result = 0.0;
    if (x < -10 || x > 10 || y < -10 || y > 10)
        System.out.println("The parameter values should be an integer between -10 and 10.");
    else 
       result = (x + y) / 2.0;
    return result;
 }

}


public static int MonthNumber (int input) {
    int month = -1;
     if (input > 12 || input < 1) {   
        System.out.println("month value should be between 1 and 12.");
    } 
    else {
        month = input;
    }
    return month;
}


public static double Aveage(int x, int y)
 {
    double result = -1.00;
    if (x < -10 || x > 10 || y < -10 || y > 10)
        System.out.println("The parameter values should be an integer between -10 and 10.");
    else 
       result = (x + y) / 2.0;
    return result;
 }


 public class Triangle
{
    public static void main(String args[])
    {
        double s1, s2, s3, s4, area; 
        Scanner s = new Scanner(System.in);
        System.out.print("Enter the first side :"); 
        s1 = s.nextDouble();
        System.out.print("Enter the second side :"); 
        s2 = s.nextDouble();
        System.out.print("Enter the third side :"); 
        s3 = s.nextDouble();
        s4 = (s1 + s2 + s3 )/ 2 ;
        area = Math.sqrt(s4 * (s4 - s1) * (s4 - s2) * (s4 - s3));
        System.out.print("Area of Triangle is:"+area+" sq units");
    }
}
public static double TriangleAreas (int a, int b, int c) {
    double hp = 0.0;
    double area = -1.0;
    if (a < 1 || a > 100 || b < 1 || b > 100 || c < 1 || c > 100)
        System.out.print("The sizes of the triagle should be a number from 1 to 100. ");
    else if ( ( a >= b + c) || (b >= a + c) || ( c>= a + b) )
        System.out.print("This is not a triagle, any side length should not be bigger than the sum of the other two. ");
    else {
        hp = (a + b + c) / 2.0;
        area = Math.sqrt( hp * (hp - a) * (hp - b) * (hp - c) );
        }
    return area;
}


public static double TriangleAreas (int x, int y, int z) {
    double hp = 0.0;
    double area = -1.0;
    if (x < 1 || x > 100 || y < 1 || y > 100 || z < 1 || z > 100) {
        System.out.print("Out of range: size should be a number from 1 to 100. ");
        return -1;
    }
    else if ( ( x >= y + z) || (y >= x + z) || ( z >= x + y) ) {
        System.out.print("Not a triangle: any side should not be larger than the sum of the other two.");
        return -1;
    }
    else {
        hp = (x + y + z) / 2.0;
        area = Math.sqrt( hp * (hp - x) * (hp - y) * (hp - z) );
        }
    return area;
}



public static int IntegerAdd( int a, int b )
{
     int c = a + b ;
     if ( a >= 0 && b >= 0 && c < 0 )
     {
        System.out.print("Result value overflow!\n");
    } 
    if ( a < 0 && b < 0 && c >= 0 )
     {
        System.out.print("Result value overflow!\n");
    } 
    return c;
}

public static int IntegerAdd(int a, int b)
{
    int c = a + b ;
    if ( a >= 0 && b >= 0 && c < 0 )
        System.out.print("Result value overflow!\n");
    else if ( a < 0 && b < 0 && c >= 0 )
        System.out.print("Result value overflow!\n");
    return c;
}


out = "";
switch(month) {
         case 1 :
         case 2 :
         case 3 :
            out = "Winter";
            break;





public static int ColorCode ( float temperature, int sun, int rain  )
{
    int code = 0;
    if ( sun == 1 )
     {
         if (temperature >= 20 )
         {
             if (rain == 1)
                code = 1;
             else if (rain == 0)
                code = 2;
             else {
                //error handling
             }
         }
         else if (temperature < 20)
          {
             if (rain == 1)
                code = 3;
             else 
                code = 4;
         }  
         else {
             //error handling
         }     
    } 
    else if ( sun == 0 ) 
    {
         if (temperature >= 20 )
         {
             if (rain == 1)
                code = 5;
             else if (rain == 0)
                code = 6;
             else
             {
                //error handling
             }
         }
         else if (temperature < 20)
          {
             if (rain == 1)
                code = 7;
             else 
                code = 4;
         }  
         else {
             //error handling
         }     
    }
    else {
         //error handling
    }
    return code;
}




public static int ColorCode ( float temperature, int sun, int rain  )
{
    int code = 0;
    if ( ( sun == 1) && (temperature >= 20) && (rain == 1) ) 
         code = 1;
    else if ( ( sun == 1) && (temperature >= 20) && (rain == 0) ) 
         code = 2;
    else if ( ( sun == 1) && (temperature < 20) && (rain == 1) ) 
         code = 3;
    else if ( ( sun == 1) && (temperature < 20) && (rain == 0) ) 
         code = 4;
    else if( ( sun == 0) && (temperature >= 20) && (rain == 1) ) 
         code = 5;
    else if ( ( sun == 0) && (temperature >= 20) && (rain == 0) ) 
         code = 6;
    else if ( ( sun == 0) && (temperature < 20) && (rain == 1) ) 
         code = 7;
    else if ( ( sun == 0) && (temperature < 20) && (rain == 1) ) 
         code = 8;
    else {
         //error handling
    }
    return code;
}



// return result"
// 0: reject; 
// 1: 1st priority admissionn consideration with finacial aid consideration. 
// 2: 2nd priority admmission cosideration with no financial aid.
// 3: 3rd prioroty admission consideration with no finacial aid.
public static int initialApplicationCatagorizing( double gpa, int sat, int achievement )
{
    int result = 0;
    if (gpa > 3.5 && sat > 1450 ) {
        result = 3;
        if (achievement == 1 ) {
            result = 2;
            if (gpa >= 4.0 || sat >= 1550) {
                result = 1;
            }
        }
    }
    return result;

public static int numberReturn (int n)
{
    int result = 0;
    for (int i = 1 ; i <= n;  i++) {
        if ( n * n  / i < 10 ) 
            result = 
            break;
    }
    result = i * i;
    return result;
}


public static int squareOfLargeNumber (int n, boolean b)
{
    if (n )
    int result = 0;
    for (int i = 0 ; i <= 100;  i++) {
        if ( m <  ) {
            result = i;
            break;
        }
        result = n * n;
    }
    return result;
}

int r = 0;                                  // 1
for (int i = 0 ; i <= n;  i++) {            // 2
    r = r + i;                              // 3
}                                           // 4

int r = 0;                                  // 1
int i = 0;                                  // 1
while ( i <= n) {                           // 2
    r = r + i;                              // 3
    i++;                                    // 3
}  

int r = 0;          // 1
if ( a > b)         
    r = a - b;      // 2
else
    r = b - a;      // 3
r = r - 1;          // 4


int color = getColor(); 
String colorString = "" ;         //1
switch (color) {
  case 1:
    System.out.println("Blue");     //2
    break;
  case 2:
    System.out.println("Yellow");   //3
    break;
  case 3:
    System.out.println("Red");      //4
    break;
  default:
    System.out.println("White");    //5
}

int color = getColor();       //1
String colorString = "" ;     //1
switch (color) {
  case 1:
    colorString = "Blue";     //2
    break;
  case 2:
    colorString = "Yellow";   //3
    break;
  case 3:
    colorString = "Red";      //4
    break;
  default:
    colorString = "White";    //5
}
System.out.println(colorString); //6


public static int squareOfNumber (int n, int m)
{
    if (m == null) {
        throw new NUllPointerException();
    }
    int result = 0;
    for (int i = 0 ; i <= n;  i++) {
        if ( m < 100 ) {
            result = n * n;
        }
    }
    return result;
}

static Boolean isSquare(int n)
    {
        for (int i = 0; i < n / 2 + 2; i++)
        {
            if (i * i == n)
            {
                return true;
            }
        }
        return false;


public static boolean isPerfectSquare(int n) {
	    int x = n % 10;
	    if (x == 2 || x == 3 || x == 7 || x == 8) {
	         return false;
	    }
	    for (int i = 0; i <= n / 2 + 1; i++) {
	         if ((long) i * i == n) {
	         return true;
	         }
	     }
	     return false;
}



 public static int characterCount (String c, String s) {
     int count = 0;
	    if ( (s == null) || c == null) ) {
	       System.out.println("empty input string.");
	    }
        
	    for (int i = 0; i < s.length(); i++) {
	         if (s.charAt(i) == c.charAt(0) ) {
	            count++;
	         }
	     }
	     return count;
}


public static int AverageArray (int[] a) {
     int result = 0;
	    if ( (a == null) || (a.length == 0) ) {
	       System.out.println("Input array is empty or not specified.");
	    }
	    for (int i = 0; i < a.length; i++) {
	         result = result + a[i];
	    }
        result = result / a.length;
	    return result;
}


public static int reverseNumber (int n) {
     int r = 0;
        while(n != 0) {
            int digit = n % 10;
            r = r * 10 + digit;
            n /= 10;
        }
	    return r;
}

public static int reverseNumber (int x, int y) {
     int r = 0;
        if (x < 0 || y < 0 ) {
            r = x
        }
	    return r;
}




public static int f1(int n) {! if (n % 4 == 0)!
return f2(n / 3, n);! else!
return f3(n);! }!
private static int f2(int a, int b) {! if (a == 0) !
return f3(b);! else!
return f4(a); ! }!
private static int f3(int n) {! if (n == 0)!
return 1;! else !
return n * f3(n - 1);! }!
private static int f4(int n) {! return n * n + 1;!
}

public class CallGraphExampleForPayment {
   public static float payment (float workedHours, int month, long year, int titleCode) {
    float result = 0;
    float factor = findFactor (titleCode, month, year);
    result = workedHours * factor * 1000 / daysInAMonth (month, year);
    retutn result;
   }
   public static int daysInAMonth (int month, long year) {
    int result = 0;
    if (month == 4 || month == 6 || month == 9 || month == 11)
        result = 30;
    else if (month == 2) 
        result = (isLeap(year)) ? 29 : 28;
    else
        result = 31;
    return result;
   }

   public static boolean isLeap(long year) {
    return ((year & 3) == 0) && ((year % 100) != 0 || (year % 400) == 0);
   }

   private static float findFactor (int titleCode, int month, long year) {
    float factor = 1.0;
    if titleCode == 1 
        factor = 2.0;
    else if titleCode == 2
        factor = 1.5;
    else 
        factor = 1.0 * daysInAMonth(month, year) / 30;
   }
}

@Test
public void testPassword (String inputPass) {
    Assert.assertEquals(inputPass, checkPassword (inputPass));   
}


public int checkPassword(String password) ()

@Test
public void testAverage () {
    Assert.assertEquals(4, average (3, 5) );   
}

Function A {
      	 	Call function C;
       		//Do some work;
}
Function B {
      		Call function C;
      		//Do some work;
}
Function C {
      		Call Function X; 
      		// Function X is a build-in function in the programing language;
      		//Do some work;
}

Thread A:
    x = 0;
	if (y == 1) 
	    x++;
	x++;
Thread B:
 	y = 0;
	if (x==1)
	    y++;
	y++;


public class AnExampleTest (){
    @Test
    @Tag("Sanity")
    @Tag("P2")
    @Tag("Freq_failed")
    @Tag("Large_n_users")
    @Category(OracleTests.class)
    void testCase1() {
    }
    @Test
    @Tag("Critical")
    @Tag("P0")
     @Tag("Smoke")
    @Category(OracleTests.class)
    void testCase2() {
    }
}


public class ExampleTests (){
    @Test
    void testCaseBase() {
        assertEquals(Average (10, 0), 5);


    }
    @Test
    void testCase2() {
    }
}


public static double Average(int x, int y)
 {
    double result = -1.00;
    if (x < -10 || x > 10 || y < -10 || y > 10)
        System.out.println("The parameter values should be an integer between -10 and 10.");
    else 
       result = (x + y) / 2.0;
    return result;
 }


(i)	{ [10, 0], [9, 1], [0, 9], [-1,10], [-10, 2], [-9,-2],[ 0, -10], [3,-9] ,[0,0] }
(ii)	{ [-11, 0], [-100, -2] }
(iii)	{ [11, 1], [99, 4] }
(iv)	{ [1, -11], [-1, -99] }
(v)	{ [0, 11], [5, 111] }



@Test
void testUserValidCase1() {
    String user_id = "test_user_01";
    int start_time = 1546304460;
    int end_time = 1567533483;
    String order_status = "Open";

    int expected_num_user_02_case1 = getNumberOfRecordsFromDBInteface (start_time, end_time, user_id, order_status);

    String APIReturn = getAPIReturn(start_time, end_time, user_id, order_status);
    int record_num = NumberOfRecordInAPIReturn (APIReturn);
    Assert.assertEquals ("Number of record does not match for expected_num_user_02_case1.", expected_num_user_02_case1), record_num );
    NodeList userTagList = APIReturn.getElementsByTagName("user");
    for (int i = 0; i < userTagList.getLength(); i++ ) {
        Node node = userTagList.item(i);
        if (node.GetNodeType() == Node.ELEMENT_NODE) {
            String tagValue = node.getTextContent();
            Assert.assertEquals ("User tag value does not match for user " + user_id + ".", user_id, tagValue) );
        }
    }
}

Test
void testUserValidCase1() {
    String user_id = "test_user_01";
    int start_time = 1546304460;
    int end_time = 1567533483;
    String order_status = "Open";

int expected_num_user_case1 = getNumberOfRecordsFromDBInteface (start_time, end_time, user_id,
                         order_status);

    String APIReturn = getAPIReturn(start_time, end_time, user_id, order_status);
    int record_num = NumberOfRecordInAPIReturn (APIReturn);
Assert.assertEquals ("Number of records does not match for user_case1.", 
                      expected_num_user_case1), record_num);

    NodeList userTagList = APIReturn.getElementsByTagName("user");
    for (int i = 0; i < userTagList.getLength(); i++ ) {
        Node node = userTagList.item(i);
        if (node.GetNodeType() == Node.ELEMENT_NODE) {
            Assert.assertEquals ("User tag value does not match for user " + user_id + ".", user_id,
                                 node.getTextContent() );
        }
    }
}




 int a = Integer.MAX_VALUE; 
    int b = Integer.MAX_VALUE;


    (a / 2) + (b / 2) + 
           ((a % 2 + b % 2) / 2);



public static double AverageOfTwoNumbers(int x, int y)
 {
    double result = -1.00;
       result =  (x / 2) + (x / 2) + ((x % 2 + x % 2) / 2);
    return result;
 }

 public void testAverageOfTwoNumbersOutOfBound (int a, int b) {
     assertAverageOfTwoNumbers (a,b);
 }

 public void assertAverageOfTwoNumbers (int a, int b) {
     assertTrue ()
 }


 package com.howtodoinjava.junit5.examples.module;
 
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
 
public class AppTest {

    int a = Integer.MAX_VALUE; 
    int b = Integer.MAX_VALUE;
 
   @Test
   void testExpectedException() {
 
    Assertions.assertThrows(NumberFormatException.class, () -> {
      Integer.parseInt("One");
    });
  }
 
  @Test
  void testExpectedExceptionWithSuperType() {
 
    Assertions.assertThrows(IllegalArgumentException.class, () -> {
      Integer.parseInt("One");
    });
  }
   
  @Test
  void testExpectedExceptionFail() {
 
    Assertions.assertThrows(IllegalArgumentException.class, () -> {
      Integer.parseInt("1");
    });
  }
 
}

public static double AverageOfTwoNumbers(int x, int y)
 {
    double result = -1.00;
       result =  (x / 2) + (x / 2) + ((x % 2 + x % 2) / 2);
    return result;
 }

public class TestAverageOfTwoNumbners {
    private static final double DELTA = 0.01;
    @Test
    void testAverageOfTwoNumbersValidNormalCase() {
        assert.assertEquals (0, AverageOfTwoNumbers(0,0));
    }
    @Test
    void testAverageOfTwoNumbersValidBoundaryCase() {
        assert.assertEquals (0, AverageOfTwoNumbers(Integer.MAX_VALUE,0), DELTA);
    }

}


public class OverflowExample3 {

    public static void main(String[] args) {
        int i = 2000000000;
        int j = 1000000000;

        try {
            int out = Math.addExact(i, j);
            System.out.println(out);
        }catch (ArithmeticException e){
            BigInteger b1 = BigInteger.valueOf(i);
            BigInteger b2 = BigInteger.valueOf(j);
            BigInteger output = b1.add(b2);
            System.out.println(output);
        }
    }
}

@Test
	void assertThrowsWithExecutableThatThrowsThrowableWithMessageSupplier() {
		EnigmaThrowable enigmaThrowable = assertThrows(EnigmaThrowable.class, (Executable) () -> {
			throw new EnigmaThrowable();
		}, () -> "message");
		assertNotNull(enigmaThrowable);
	}

	@Test
	void assertThrowsWithExecutableThatThrowsCheckedException() {
		IOException exception = assertThrows(IOException.class, (Executable) () -> {
			throw new IOException();
		});
		assertNotNull(exception);
	}

	@Test
	void assertThrowsWithExecutableThatThrowsRuntimeException() {
		IllegalStateException illegalStateException = assertThrows(IllegalStateException.class, (Executable) () -> {
			throw new IllegalStateException();
		});
		assertNotNull(illegalStateException);
	}

	@Test
	void assertThrowsWithExecutableThatThrowsError() {
		StackOverflowError stackOverflowError = assertThrows(StackOverflowError.class,
			(Executable) AssertionTestUtils::recurseIndefinitely);
		assertNotNull(stackOverflowError);
	}

	@Test
	void assertThrowsWithExecutableThatDoesNotThrowAnException() {
		try {
			assertThrows(IllegalStateException.class, nix);
			expectAssertionFailedError();
		}
		catch (AssertionFailedError ex) {
			assertMessageEquals(ex, "Expected java.lang.IllegalStateException to be thrown, but nothing was thrown.");
		}
	}

	@Test
	void assertThrowsWithExecutableThatDoesNotThrowAnExceptionWithMessageString() {
		try {
			assertThrows(IOException.class, nix, "Custom message");
			expectAssertionFailedError();
		}
		catch (AssertionError ex) {
			assertMessageEquals(ex,
				"Custom message ==> Expected java.io.IOException to be thrown, but nothing was thrown.");
		}
	}

	@Test
	void assertThrowsWithExecutableThatDoesNotThrowAnExceptionWithMessageSupplier() {
		try {
			assertThrows(IOException.class, nix, () -> "Custom message");
			expectAssertionFailedError();
		}
		catch (AssertionError ex) {
			assertMessageEquals(ex,
				"Custom message ==> Expected java.io.IOException to be thrown, but nothing was thrown.");
		}
	}

	@Test
	void assertThrowsWithExecutableThatThrowsAnUnexpectedException() {
		try {
			assertThrows(IllegalStateException.class, (Executable) () -> {
				throw new NumberFormatException();
			});
			expectAssertionFailedError();
		}
		catch (AssertionFailedError ex) {
			assertMessageStartsWith(ex, "Unexpected exception type thrown ==> ");
			assertMessageContains(ex, "expected: <java.lang.IllegalStateException>");
			assertMessageContains(ex, "but was: <java.lang.NumberFormatException>");
		}
	}

	@Test
	void assertThrowsWithExecutableThatThrowsAnUnexpectedExceptionWithMessageString() {
		try {
			assertThrows(IllegalStateException.class, (Executable) () -> {
				throw new NumberFormatException();
			}, "Custom message");
			expectAssertionFailedError();
		}
		catch (AssertionFailedError ex) {
			// Should look something like this:
			// Custom message ==> Unexpected exception type thrown ==> expected: <java.lang.IllegalStateException> but was: <java.lang.NumberFormatException>
			assertMessageStartsWith(ex, "Custom message ==> ");
			assertMessageContains(ex, "Unexpected exception type thrown ==> ");
			assertMessageContains(ex, "expected: <java.lang.IllegalStateException>");
			assertMessageContains(ex, "but was: <java.lang.NumberFormatException>");
		}
	}

	@Test
	void assertThrowsWithExecutableThatThrowsAnUnexpectedExceptionWithMessageSupplier() {
		try {
			assertThrows(IllegalStateException.class, (Executable) () -> {
				throw new NumberFormatException();
			}, () -> "Custom message");
			expectAssertionFailedError();
		}
		catch (AssertionFailedError ex) {
			// Should look something like this:
			// Custom message ==> Unexpected exception type thrown ==> expected: <java.lang.IllegalStateException> but was: <java.lang.NumberFormatException>
			assertMessageStartsWith(ex, "Custom message ==> ");
			assertMessageContains(ex, "Unexpected exception type thrown ==> ");
			assertMessageContains(ex, "expected: <java.lang.IllegalStateException>");
			assertMessageContains(ex, "but was: <java.lang.NumberFormatException>");
		}
	}


      try{
	 int num=Integer.parseInt ("XYZ") ;
	 System.out.println(num);
      }catch(NumberFormatException e){
	  System.out.println("Number format exception occurred");
       }


       @Test
public void whenExceptionThrown_thenAssertionSucceeds() {
    String test = null;
    assertThrows(NullPointerException.class, () -> {
        test.length();
    });
}



public class Type0TestsForAverageOfTwoNumbersInvalidPartitions () {
   public static final int INTMAX = Integer.MAX_VALUE;
   public static final int INTMIN = Integer.MIN_VALUE;

   @Test
   public void testAverageOfTwoNumbersValidPartitionValuesINTMAXandZero() {
     assert.assertEquals (1073741823.5, AverageOfTwoNumbers(INTMAX, 0), DELTA);
   }
   @Test
   public void testAverageOfTwoNumbersValidPartitionValuesINTMAXminusOneAndOne() {
     assert.assertEquals (1073741823.5, AverageOfTwoNumbers(INTMAX-1, 1), DELTA);
   }
}


@Test
public void whenDerivedExceptionThrown_thenAssertionSucceds() {
    String test = null;
    assertThrows(RuntimeException.class, () -> {
        test.length();
    });
}

 public static double divideNumbers(double dividend, double divisor) {
        if (divisor == 0) {
            throw new ArithmeticException("Division by zero!");
        }
        return dividend / divisor;
    }

    
public void test_isPrime_inputValue5 () {
   int input = 5;
   try {
      if (AverageOfTwoNumbers(1,1) == 1) 
        System.out.println (“test passed: “ + input + “ is a prime number.”);
      else {
        Throw new AssetionError(“test failed: “ + input + “ should be a prime number.”);
        }
Catch (AssertionError e) {
    System.out.println ( e.getMesssage() );
}      
}


public static int numberReturn (int n)
{
    int result = 0;
    for (int i = 1 ; i <= n;  i++) {
        if ( n  < 10 ) {
            result = result + i;
            break;
        }
        result = result + i + n;
    }
    return result;
}

public static int numberReturn (int n)
{
    int result = 0;
    while (n > 0 ) {
        n--;
        if ( n  < 10 ) {
            result = result + n;
            break;
        }
        result = result + n * n;
    }
    return result;
}