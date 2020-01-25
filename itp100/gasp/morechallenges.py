from gasp import *

 challenge1 = "What is " + str(random_between(1, 10)) + " times " + str(random_between(1, 10)) + "? "
 print(challenge1)

 challenge2 = read_number("Give me a number: ") + read_number("Give me another number: ")
 print(challenge2)

challenge4 = random_between(1, 100)
print(str(challenge4) * 5)

challenge6 = read_number("Give me a number: ")
if challenge6 >= 100:
    print("hahahhahahha")
else:
    print("no")

challenge7 = read_number("Give me a number: ")
if challenge7 == 100:
    print("hahahhahahha")
else:
    print("no")


#challenge 9
for index in range(0, 3):
    win1 = random_between(1, 10)
    win2 = random_between(11, 20)
    win3 = random_between(21, 30)
    index += 1
    winners = str(win1) + " " + str(win2) + " " + str(win3)

print("And the three lucky winners are: " + winners + ".")
