import sys

def pivot(tableau, row, col):
    pivot_element = tableau[row][col]
    tableau[row] = [element / pivot_element for element in tableau[row]]
    
    for i in range(len(tableau)):
        if i != row:
            ratio = tableau[i][col]
            tableau[i] = [tableau[i][j] - ratio * tableau[row][j] for j in range(len(tableau[0]))]

def is_infeasible(tableau, n):
    return any(tableau[i][-1] < 0 for i in range(n))

def simplex(n, m, c, A, b):
    tableau = []
    for i in range(n):
        #tableau.append(A[i] + [0]*i + [1] + [0]*(n-i-1) + [b[i]])
        tableau.append(A[i] + [0]*n + [b[i]])

    #tableau.append([0]*(m + n) + [1])
    tableau.append([-ci for ci in c] + [0]*n + [0])

    
    while is_infeasible(tableau, n):
        row = min(range(n), key=lambda i: tableau[i][-1])
        col = min(range(m + n), key=lambda j: tableau[row][j] if tableau[row][j] < 0 else float('inf'))
        if tableau[row][col] >= 0:
            break
        pivot(tableau, row, col)
    
    if any(tableau[i][-1] < 0 for i in range(n)):
        print("inviavel")
        # certificate = [0]*m
        # for i in range(n):
        #     for j in range(m):
        #         if tableau[i][j] == 1:
        #             certificate[j] = tableau[i][-1]
        # print(" ".join(f"{y:.3f}" for y in certificate))
        return
    
    tableau.pop()
    
    # Adding the objective function to the tableau
    tableau.append([-ci for ci in c] + [0]*n + [0])
    
    while True:
        col = min(range(len(tableau[0])-1), key=lambda j: tableau[-1][j])
        if tableau[-1][col] >= 0:
            break
        
        row = -1
        min_ratio = float('inf')
        for i in range(n):
            if tableau[i][col] > 0:
                ratio = tableau[i][-1] / tableau[i][col]
                if ratio < min_ratio:
                    min_ratio = ratio
                    row = i
        
        if row == -1:
            print("ilimitada")
            # solution = [0]*m
            # for i in range(n):
            #     for j in range(m):
            #         if tableau[i][j] == 1:
            #             solution[j] = tableau[i][-1]
            # print(" ".join(f"{x:.3f}" for x in solution))
            # direction = [0]*m
            # direction[col] = 1
            # print(" ".join(f"{d:.3f}" for d in direction))
            return
        
        pivot(tableau, row, col)
    
    solution = [0]*m
    for i in range(n):
        for j in range(m):
            if tableau[i][j] == 1:
                solution[j] = tableau[i][-1]
    
    print("otima")
    print(f"{tableau[-1][-1]:.3f}")
    print(" ".join(f"{x:.3f}" for x in solution))
    
    certificate = tableau[-1][m:m+n]
    #print(" ".join(f"{y:.3f}" for y in certificate))


if __name__ == "__main__":
    # Lê o nome do arquivo de entrada do argumento de linha de comando
    input_file = sys.argv[1]
    
    with open(input_file, 'r') as file:
        # Lê a primeira linha (n e m)
        n, m = map(int, file.readline().split())
        
        # Lê a segunda linha (vetor de custos c)
        c = list(map(float, file.readline().split()))
        
        # Lê as n linhas seguintes contendo as restrições
        A = []
        b = []
        for i in range(n):
            linha = list(map(float, file.readline().split()))
            A.append(linha[:m])  # m primeiros valores são os coeficientes da restrição
            b.append(linha[m])   # último valor é o valor b_i
    
    # Chama o método simplex com os dados lidos
    simplex(n, m, c, A, b)