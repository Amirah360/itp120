fruits = open("sortedfruits.txt","r") #not actually sorted yet

sortin = fruits.readlines()
sortin = sorted(fruits)

fruits.close()

print(fruits)




