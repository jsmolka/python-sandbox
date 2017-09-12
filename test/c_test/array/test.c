#include <stdlib.h>
#include <stdio.h>

void func(const void* input, int rows, int cols)
{
    int** array = (int**) input;
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            printf("%i\n", array[i][j]);
        }
    }

}