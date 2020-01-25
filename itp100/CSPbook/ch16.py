def name_procedure(name):
    start = "My name is "
    combined = start + (name * 2)
    print(combined)
    print(len(combined))

name_procedure('John')



def item_lister(items):
    items[0] = "First item'
    items[1] = items[0]
    items[2] = items[2] + 1
    print items

 item_lister([2, 4, 6 8])

"

name = "Mark"
start = "My name is "
combined = start + name
print(len(combined))
print(combined)
print(name * 3)


a_string = "limo"
b_string = "bow"
c_string = (a_string + b_string) * 2
print(len(c_string))



my_first_list = [12,"ape",13]
print(len(my_first_list))
print(my_first_list * 3)
my_second_list = my_first_list + [321.4]
print(my_second_list)

source = ["This", "is", "a", "list"]
so_far = []
for index in range(0,len(source)):
    so_far = [source[index]] + so_far
    print(so_far)


items = ["hi", 2, 3, 4]
items[0] = items[0] + items[0]
items[1] = items[2] - 3
items[2] = items[1]
print(items)

source = ["This","is", "a","list"]

so_far = []
for index in range(0, len(source)):


    so_far = [source[index]] + so_far
print(so_far)



def item_lister(items):
    items[0] = "First item"
    items[1] = items[0]
    items[2] = items[2] + 1
    print(items)
item_lister([2, 4, 6, 8])
i
for index in range(range 5, -1, -1):
    print(index

source = [1, 2, 3, 4]
addList = []
def adding(numbers):
    addList = []
    for index in range(0, len(numbers)):
        addList = numbers[index] + 5
        print(addList)
    return addList 

for index in range(0, len(source)):
    addList = source[index] + 5
    print(addList)
adding([1, 2, 3, 4])

def sumAll(numbers):
    sumPos = 0
    sumNeg = 0
    total = 0
    for item in numbers:
        if item >= 0:
            sumPos = sumPos + item
        if item < 0:
            item = abs(item)
            sumNeg = sumNeg + item
    total = sumPos + sumNeg
    return(total)

print(sumAll([-3, 2, -8, 5, -20, -33, 15]))

`
