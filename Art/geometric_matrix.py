def create_symmetrical_matrix(size):
    # Create an empty matrix with the specified size
    matrix = [[0 for _ in range(size)] for _ in range(size)]

    # Fill the matrix with symmetrical values
    for i in range(size):
        for j in range(size):
            if i <= j:
                # Set the value of the element at position (i, j) to be the same as the value at position (j, i)
                matrix[i][j] = matrix[j][i]
            else:
                # Set the value of the element at position (i, j) to be the same as the value at position (j, i)
                matrix[i][j] = matrix[j][i]
    return matrix

# Test the function by creating a 5x5 symmetrical matrix
matrix = create_symmetrical_matrix(5)
print(matrix)


