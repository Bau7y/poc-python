def winner(a, b):
    if(a < b):
        return True;


def main():
    playerA = int(input("Ingrese los puntos del jugador 1: "))
    playerB = int(input("Ingrese los puntos del jugador 2: "))
    if winner(playerA, playerB):
        print("El jugador B ha ganado el set!!!")
    elif (playerA <= 5 and playerB <= 5):
        print("El partido sigue...")
    elif (playerA == 6 and playerB == 6):
        print("El set ha terminado en empate...")
    elif (playerA > 7 or playerB > 7):
        print("El set es invalido...")
    else:
        print("El jugador A ha ganado el set!!!")


if __name__ == "__main__":
    main()