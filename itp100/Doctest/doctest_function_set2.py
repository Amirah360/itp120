def to_binary(num):
    """
    Convert an decimal integer into a string representation of its binary
    (base2) digits.
      >>> to_binary(10) 
      '1010'
      >>> to_binary(12) 
      '1100'
      >>> to_binary(0) 
      '0'
      >>> to_binary(1) 
      '1'
    """
    
    return bin(num)[2:]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
