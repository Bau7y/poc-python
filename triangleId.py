def calcTriangle(triangleM):
    if triangleM[0] == triangleM[1] and triangleM[0] == triangleM[2] and triangleM[1] == triangleM[2]:
        return print("El triangulo es equilatero")
    if triangleM[0] == triangleM[1] or triangleM[0] == triangleM[2] or triangleM[1] == triangleM[2]:
        return print("El triangulo es Isóceles")
    print("El triangulo es escaleno")


def reqTriangle():
    triangleMeasure = []
    for i in range(0, 3):
        user = float(int(input("Ingrese la medida de los lados del triangulo: ")))
        triangleMeasure.append(user)
    return triangleMeasure


def main():
    triangle = reqTriangle()
    calcTriangle(triangle)


if __name__ == '__main__':
    main()