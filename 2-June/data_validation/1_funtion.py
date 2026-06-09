from pydantic import validate_call
@validate_call
def add_numbers(a:int ,b:int ):
    return a+b

res = add_numbers("12",3)

print(res)
