def main(lista):
    for i in range(len(lista)-1):
        min_elem = min(lista[i:])
        idx_min = lista[i:].index(min_elem)
        lista[i], lista[idx_min+i] = lista[idx_min+i], lista[i]
    print(lista)

if __name__ == "__main__":
    main([2,1,1,3,3,5,10,12,5,5])