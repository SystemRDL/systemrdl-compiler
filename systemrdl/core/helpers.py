
def is_pow2(x):
    return((x > 0) and ((x & (x - 1)) == 0))


def roundup_pow2(x):
    return(1<<(x-1).bit_length())

def roundup_to(x, n):
    if(x % n):
        return((x//n + 1) * n)
    else:
        return((x//n) * n)
