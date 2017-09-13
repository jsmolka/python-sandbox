#include <stdlib.h>
#include <stdio.h>

void func(int** array)
{
    for (int i = 0; i < 10; i++)
    {
        for (int j = 0; j < 10; j++)
        {
            printf("%i\n", array[i][j]);
        }
    }
}
