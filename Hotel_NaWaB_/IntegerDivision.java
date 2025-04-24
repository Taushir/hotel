import java.util.Scanner;

public class IntegerDivision {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        try {
            // Prompt user for input
            System.out.print("Enter the first integer (Num1): ");
            String num1Input = scanner.nextLine();
            System.out.print("Enter the second integer (Num2): ");
            String num2Input = scanner.nextLine();

            // Parse the input numbers
            int num1 = Integer.parseInt(num1Input);
            int num2 = Integer.parseInt(num2Input);

            // Perform division
            int result = num1 / num2;

            // Display the result
            System.out.println("Result: " + result);
        } catch (NumberFormatException e) {
            // Handle non-integer input
            System.out.println("Error: Please enter valid integers.");
        } catch (ArithmeticException e) {
            // Handle division by zero
            System.out.println("Error: Cannot divide by zero.");
        } finally {
            // Close the scanner
            scanner.close();
        }
    }
}