/* Command to create shared library
gcc -o test.so -shared -fPIC test.c */

# include <stdio.h>
# include <stdlib.h>

int init(int n)
{
    return n;
}

char* hello(char *what)
{
    printf("Hello \"%s\" from inside the c function!\n", what);
    return what;
}

int* array_1d(int cols)
{
    int* arr = malloc(cols * sizeof(int));
    for (int i = 0; i < cols; i++)
    {
        arr[i] = i;
    }
    return arr;
}

int** array_2d(int rows, int cols)
{
    /* Allocate memory for multidimensional array */
    int** arr = malloc(rows * sizeof(int*));
    for (int i = 0; i < cols; i++)
    {
        arr[i] = malloc(cols * sizeof(int));
    }

    /* Fill array */
    for (int j = 0; j < rows; j++)
    {
        for (int k = 0; k < cols; k++)
        {
            arr[j][k] = (j + 1) * (k + 1);
        }
    }
    return arr;
}

void main() {}
