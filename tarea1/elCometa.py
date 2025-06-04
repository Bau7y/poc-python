import random

def showSalePrice(rawMat, labor, manufactCost, key):
    print("La clave de su producto es: ", key)
    print("El precio de venta final es de: ", rawMat + labor + manufactCost)


def calcManufactCost(rawMat, prodKey):
    if (prodKey == 2) | (prodKey == 5):
        return rawMat * 0.30;
    if (prodKey == 3) | (prodKey == 6):
        return rawMat * 0.35;
    if (prodKey == 1) | (prodKey == 4):
        return rawMat * 0.28;

def calcLabor(rawMat, prodKey):
    if (prodKey == 3) | (prodKey == 4):
        return rawMat * 0.75;
    if (prodKey == 1) | (prodKey == 5):
        return rawMat * 0.80;
    if (prodKey == 2) | (prodKey == 6):
        return rawMat * 0.85;


def reqData():
    return int(input("Digite la materia prima total del producto: "))


def main():
    key = random.randrange(1, 6)
    rawMaterial = reqData()
    labor = calcLabor(rawMaterial, key)
    manufactCost = calcManufactCost(rawMaterial, key)
    showSalePrice(rawMaterial, labor, manufactCost, key)

if __name__ == "__main__":
    main()