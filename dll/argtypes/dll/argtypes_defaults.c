#include <stdio.h>

void at_int(int i)
{
    printf("at_int: %d\n", i);
}

void at_dbl(double d)
{
    printf("at_dbl: %.10f\n", d);
}

void at_str(char* s)
{
    printf("at_str: ");
    printf(s);
    printf("\n");
}
