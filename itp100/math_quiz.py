from gasp import *

right = 0

for index in range(0, 10):
    num1 = random_between(1, 10)
    num2 = random_between(1, 10)
    answer = read_number("What is " + str(num1) + " times " + str(num2) + "? ")
    if answer == num1 * num2:
        print("well done!")
        right += 1
        index += 1
    else:
        print("no!")
        index += 1

print("I asked you 10 questions.  You got " + str(right) + " of them right.")

