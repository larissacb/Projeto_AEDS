class Sala:
    def __init__(self, nome, lotacao):
        self.nome=nome
        self.lotacao=lotacao
        self.matriz_horarios=list()
        # a matiz de horarios tem 6 linhas, 8 colunas e armazena strings
        # cada linha representa um dia semana
        #a coluna representa um dos horarios
        self.matriz_horarios=[[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

    def getLotacao(self):
        return self.lotacao

    def getNome(self):
        return self.nome
    
    def verificaElemMatriz(self, linha, coluna): #verifico uma determinada posicao da matriz
        return self.matriz_horarios[linha][coluna]

    def getTamMatriz(self): #retorno a quantidade de linhas da matriz
        return len(self.matriz_horarios)

    def getTamColuna(self, linha): #retorno o tamanho de cada coluna da matriz
        return len(self.matriz_horarios[linha])

    def addElemento(self, linha, coluna, elemento): #adiciono a turma em um horario da matriz dessa sala
        self.matriz_horarios[linha][coluna] = elemento

    def imprimirDados(self):
        print("Sala: ", self.nome)
        for i in range(len(self.matriz_horarios)): #percorrendo as linhas da matriz
            if i == 0:
                print("====== Segunda-feira ======")
            elif i == 1:
                print("====== Terca-feira ======")
            elif i == 2:
                print("====== Quarta-feira ======")
            elif i == 3:
                print("====== Quinta-feira ======")
            elif i == 4:
                print("====== Sexta-feira ======")
            elif i == 5:
                print("====== Sabado ======")
            for j in range(len(self.matriz_horarios[i])): #percorrendo as colunas da matriz
                if j == 0:
                    print("12M", self.matriz_horarios[i][j])
            
            


        
        
        
       
        
