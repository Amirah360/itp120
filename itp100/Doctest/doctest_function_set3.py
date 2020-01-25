import numpy as np


def to_base3(num):
    """
    Convert an decimal integer into a string representation of its base3
    digits.

      >>> to_base3(10)
      '101'
      >>> to_base3(12)
      '110'
      >>> to_base3(6)
      '20'
    """

    return np.base_repr(num,base=3)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
