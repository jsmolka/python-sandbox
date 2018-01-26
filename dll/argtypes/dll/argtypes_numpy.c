#include <stdio.h>
#include <stdint.h>

void at_npy_1d_int(int* l, int len)
{
    printf("at_npy_1d_int: ");
    for (int i = 0; i < len; i++)
    {
        printf("%d ", l[i]);
    }
    printf("\n");
}

void at_npy_1d_dbl(double* l, int len)
{
    printf("at_npy_1d_dbl: ");
    for (int i = 0; i < len; i++)
    {
        printf("%.1f ", l[i]);
    }
    printf("\n");
}

void at_npy_2d_int(int** l, int rows, int cols)
{
    printf("at_npy_2d_int:\n");
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            printf("%d ", l[i][j]);
        }
        printf("\n");
    }
}

void at_npy_2d_dbl(double** l, int rows, int cols)
{
    printf("at_npy_2d_double:\n");
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            printf("%.1f ", l[i][j]);
        }
        printf("\n");
    }
}

void at_npy_1d_uint32(uint32_t* l, int len)
{
    printf("at_npy_1d_uint32: ");
    for (int i = 0; i < len; i++)
    {
        printf("%d ", l[i]);
    }
    printf("\n");
}

void at_npy_2d_uint16(uint16_t** l, int rows, int cols)
{
    printf("at_npy_2d_uint16:\n");
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            printf("%d ", l[i][j]);
        }
        printf("\n");
    }
}

void at_npy_1d_out_int(int* in, int len, int* out)
{
    for (int i = 0; i < len; i++)
    {
        out[i] = 2 * in[i];
    }
}

void at_npy_2d_out_dbl(double** in, int rows, int cols, double** out)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            out[i][j] = 2 * in[i][j];
        }
    }
}
