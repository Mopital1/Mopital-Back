import random
import string


def randomize_digit_char(chars=string.digits, N=5):
    """
    custom code generator for mpi
    """
    return "".join(random.choice(chars) for _ in range(N))
