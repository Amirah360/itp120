num_set = {1, 2, 3, 4, 5}
word_set = set(["spam", "eggs", "sausage"])

print(3 in num_set) 
#true because it's there
print("spam" not in word_set)
#false because spam is there 

letters = {"a", "b", "c", "d"}
if "e" not in letters:
  print(1)
else:
  print(2)
#print 1

nums = {1, 2, 1, 3, 1, 4, 5, 6}
print(nums) 
#okay what? where do the other 1s go?
#ohhh nvm sets can nt contain duplicated elements 

nums.add(-7)
nums.remove(3)
print(nums)

first = {1, 2, 3, 4, 5, 6}
second = {4, 5, 6, 7, 8, 9}

print(first | second)
print(first & second)
print(first - second)
print(second - first)
print(first ^ second)
