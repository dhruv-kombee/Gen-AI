for i in range(100):
    st = input("Enter y or n for the calculation (Yes / No): ")
    if st == "y" or st == "Y":
        arr = []
        print("For Exit Enter Q or q")
        num = 1
        while True:
            n = input(f"Enter Q or the value of number {num}: ")
            if n == "q" or n == "Q":
                break
            arr.append(int(n))
            print(
                "\nFor Sum            = 1\n"
                "For Subtraction    = 2\n"
                "For Multiplication = 3\n"
                "For Divide         = 4\n"
                "Enter C for Calculation \n"
            )
            op = input("Enter arithmetic operation: ")

            if op == "c" or op == "C":
                break
            arr.append(op)
            num += 1
        print("Array =", arr)
        total = arr[0]
        i = 1

        while i < len(arr):

            op = arr[i]
            num = arr[i + 1]

            if op == "1":
                total += num
            elif op == "2":
                total -= num
            elif op == "3":
                total *= num
            elif op == "4":
                total /= num
            else:
                print("Invalid operation")
            i += 2
        print("Answer =", total)
    elif st == "n" or st == "N":
        print("Exiting...")
        break
    else:
        print("Enter valid answer")