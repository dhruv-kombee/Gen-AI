# variables
a = 10.0
b = "Dhruv"
c = True
d = None  # nonetpe
e = [1, 2, 3]  # list
e2 = [1, 2, 3]  # list
f = (1, 2, 3)  # touple
g = {1, 3, 4}  # set
# comment

print(a, type(a))
print(a, b, type(b))
print(c, a)
print(e)
h = (e, e2)
print("The value of h is ", h)

print(int(a))


# type conversion

s = "1111"
aa = int(s, 2)
print(aa)

# input form the user
print("========================")
ainput = input("Enter the name = ")
print(ainput)

print(" %s comes and goes " % (ainput))
print(" %s %s come and seat " % ("hello", ainput))
print(" %f comes and goes " % (a))


# arithmatic operation

a = 10
b = 3

c = a / b
print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
print(f"Division:{c:.2f}")
print("Floor Division:", a // b)
print("Modulus:", a % b)
print("Exponentiation:", a**b)
