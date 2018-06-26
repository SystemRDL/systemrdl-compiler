from antlr4.Token import CommonToken

def is_pow2(x):
    return (x > 0) and ((x & (x - 1)) == 0)


def roundup_pow2(x):
    return 1<<(x-1).bit_length()

def roundup_to(x, n):
    if x % n:
        return (x//n + 1) * n
    else:
        return (x//n) * n

def get_ID_text(token):
    """
    Get the text from the ID token.
    Strips off leading slash escape if present
    """
    if isinstance(token, CommonToken):
        text = token.text
    else:
        text = token.getText()
    
    text = text.lstrip('\\')
    return text

def truncate_int(v, width):
    mask = (1 << width) - 1
    return v & mask
