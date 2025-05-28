#def sortNums():
#    pass

def calc(num1, num2, num3):
    if num1 != num2 and num1 != num3 and num2 != num3:
        if num1 > num2 and num1 > num3:
            if num2 > num3:
                print(num1, " es el mayor y ", num3, " es el menor")
            else:
                print(num1, " es el mayor y ", num2, " es el menor")
        elif num2 > num1 and num2 > num3:
            if num1 > num3:
                print(num2, "Es el mayor y ", num3, " es el menor")
            else:
                print(num2, "Es el mayor y ", num1, " es el menor")
        elif num1 > num2:
            print(num3, " Es el mayor y ", num2, " es el menor")
        else:
            print(num3, " Es el mayor y ", num1, " es el menor")

    else:        
        print("Debe digitar numeros distintos entre ellos")


def userInput():
    num1 = int(input("Digite numero: "))
    num2 = int(input("Digite numero: "))
    num3 = int(input("Digite numero: "))
    calc(num1, num2, num3)


def main():
    userInput()
        

if __name__ == '__main__':
    main()