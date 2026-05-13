#include <stdio.h>
#include <stdlib.h>

int keyExistInMatrix(int** matrix, int rows, int cols, int key) {
    int x = 0, y = cols - 1;
    while (x < rows && y >= 0) {
        if (matrix[x][y] == key) 
            return 1;
        else if (matrix[x][y] > key)
            y--;
        else
            x++;
    } 
    return 0;
}

int main() {
    int rows, cols, key;
    printf("Enter the number of rows and columns: ");
    scanf("%d %d", &rows, &cols);
    int** matrix = (int**)malloc(rows * sizeof(int*));
    for (int i = 0; i < rows; i++) {
        matrix[i] = (int*)malloc(cols * sizeof(int));
        printf("Enter row %d: ", i + 1);
        for (int j = 0; j < cols; j++) {
            scanf("%d", &matrix[i][j]);
        }
    }
    printf("Enter the element to search: ");
    scanf("%d", &key);

    if (keyExistInMatrix(matrix, rows, cols, key))
        printf("Element exists in the matrix.\n");
    else
        printf("Element does not exist in the matrix.\n");
    
    for (int i = 0; i < rows; i++)
        free(matrix[i]);

    free(matrix);
    return 0;
}