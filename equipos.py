def calcMatches(points):
        wMatches = int(input("Digite el numero de partidos ganados: "))
        return points.insert(0, wMatches * 3)
        #tMatches = int(input("Digite el numero de partidos empatados: "))
        #return points.insert(1, tMatches * 2 + points[1])
        #lMatches = int(input("Digite el numero de partidos empatados: "))
        #return points.insert(2, lMatches  + points[2])

def reqMatchesW(points):
    userOpt = int(input("Digite 1 para digitar los partidos ganados, 2 para los empatados, 3 para los perdidos y 4 para salir "))
    while (userOpt != 4):
        match userOpt:
            case 1:
                listaPuntos = calcMatches(points)
                
            case 2:
                calcMatches(points, userOpt)
            case 3:
                calcMatches(points, userOpt)
            case _:
                print("La opcion digitada no es valida...")
                continue;
    else:
        pass
    


def main():
    points = []
    reqMatchesW(points)


if __name__ == '__main__':
    try:
        main()
    except:
        print("error!!!")