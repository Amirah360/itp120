def to_base(num, base):
    """
    Convert an decimal integer into a string representation of the digits
    representing the number in the base (between 2 and 16) provided.

      >>> to_base(10, 3)
      '101'
      >>> to_base(11, 2)
      '1011'
      >>> to_base(10, 6)
      '14'
      >>> to_base(21, 3)
      '210'
      >>> to_base(21, 11)
      '1A'
      >>> to_base(47, 16)
      '2F'
      >>> to_base(65535, 16)
      'FFFF'
      >>> to_base(53593, 64)
      'NFZ'
    """
    if num == 0
        return '0'

    wild = '0123456789ABCDEF'

    if base == 64:
        wild = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijglmnopqrstuvwxyz0123456789+/'

    numstr = ''

    while num:
        numstr = wild[num % base] + numstr
        num //= base 
        
    return numstr
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
