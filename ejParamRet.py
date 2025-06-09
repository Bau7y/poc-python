def shAddition(a, b):
    print(f"La suma de {a} + {b} es: {a + b}")


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