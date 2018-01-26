#include <stdio.h>

void at_lst_1d_int(int* l, int len)
{
    printf("at_lst_1d_int: ");
    for (int i = 0; i < len; i++)
    {
        printf("%d ", l[i]);
    }
    printf("\n");
}

void at_lst_1d_dbl(double* l, int len)
{
    printf("at_lst_1d_dbl: ");
    for (int i = 0; i < len; i++)
    {
        printf("%.1f ", l[i]);
    }
    printf("\n");
}

void at_lst_2d_int(int** l, int rows, int cols)
{
    printf("at_lst_2d_int:\n");
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            printf("%d ", l[i][j]);
        }
        printf("\n");
    }
}

void at_lst_2d_dbl(double** l, int rows, int cols)
{
    printf("at_lst_2d_double:\n");
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            printf("%.1f ", l[i][j]);
        }
        printf("\n");
    }
}
