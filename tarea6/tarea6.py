def showUsers(usersList):
    for users in usersList:
        for key, value in users.items():
            print(key, ": ", value, "\n")


def followCase(userReg, usersList):
    for showUser in usersList:
        print(showUser["nombre"], ":", showUser["cedula"])
    follow = int(input("\nCedula del usuario que desea seguir: "))
    for user in usersList:
        if user["cedula"] == follow:
            if userReg["cedula"] not in user["seguidores"]:
                user["seguidores"].append(userReg["cedula"]) 
                print("Usuario seguido con exito...\n")
                break;
            else:
                print("Ya sigues a este usuario...\n")
                break;
    else:
        print("Usuario no encontrado...")


def messagesCase(user):
    messagesList = []
    for i in range(int(input("Cuantos mensajes desea publicar: "))):
        messagesList.append(input("Mensaje: "))
    user["mensajes"] = messagesList
    print(user["mensajes"])
    print("Mensajes publicados con exito...\n")
    return user;


def loginMnu(user, usersList):
    while(True):
        print("\n1.Publicar Mensajes\n2.Seguir Usuarios\n3.Salir")
        try:
            opt = int(input("Opción: "))
            match opt:
                case 1:
                    messagesCase(user)
                case 2:
                    followCase(user, usersList)
                case 3:
                    print("\nSaliendo...\n")
                    break;
                case _:
                    print("No se ha encontrado la opción digitada...")
        except ValueError:
            print("Solo se admiten numeros...")


def loginHandler(usersList):
    print("\n-Iniciar Sesion-\n\n")
    ced =int(input("Ingrese su cedula: ").replace(" ", ""))
    for user in usersList:
        if user["cedula"] == ced:
            print("Bienvenido\n", user["nombre"])
            loginMnu(user, usersList)
            break;
    else:
        print("Usuario no encontrado...")


def reqGender():
    while(True):
        gender = input("Género (M/F): ").upper()
        if gender == "M" or gender == "F":
            return gender;
        print("Género no válido...")


def reqId(usersList):
    while(True):
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
        "genero": reqGender(),
        "seguidores": []
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
                if listaPersonas == []:
                    print("No hay usuarios registrados...")
                else:
                    showUsers(listaPersonas)
            case 4:
                print("Saliendo...")
                quit()
            case _:
                print("No se ha encontrado la opción digitada...")


if __name__ == "__main__":
    mnuHandler()