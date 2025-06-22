
def messagesCase(user):
    messagesList = []
    for i in range(int(input("Cuantos mensajes desea publicar: "))):
        messagesList.append(input("Mensaje: "))
    user["mensajes"] = messagesList
    print(user["mensajes"])
    print("Mensajes publicados con exito...\n")
    return user


def loginMnu(user):
    while(True):
        print("\n1.Publicar Mensajes\n2.Seguir Usuarios\n3.Salir")
        try:
            opt = int(input("Opción: "))
            match opt:
                case 1:
                    messagesCase(user)
                case 2:
                    print("Seguir Usuarios")
                case 3:
                    print("\nSaliendo...\n")
                    break;
                case _:
                    print("No se ha encontrado la opción digitada...")
        except ValueError:
            print("Solo se admiten numeros...")


def loginHandler(usersList):
    print("\n-Iniciar Sesion-\n\n")
    for user in usersList:
        if user["cedula"] == int(input("Ingrese su cedula: ").replace(" ", "")):
            print("Bienvenido\n", user["nombre"])
            loginMnu(user)
        else:
            print("Cedula no encontrada...")
            break;


def reqGender():
    while(True):
        gender = input("Género (M/F): ").upper()
        if gender == "M" or gender == "F":
            return gender;
        print("Género no válido...")


def reqId(usersList):
    if usersList == []:
        try:
            return int(input("Ingrese su cedula: ").replace(" ", ""))
        except ValueError:
            print("Solo se admiten numeros...")
    else:
        for user in usersList:
            try:
                userId = int(input("Ingrese su cedula: ").replace(" ", ""))
                if userId == user["cedula"]:
                    print("La cedula ya se encuentra registrada...")
                else:
                    return userId
            except ValueError:
                print("Solo se admiten numeros...")


def userRegistration(usersList):
    user = {
        "cedula": reqId(usersList),
        "nombre" : input("Ingrese su nombre: ").capitalize(),
        "genero": reqGender()
    }
    return user;


def reqUserOpt():
    print("1.Iniciar Sesion\n2.Registrar Persona\n3.Reporte\n4.Salir\n")
    try:
        return int(input("Opción: "))
    except ValueError:
        print("Solo se admiten numeros...")


def mnuHandler():
    listaPersonas = []
    while(True):
        userOption = reqUserOpt()
        match userOption:
            case 1:
                if listaPersonas == []:
                    print("No hay usuarios registrados...")
                else:
                    loginHandler(listaPersonas)
            case 2:
                newUser = userRegistration(listaPersonas)
                listaPersonas.append(newUser)
            case 3:
                print("Reporte")
            case 4:
                print("Saliendo...")
                quit()
            case _:
                print("No se ha encontrado la opción digitada...")


if __name__ == "__main__":
    mnuHandler()