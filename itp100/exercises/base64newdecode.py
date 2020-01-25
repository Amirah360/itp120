def base64encode(f):
    """
    Read the contents of a binary file and return a base64 encoded string.
    """
    s = ''
    data = f.read(3)

    while data:
        s += encode3bytes(data)
        data = f.read(3)

    return s


def base64decode(f):
    """
    Take the encoded string and decode it
    """
    s = 'VGhpcyBpcyBhIHRlc3QuIEl0IGlzIG9ubHkgYSB0ZXN0IQ=='
    encoded_string = s 
    
    digits = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    
    #take those 4  and then convert them and correlate them to the thingy
    #this it it decoded now figure out how to write that in python 
    
   #  digits.index(letters) for letters in encoded_string

 if encoded_string(len) == 48 
    encoded_string(len) // 8 

            return encoded_string 
