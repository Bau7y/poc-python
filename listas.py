
def concatLists(l1, l2):
    newList = [l1, l2]
    print(newList[1])


def list1Changes(n1List):
    print(len(n1List))
    n1List.append(9)
    print(n1List)
    n1List.insert(0, 10)
    print(n1List)
    n1List.sort()
    print(n1List)
    n1List.remove(5)
    print(n1List)
    n1List.extend([11, 12, 13])
    

def main():
    num1List = [1, 2, 3, 4, 5, 6, 7, 8]
    num2List = [10, 20, 30, 40, 50]
    list1Changes(num1List)
    concatLists(num1List, num2List)

    

if __name__ == "__main__":
    main()