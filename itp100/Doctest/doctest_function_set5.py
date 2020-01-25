import numpy as np

def to_base(num, base):
    """
    Convert an decimal integer into a string representation of the digits
    representing the number in the base (between 2 and 10) provided.

      >>> to_base(10, 3)
      '101'
      >>> to_base(11, 2)
      '1011'
      >>> to_base(10, 6)
      '14'
    """

    return np.base_repr(num,base)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

