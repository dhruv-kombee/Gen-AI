def marks():
    mark = []
    sub = ["Gujarati", "Maths", "English", "Hindi", "Science"]
    i = 0
    try:
        while i < 5:
            num = int(input(f"Enter Subject {sub[i]} Marks : "))
            mark.append(num)
            i += 1
    except ValueError:
        print("Please Enter Valid input again !! ")

    return mark,sub

def calculate():

    mark , sub = marks()
    total = 0;
    for i in range(len(mark)):
        total += mark[i]
    print(total)
    per = total*0.20
    print(per)
    return per

def grade():
    per = calculate()
    if per >= 90:
        print("Grade A")
    elif per >= 75 and per < 90:
        print("Grade B")
    elif per >= 60 and per <75:
        print("Grade C")
    elif per>=40 and per <60:
        print("Grade D")
    elif per>=0 and per<40:
        print("Fail")
    else:
        print("Grade is not generated due to some error !!")



name = input("Enter your name : ")
print(name)
grade()

