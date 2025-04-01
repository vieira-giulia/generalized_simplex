import sys  # Imports the sys module, which is used to handle command-line arguments and interact with the system.

def pivot(tableau, row, col):  # Function to perform the pivoting operation on the tableau given a pivot row and column.
    pivot_element = tableau[row][col]  # The pivot element is the value at the given row and column.
    tableau[row] = [element / pivot_element for element in tableau[row]]  # Divide all elements in the pivot row by the pivot element to normalize it.
    
    # For all other rows, adjust the values to eliminate the value in the pivot column.
    for i in range(len(tableau)):  
        if i != row:  # Skip the pivot row itself.
            ratio = tableau[i][col]  # The ratio is the value in the pivot column of the current row.
            tableau[i] = [tableau[i][j] - ratio * tableau[row][j] for j in range(len(tableau[0]))]  # Update the row values based on the pivot.

def is_infeasible(tableau, n):  # Function to check if the solution is infeasible.
    return any(tableau[i][-1] < 0 for i in range(n))  # If any value in the last column (b_i) is negative, the solution is infeasible.

def simplex(n, m, c, A, b):  # Main function that implements the Simplex method, taking in n (number of constraints), m (number of variables),
                              # c (cost vector), A (constraint matrix), and b (right-hand side vector of constraints).
    tableau = []  # Create a list to store the Simplex tableau.
    
    # Fill the tableau with the constraints and b values.
    for i in range(n):
        # For each row in matrix A, append the coefficients of the variables, slack variables (0's), and the value of b[i].
        tableau.append(A[i] + [0]*n + [b[i]])  # The i-th row of A is concatenated with n zeros (for slack variables) and the value b[i].

    # Add the objective function to the tableau, negating the coefficients of c (since Simplex works with maximization).
    tableau.append([-ci for ci in c] + [0]*n + [0])  # The last row contains the negative coefficients of the objective function, with 0's for slack variables and 0 for the right-hand side.

    # While there are negative values in the last column (indicating infeasibility), continue pivoting.
    while is_infeasible(tableau, n):  # Check if the solution is infeasible.
        row = min(range(n), key=lambda i: tableau[i][-1])  # Select the row with the smallest value in the last column (b[i]).
        col = min(range(m + n), key=lambda j: tableau[row][j] if tableau[row][j] < 0 else float('inf'))  # Select the column with the most negative value.
        
        if tableau[row][col] >= 0:  # If the pivot value in the selected column is greater than or equal to zero, exit the loop.
            break
        pivot(tableau, row, col)  # Perform the pivoting operation on the tableau.

    if any(tableau[i][-1] < 0 for i in range(n)):  # If any value in b[i] is negative after pivoting, the solution is infeasible.
        print("inviavel")  # Print "infeasible" and return, as no feasible solution exists.
        return
    
    tableau.pop()  # Remove the last row (which contains the modified objective function).

    # Add the objective function back to the tableau.
    tableau.append([-ci for ci in c] + [0]*n + [0])  # The objective function is placed back in the last row of the tableau.

    # Loop to find the optimal solution.
    while True:
        col = min(range(len(tableau[0])-1), key=lambda j: tableau[-1][j])  # Select the column with the smallest value in the last row.
        if tableau[-1][col] >= 0:  # If all values in the last row are non-negative, the optimal solution is found.
            break
        
        row = -1  # Initialize the pivot row.
        min_ratio = float('inf')  # Initialize the minimum ratio.
        
        # Find which row has the smallest ratio to select the pivot row.
        for i in range(n):
            if tableau[i][col] > 0:  # Only consider rows that have a positive value in the pivot column.
                ratio = tableau[i][-1] / tableau[i][col]  # Calculate the ratio (last column / value in the pivot column).
                if ratio < min_ratio:  # Update the minimum ratio.
                    min_ratio = ratio
                    row = i  # Set the pivot row.

        if row == -1:  # If no row was found with a positive ratio, the solution is unbounded.
            print("ilimitada")  # Print "unbounded" and return.
            return
        
        pivot(tableau, row, col)  # Perform the pivot operation to optimize the solution.

    # Prepare the final solution, where each variable is associated with the value in the last column.
    solution = [0]*m
    for i in range(n):
        for j in range(m):
            if tableau[i][j] == 1:  # If the value in the tableau is 1 (indicating the variable is in the basis).
                solution[j] = tableau[i][-1]  # Assign the value of b[i] to the corresponding variable.

    print("otima")  # Print "optimal", indicating the optimal solution has been found.
    print(f"{tableau[-1][-1]:.3f}")  # Print the value of the objective function at the optimal solution.
    print(" ".join(f"{x:.3f}" for x in solution))  # Print the values of the decision variables, formatted with 3 decimal places.

    certificate = tableau[-1][m:m+n]  # Extract the certificate of feasibility (the values of the slack variables).
    #print(" ".join(f"{y:.3f}" for y in certificate))  # Optionally, print the certificate (commented out).

if __name__ == "__main__":  # Main block that will be executed when the script is run directly.
    # Read the input file name from the command-line argument.
    input_file = sys.argv[1]
    
    with open(input_file, 'r') as file:  # Open the input file for reading.
        # Read the first line (n and m), which defines the number of constraints and the number of variables.
        n, m = map(int, file.readline().split())
        
        # Read the second line (cost vector c), which contains the coefficients of the objective function.
        c = list(map(float, file.readline().split()))
        
        # Read the next n lines containing the constraints.
        A = []  # List to store the coefficients of the constraints.
        b = []  # List to store the right-hand side values of the constraints.
        for i in range(n):
            line = list(map(float, file.readline().split()))  # Read a row of the constraint matrix.
            A.append(line[:m])  # The first m values are the coefficients of the variables.
            b.append(line[m])  # The last value is the constant b_i.

    # Call the Simplex method with the data read from the file.
    simplex(n, m, c, A, b)
