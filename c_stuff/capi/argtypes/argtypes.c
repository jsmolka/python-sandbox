#include<stdio.h>

void arg_int(int i)
{
    printf("arg_int: %d\n", i);
}

void arg_double(double d)
{
    printf("arg_double: %f\n", d);
}

void arg_string(char* s)
{
    printf("arg_string: "); 
    printf(s);
    printf("\n");    
}

void arg_list_int(int* l, int len)
{
    printf("arg_list_int: ");
    for (int i = 0; i < len; i++)
    {
        printf("%d ", l[i]);
    }
    printf("\n");
}

void arg_list_double(double* l, int len)
{
    printf("arg_list_double: ");
    for (int i = 0; i < len; i++)
    {
        printf("%1f ", l[i]);
    }
    printf("\n");
}

void arg_list_2d(int** l, int r, int c)
{
    printf("arg_list_2d:\n");
    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++)
        {
            printf("%d ", l[i][j]);
        }
        printf("\n");
    }
}