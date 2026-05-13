#include <stdio.h>
#include <stdlib.h>

void rearrangeArray(int* arr, int size) {
    for (int i = 1; i < size; i++) {
        if (*(arr + i) % 2 == 0) {
            int key = *(arr + i);
            int j = i - 1;
            while (j >= 0 && *(arr + j) % 2 != 0) {
                *(arr + j + 1) = *(arr + j);
                j--;
            }
            *(arr + j + 1) = key;
        }
    }
}

int main() {
    int size;
    printf("Enter the size of the array: ");
    scanf("%d", &size);
    int* arr = (int*)malloc(size * sizeof(int));

    printf("Enter %d integers:\n", size);
    for (int i = 0; i < size; i++) {
        printf("Element %d: ", i + 1);
        scanf("%d", arr + i);
    }
    
    rearrangeArray(arr, size);

    printf("Rearranged array: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", *(arr + i));
    }
    printf("\n");
    free(arr);

    return 0;
}