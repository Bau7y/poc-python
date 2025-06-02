def userTypeValidation(client):
    if (client["tipoCliente"] == "Unitario"):
        return True;


def ageValidation(client):
    if (client["edad"] >= 25 and client["edad"] <= 35):
        return True;
    

def reqProducts():
    prodList = []
    for i in range(0,3):
        try:
            pedido = int(input("Digite la cantidad de paquetes de arroz, coca colas y pan que va a comprar: "))
            prodList.append(pedido)
        except:
            print("Solo se permiten numeros...")
    return prodList;


def reqData():
    client = {
        "nombre": "",
        "edad" : 0,
        "tipoCliente" : "Unitario"
    }
    client["nombre"] = input("Digite su nombre: ")
    try:
        client["edad"] = int(input("Digite su edad: "))
    except:
        print("Solo se admiten numeros...")
    client["tipoCliente"] = input("ingrese tipo de cliente: ").capitalize()
    return client;


def caja(productos):
    clients = 0
    while (clients < 3):
        datosCliente = reqData()
        prodQuantity = reqProducts()
        total = prodQuantity[0] * productos["Arroz"] + prodQuantity[1] * productos["Coca Cola"] + prodQuantity[2] * productos["Pan"]
        if userTypeValidation(datosCliente):
            if ageValidation(datosCliente):
                print("su total es de: ", total - (total * 0.05), " con un 5% incluido")
            else:
                print("su total es de: ", total)
        else:
            print("Su total es de: ", total - (total * 0.15), " con un 15% incluido")

        
        

def main():
    productos = {
        "Arroz" : 1000,
        "Coca Cola" : 1500,
        "Pan" : 800
    }
    caja(productos)


if __name__ == "__main__":
    main()