#include <stdio.h>
#include <stdlib.h>

void func(int* indata, size_t size)
{
    size_t i;
    for (i = 0; i < size; i++)
    {
        indata[i] = 4 * indata[i];
    }
}
