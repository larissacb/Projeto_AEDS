class tabelaHash:
    def __init__(self):
        self.tabelaHash=dict() #crio um dicionario
        
    def verificaElemento(self, elemento): #verificar se ja existe essa chave no dict
        if elemento in self.tabelaHash: #se o elemento ja existe e necessario adicionar a posicao na lista correspondente a chave que ja foi criada
            return True
        else:
            return False
    
    def addElementoNovo(self, elemento, pos): #se o elemento nao existe, add o mesmo e o valor equivelente na posicao
        self.tabelaHash[elemento]=list()
        self.tabelaHash[elemento].append(pos)

    def addElementoRep(self, elemento, pos): #se o elemento ja existe, nao ha necessidade de criar uma lista nem uma nova posicao no dict
        self.tabelaHash[elemento].append(pos)

    def getTamLista(self, elemento): #retorno o tamanho da lista que constitui o valor do dicionario
        return len(self.tabelaHash[elemento])

    def getElemLista(self, elemento, i): #retorno o elemento de determinada posicao da lista que constitui o parametro de valor do dicionario
        return int(self.tabelaHash[elemento][i])
