int rt_int(int* l, int len)
{
    int sum = 0;
    for (int i = 0; i < len; i++)
    {
        sum += l[i];
    }
    return sum;
}

double rt_dbl(double* l, int len)
{
    double sum = 0.f;
    for (int i = 0; i < len; i++)
    {
        sum += l[i];
    }
    return sum;
}

int rt_none(int* l, int len)
{
    return rt_int(l, len);
}
