def calcMatches(points, user):
        match user:
            case 1:
                wMatches = int(input("Digite el numero de partidos ganados: "))
                return points.insert(0, wMatches * 3)
            case 2:
                tMatches = int(input("Digite el numero de partidos empatados: "))
                return points.insert(1, tMatches * 2 )
            case 3:
                lMatches = int(input("Digite el numero de partidos perdidos: "))
                return points.insert(2, lMatches)
            

def reqMatchesW(points):
    userOpt = 0
    listaPuntos = []
    while (userOpt != 4):
        userOpt = int(input("Digite 1 para digitar los partidos ganados, 2 para los empatados, 3 para los perdidos y 4 para salir "))
        match userOpt:
            case 1:
                listaPuntos = calcMatches(points, userOpt)
                print(listaPuntos)
            case 2:
                calcMatches(points, userOpt)
            case 3:
                calcMatches(points, userOpt)
            case 4:
                print("Saliendo...")
            case _:
                print("La opcion digitada no es valida...")
    

def main():
    points = []
    reqMatchesW(points)


if __name__ == '__main__':
    try:
        main()
    except:
        print("error!!!")