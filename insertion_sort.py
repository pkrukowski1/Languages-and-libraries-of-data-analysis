def main(lista):
    for i in range(1,len(lista)):
        for j in range(0,i):
            if (lista[i] < lista[j]):
                lista[i], lista[j] = lista[j], lista[i]
    print(lista)

if __name__ == '__main__':
    main([1,2,4,1,20,2,4,14,16,3])
