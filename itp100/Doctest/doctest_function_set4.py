import numpy as np

def to_base4(num):
    """
    Convert an decimal integer into a string representation of its base4
    digits.

      >>> to_base4(20)
      '110'
      >>> to_base4(28)
      '130'
      >>> to_base4(3)
      '3'
    """

    return np.base_repr(num,base=4)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
