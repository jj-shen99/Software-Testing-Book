import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.mockito.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for BalanceUpdateService using mocking and stubbing techniques
 * Focuses on valid input vectors (valid partition) as requested
 */
public class BalanceUpdateServiceTest {
    
    // System Under Test
    private BalanceUpdateService balanceUpdateService;
    
    // Mock dependency
    @Mock
    private DatabaseInterface mockDbAccess;
    
    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        balanceUpdateService = new BalanceUpdateService(mockDbAccess);
    }
    
    // =================================================================
    // CLASSES UNDER TEST (for completeness)
    // =================================================================
    
    public static class BalanceUpdateService {
        private final DatabaseInterface dbaccess;
        
        public BalanceUpdateService(DatabaseInterface dbaccess) {
            this.dbaccess = dbaccess;
        }
        
        public void UpdateAccountBalance(int customer_id, float deposit) {
            if ((deposit <= 0.0) || (customer_id <= 0)) {
                // error message here
                System.out.println("Invalid input: Customer ID and deposit must be positive");
            } else {
                float balance = dbaccess.getBalance(customer_id);
                dbaccess.updateBalance(customer_id, balance + deposit);
            }
        }
    }
    
    public interface DatabaseInterface {
        public float getBalance(int customer_id);
        public void updateBalance(int customer_id, float balance);
    }
    
    // =================================================================
    // VALID INPUT TEST CASES - BASIC FUNCTIONALITY
    // =================================================================
    
    @Test
    @DisplayName("Valid Input: Small positive deposit to account with zero balance")
    public void testValidDeposit_ZeroBalance_SmallAmount() {
        // Arrange
        int customerId = 1;
        float depositAmount = 10.0f;
        float currentBalance = 0.0f;
        float expectedNewBalance = 10.0f;
        
        // Stub the getBalance method
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert - Verify interactions
        verify(mockDbAccess, times(1)).getBalance(customerId);
        verify(mockDbAccess, times(1)).updateBalance(customerId, expectedNewBalance);
        verifyNoMoreInteractions(mockDbAccess);
    }
    
    @Test
    @DisplayName("Valid Input: Large deposit to account with existing balance")
    public void testValidDeposit_ExistingBalance_LargeAmount() {
        // Arrange
        int customerId = 12345;
        float depositAmount = 5000.50f;
        float currentBalance = 1200.75f;
        float expectedNewBalance = 6201.25f;
        
        // Stub the getBalance method
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert
        verify(mockDbAccess).getBalance(customerId);
        verify(mockDbAccess).updateBalance(customerId, expectedNewBalance);
    }
    
    @Test
    @DisplayName("Valid Input: Minimum valid values (boundary case)")
    public void testValidDeposit_MinimumValidValues() {
        // Arrange - smallest valid positive values
        int customerId = 1; // minimum valid customer ID
        float depositAmount = 0.01f; // minimum valid deposit (just above 0)
        float currentBalance = 0.01f;
        float expectedNewBalance = 0.02f;
        
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert
        verify(mockDbAccess).getBalance(customerId);
        verify(mockDbAccess).updateBalance(customerId, expectedNewBalance);
    }
    
    @Test
    @DisplayName("Valid Input: High customer ID with decimal deposit")
    public void testValidDeposit_HighCustomerId_DecimalAmount() {
        // Arrange
        int customerId = 999999;
        float depositAmount = 123.45f;
        float currentBalance = 876.55f;
        float expectedNewBalance = 1000.00f;
        
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert
        verify(mockDbAccess).getBalance(customerId);
        verify(mockDbAccess).updateBalance(customerId, expectedNewBalance);
    }
    
    // =================================================================
    // VALID INPUT TEST CASES - DIFFERENT BALANCE SCENARIOS
    // =================================================================
    
    @Test
    @DisplayName("Valid Input: Deposit to account with high existing balance")
    public void testValidDeposit_HighExistingBalance() {
        // Arrange
        int customerId = 5678;
        float depositAmount = 250.0f;
        float currentBalance = 50000.0f;
        float expectedNewBalance = 50250.0f;
        
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert
        verify(mockDbAccess).getBalance(customerId);
        verify(mockDbAccess).updateBalance(customerId, expectedNewBalance);
    }
    
    @Test
    @DisplayName("Valid Input: Multiple deposits to same account (different test runs)")
    public void testValidDeposit_MultipleDepositsSimulation() {
        // Test simulates multiple separate deposit transactions
        int customerId = 100;
        
        // First deposit
        float firstDeposit = 100.0f;
        float initialBalance = 500.0f;
        when(mockDbAccess.getBalance(customerId)).thenReturn(initialBalance);
        
        balanceUpdateService.UpdateAccountBalance(customerId, firstDeposit);
        
        verify(mockDbAccess).getBalance(customerId);
        verify(mockDbAccess).updateBalance(customerId, 600.0f);
        
        // Reset mock for second deposit test
        reset(mockDbAccess);
        
        // Second deposit (simulating updated balance from first deposit)
        float secondDeposit = 200.0f;
        float updatedBalance = 600.0f; // Result from first deposit
        when(mockDbAccess.getBalance(customerId)).thenReturn(updatedBalance);
        
        balanceUpdateService.UpdateAccountBalance(customerId, secondDeposit);
        
        verify(mockDbAccess).getBalance(customerId);
        verify(mockDbAccess).updateBalance(customerId, 800.0f);
    }
    
    // =================================================================
    // VALID INPUT TEST CASES - PRECISION AND EDGE CASES
    // =================================================================
    
    @Test
    @DisplayName("Valid Input: Deposit with many decimal places")
    public void testValidDeposit_PrecisionHandling() {
        // Arrange
        int customerId = 777;
        float depositAmount = 99.999f;
        float currentBalance = 0.001f;
        float expectedNewBalance = 100.0f; // Note: float precision limitations
        
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert
        verify(mockDbAccess).getBalance(customerId);
        // Note: Using delta for float comparison due to precision
        ArgumentCaptor<Float> balanceCaptor = ArgumentCaptor.forClass(Float.class);
        verify(mockDbAccess).updateBalance(eq(customerId), balanceCaptor.capture());
        
        float actualBalance = balanceCaptor.getValue();
        assertEquals(expectedNewBalance, actualBalance, 0.001f, 
                    "Balance should be approximately " + expectedNewBalance);
    }
    
    @Test
    @DisplayName("Valid Input: Very small deposit amount")
    public void testValidDeposit_VerySmallAmount() {
        // Arrange
        int customerId = 2;
        float depositAmount = 0.001f;
        float currentBalance = 1000.0f;
        float expectedNewBalance = 1000.001f;
        
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert
        verify(mockDbAccess).getBalance(customerId);
        ArgumentCaptor<Float> balanceCaptor = ArgumentCaptor.forClass(Float.class);
        verify(mockDbAccess).updateBalance(eq(customerId), balanceCaptor.capture());
        
        float actualBalance = balanceCaptor.getValue();
        assertEquals(expectedNewBalance, actualBalance, 0.0001f);
    }
    
    // =================================================================
    // VALID INPUT TEST CASES - INTERACTION VERIFICATION
    // =================================================================
    
    @Test
    @DisplayName("Valid Input: Verify correct sequence of database calls")
    public void testValidDeposit_DatabaseCallSequence() {
        // Arrange
        int customerId = 456;
        float depositAmount = 75.25f;
        float currentBalance = 200.0f;
        
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert - Verify order of calls
        InOrder inOrder = inOrder(mockDbAccess);
        inOrder.verify(mockDbAccess).getBalance(customerId);
        inOrder.verify(mockDbAccess).updateBalance(customerId, 275.25f);
        inOrder.verifyNoMoreInteractions();
    }
    
    @Test
    @DisplayName("Valid Input: Verify exact number of database interactions")
    public void testValidDeposit_ExactInteractionCount() {
        // Arrange
        int customerId = 789;
        float depositAmount = 150.0f;
        float currentBalance = 350.0f;
        
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert - Verify exact interaction counts
        verify(mockDbAccess, times(1)).getBalance(customerId);
        verify(mockDbAccess, times(1)).updateBalance(customerId, 500.0f);
        verify(mockDbAccess, never()).getBalance(not(eq(customerId))); // No other customer queries
        verifyNoMoreInteractions(mockDbAccess);
    }
    
    @Test
    @DisplayName("Valid Input: Verify method parameters are passed correctly")
    public void testValidDeposit_ParameterVerification() {
        // Arrange
        int customerId = 321;
        float depositAmount = 42.42f;
        float currentBalance = 57.58f;
        float expectedNewBalance = 100.0f;
        
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert - Verify parameters using argument captors
        ArgumentCaptor<Integer> customerIdCaptor = ArgumentCaptor.forClass(Integer.class);
        ArgumentCaptor<Float> balanceCaptor = ArgumentCaptor.forClass(Float.class);
        
        verify(mockDbAccess).getBalance(customerIdCaptor.capture());
        verify(mockDbAccess).updateBalance(customerIdCaptor.capture(), balanceCaptor.capture());
        
        // Verify captured values
        assertEquals(customerId, customerIdCaptor.getAllValues().get(0));
        assertEquals(customerId, customerIdCaptor.getAllValues().get(1));
        assertEquals(expectedNewBalance, balanceCaptor.getValue(), 0.001f);
    }
    
    // =================================================================
    // VALID INPUT TEST CASES - STUBBING VARIATIONS
    // =================================================================
    
    @Test
    @DisplayName("Valid Input: Test with different stub return values")
    public void testValidDeposit_DifferentStubValues() {
        // Test 1: Zero balance
        int customerId = 111;
        float deposit1 = 50.0f;
        when(mockDbAccess.getBalance(customerId)).thenReturn(0.0f);
        
        balanceUpdateService.UpdateAccountBalance(customerId, deposit1);
        verify(mockDbAccess).updateBalance(customerId, 50.0f);
        
        // Reset and Test 2: Negative balance (overdraft scenario)
        reset(mockDbAccess);
        float deposit2 = 100.0f;
        when(mockDbAccess.getBalance(customerId)).thenReturn(-25.0f);
        
        balanceUpdateService.UpdateAccountBalance(customerId, deposit2);
        verify(mockDbAccess).updateBalance(customerId, 75.0f);
    }
    
    @Test
    @DisplayName("Valid Input: Test with conditional stubbing")
    public void testValidDeposit_ConditionalStubbing() {
        // Arrange - Different customers have different balances
        when(mockDbAccess.getBalance(1)).thenReturn(100.0f);
        when(mockDbAccess.getBalance(2)).thenReturn(200.0f);
        when(mockDbAccess.getBalance(3)).thenReturn(300.0f);
        
        float depositAmount = 50.0f;
        
        // Act & Assert for customer 1
        balanceUpdateService.UpdateAccountBalance(1, depositAmount);
        verify(mockDbAccess).updateBalance(1, 150.0f);
        
        // Act & Assert for customer 2
        balanceUpdateService.UpdateAccountBalance(2, depositAmount);
        verify(mockDbAccess).updateBalance(2, 250.0f);
        
        // Act & Assert for customer 3
        balanceUpdateService.UpdateAccountBalance(3, depositAmount);
        verify(mockDbAccess).updateBalance(3, 350.0f);
    }
    
    // =================================================================
    // VALID INPUT TEST CASES - BEHAVIOR VERIFICATION
    // =================================================================
    
    @Test
    @DisplayName("Valid Input: Verify no side effects on valid operations")
    public void testValidDeposit_NoSideEffects() {
        // Arrange
        int customerId = 999;
        float depositAmount = 25.0f;
        float currentBalance = 75.0f;
        
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert - Only expected methods should be called
        verify(mockDbAccess, only()).getBalance(customerId);
        verify(mockDbAccess, only()).updateBalance(customerId, 100.0f);
        
        // Verify no unexpected method calls
        verifyNoMoreInteractions(mockDbAccess);
    }
    
    @Test
    @DisplayName("Valid Input: Test service handles normal float arithmetic correctly")
    public void testValidDeposit_FloatArithmeticHandling() {
        // Arrange
        int customerId = 555;
        float depositAmount = 33.33f;
        float currentBalance = 66.67f;
        float expectedNewBalance = 100.0f;
        
        when(mockDbAccess.getBalance(customerId)).thenReturn(currentBalance);
        
        // Act
        balanceUpdateService.UpdateAccountBalance(customerId, depositAmount);
        
        // Assert with tolerance for floating-point arithmetic
        ArgumentCaptor<Float> balanceCaptor = ArgumentCaptor.forClass(Float.class);
        verify(mockDbAccess).updateBalance(eq(customerId), balanceCaptor.capture());
        
        float actualNewBalance = balanceCaptor.getValue();
        assertEquals(expectedNewBalance, actualNewBalance, 0.01f,
                    "Float arithmetic should be handled correctly");
    }
}