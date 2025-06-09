def shAddition(a, b):
    print("La suma de {} y {} es: {}".format(a, b, a + b))


def reqNumbs():
    try:
        return int(input("Digite el primer numero: ")), int(input("Digite el segundo numero: "))
    except ValueError:
        print("Solo se admiten numeros...")


def main():
    x, y = reqNumbs()
    shAddition(x, y)


if __name__ == "__main__":
    main()