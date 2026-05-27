def outer_sum(x):
    def inner_sum(y):
        return x+y
    return inner_sum

clouser = outer_sum(10)

print(clouser(2000)) #inner function 
        