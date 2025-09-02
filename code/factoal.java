public static Integer Factorial (int n) {
        int c, fact = 1;
        if (n < 0)
            System.out.println("Number should be non-negative.");
        else if (m > 100) {
            System.out.println("Number larger than 100 is not handled by this program.");
        }
        else {
            for (c = 1; c <= n; c++)
                 fact = fact*c;
        }
        return fact;
}