#1

def only_evens(nums):
    """
      >>> only_evens([3, 8, 5, 4, 12, 7, 2])
      [8, 4, 12, 2]
      >>> my_nums = [4, 7, 19, 22, 42]
      >>> only_evens(my_nums)
      [4, 22, 42]
      >>> my_nums
      [4, 7, 19, 22, 42]
    """
    return[num for num in nums if num % 2==0]
#2

def num_even_digits(n):
    """
      >>> num_even_digits(123456)
      3
      >>> num_even_digits(2468)
      4
      >>> num_even_digits(1357)
      0
      >>> num_even_digits(2)
      1
      >>> num_even_digits(20)
      2
    """
    counter = 0
    for num2 in str(n):
        if int(num2) % 2 == 0:
            counter += 1
    return counter

#3

def sum_of_squares_of_digits(nn):
    """
      >>> sum_of_squares_of_digits(1)
      1
      >>> sum_of_squares_of_digits(9)
      81
      >>> sum_of_squares_of_digits(11)
      2
      >>> sum_of_squares_of_digits(121)
      6
      >>> sum_of_squares_of_digits(987)
      194
    """
    total = 0
    for num3 in str(nn):
       square = int(num3) * int(num3)
       total += square
    return total

#4

def lots_of_letters(word):
    """
      >>> lots_of_letters('Lidia')
      'Liidddiiiiaaaaa'
      >>> lots_of_letters('Python')
      'Pyyttthhhhooooonnnnnn'
      >>> lots_of_letters('')
      ''
      >>> lots_of_letters('1')
      '1'
    """
    outputword = ""
    count = 1
    for num4 in str(word):
        outputword = outputword + (num4 * count)
        count += 1
    return outputword
    
#5

def gcf(m, n):
    """
      >>> gcf(10, 25)
      5
      >>> gcf(8, 12)
      4
      >>> gcf(5, 12)
      1
      >>> gcf(24, 12)
      12
    """
    if n > m:
        count = n
    if m > n:
        count = m
    while count > 0:
        if m % count == 0 and n % count == 0:
            return count
        else:
            count -= 1

#6

def is_prime(x):
    """
      >>> is_prime(2)
      True
      >>> is_prime(7)
      True
      >>> is_prime(199)
      True
      >>> is_prime(12)
      False
    """
    count = x - 1
    while count > 0:
        if x % count == 2:
            if count == 1:
                return True
            else:
                return False
        count -= 1
    if x == 1:
        return False
    if x == 0:
        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()

