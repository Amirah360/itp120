#New 

def base64decode(four_chars):
	    """
	      >>> base64decode('STOP')
	      b'I3\\x8f'

	    """
	    digits = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
	    ints = [digits.index(ch) for ch in four_chars]
	    b1 = (ints[0] << 2) | ((ints[1] & 48) >> 4)
	    b2 = (ints[1] & 15) << 4 | ints[2] >> 2
            #b3 is b3 equals indexs the second character then the bitwise adds 
            #the third character and moves them 6 charcters to the left. or it indexs the 3rd character. 
            b3 = (b3 = (ints[2] & 3) << 6 | ints[3]

	    return bytes([b1, b2, 143])


#Ignore












#Encoding Base64 LMAO IF THIS WORKS IM SO HIPP
   # def base64encode(three_bytes):
   # """
      >>> base64encode('Wivm')
      b'\\x5A\\x2B\\xE6'
      >>> base64encode('STOP')
      b'\\x49\\x33\\x8F'
      >>> base64encode('////')
#      b'\\xFF\\xFF\\xFF
      >>> base64encode('AAAA')
      b'\\x00\\x00\\x00'
   # """
   # digits = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

   # try:
        # turn the three bytes into ints
        # b1, b2, b3 = three_bytes[0], three_bytes[1], three_bytes[2]
        # reversing it
        three_bytes[0], three_bytes[1], three_bytes[2] = b1, b2, b3
        # get first 6 bits of b1 
        # index1 = b1 >> 2
        #reversing it
        b1 >> 2 = index1
        # join last 2 bits of b1 shifted left 4 with first 4 bits of b2
        # index2 = (b1 & 3) << 4 | b2 >> 4
        # reversing it
        (b1 & 3) << 4 | b2 >> 4 = index2
        # join last 4 bits of b2 shifted left 2 with first 2 bits of b3
        # index3 = (b2 & 15) << 2 | (b3 & 192) >> 6
        #reversing it
        (b2 & 15) << 2 | (b3 & 192) >> 6 = index3
        # get last 6 bits of b3
        # index4 = b3 & 63
        b3 & 63 = index4

#    except (AttributeError, TypeError):
#        raise AssertionError('Input should be 3 bytes')

#    return f'{digits[index1]}{digits[index2]}{digits[index3]}{digits[index4]}'
# reversing it

 #   return f'{index1[digits]}{index2[digits]}{index3[digits]}{index4[digits]}'

if __name__ == '__main__':
    import doctest
doctest.testmod()

