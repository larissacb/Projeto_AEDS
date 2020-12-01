from turma import Turma
from sala import Sala
from TabelaHash import tabelaHash

#============================================================================================================================================
menu=False
aux=list()
turmas=list()
salas=list()

#============================================================================================================================================
def menu_inicial():
    print("======== Menu ========")
    print("1 - Imprimir turmas")
    print("2 - Alocacao das salas conforme a demanda ja apresentada")
    print("0 - Sair")
    op = int(input("Informe a opcao desejada: "))
    return op

#============================================================================================================================================
def abre_arq_cursos(arq):
    #teste para verificacao de arquivos com nomes errados ou inexistentes
    try:
        fhand=open(arq)
    except:
        print("O arquivo com o nome informado nao pode ser localizado e/ou aberto")
        quit()

    for linha in fhand: #lendo cada linha do arquivo
        linha = linha.rstrip()
        aux = linha.split()  #quebro a linha em varias strings
        curso = aux[0]
        disciplina = aux[1]
        professor = aux[2]
        num_alunos = int(aux[3])
        turno = aux[4]
        obj1 = Turma(curso, disciplina, professor, num_alunos, turno)  # criando um objeto
        turmas.append(obj1)#adiciono o objeto que foi criado a lista de turmas
        
#============================================================================================================================================
def abre_arq_salas():
    salas1 = input("Informe o nome do arquivo com os dados das salas disponiveis no campus: ")
    #teste para verificacao de arquivos com nomes errados ou inexistentes
    try:
        fhand=open(salas1)
    except:
        print("O arquivo com o nome informado nao pode ser localizado e/ou aberto")
        quit()

    for linha in fhand: #lendo cada linha do arquivo
        linha = linha.rstrip()
        aux = linha.split()  # quebro a linha em varias strings
        sala=aux[0]
        lotacao=int(aux[1])
        obj2 = Sala(sala, lotacao) #criando um obejto do tipo Sala e adicionando o nome da sala e a sua lotacao
        salas.append(obj2)#adiciono o objeto que foi criado a lista de salas
#============================================================================================================================================
#antes de mais nada, informar o arquivo com as salas disponiveis no campus
abre_arq_salas()

num_arq=int(input("Insira o numero de arquivos de demanda que deseja informar: "))
leitura=0
while(True):
    arq=input("Informe o nome do arquivo de demanda de salas: ")
    abre_arq_cursos(arq)
    leitura+=1
    if(leitura == num_arq):
        break
    
menu=True
while (menu==True):
    op=menu_inicial() #chama a funcao do menu
    if (op==1): #Imprimir turmas
        for i in range(len(turmas)):  #percorrendo a lista com as turmas
            turmas[i].imprimir_inf()

    elif(op==2): #Alocacao das salas conforme a demanda ja apresentada
        #criar o objeto tabela hash para separar os turnos
        turnos=tabelaHash()

        #preciso separar as turmas a serem alocadas por turno
        #eu tenho as turmas armazenadas em uma lista
        i=0
        for i in range(len(turmas)):
            #para data de entrega
            if turnos.verificaElemento(turmas[i].get_turno_pref()): #se a chave ja existe no dicionario
                turnos.addElementoRep(turmas[i].get_turno_pref(), i)
            else: #se a chave e nova no dicionario
                turnos.addElementoNovo(turmas[i].get_turno_pref(), i)
        #entao foram separadas todas as turmas em funcao do turno
        #foram gerados todos os vizinhos

        #primeiro avaliar os cursos noturnos
        #separo todas as posicoes correspondentes aos cursos noturnos na lista x 
        x=list()
        i=0
        #todas as posicoes correspondentes as turmas noturnas estao salvas em x
        for i in range(turnos.getTamLista('N')):
            x.append(turnos.getElemLista('N', i))

        #rodar toda a lista de turmas noturnas e comparar com a lista de salas para verificar qual delas tem a menor diferença de demanda e lotacao
        i=0
        for i in range(len(x)):
            diferencaAnterior=44
            salaAtual=0
            demanda = turmas[x[i]].get_num_alunos() #pego o valor corresponte ao numero de alunos de uma determinada turma de curso noturno
            for j in range(len(salas)): #percorrer a lista de salas
                tamSala = salas[j].getLotacao()
                diferenca = tamSala - demanda
                
                if (diferenca < diferencaAnterior and diferenca>=0): #verifico se existe uma sala com a diferenca entre demanda e lotacao melhor que a encontrada em uma iteracao anterior e diferenca positiva
                    salaAtual=j #salvo qual e a posicao da sala que tem a menor diferenca entre a demanda e a lotacao
                    deferencaAnterior=diferenca #salvo a melhor diferenca
            #ja sei qual e a melhor sala para ocupar uma turma
            #agora tenho que verificar os horarios disponiveis para essa sala
            j=0
            for j in range(salas[salaAtual].getTamMatriz()-1): #vou rodar na matriz de horarios da melhor sala encontrada para alocar uma turma noturna. nao posso incluir o sabado
                #j vai rodar nas linhas da matriz. ou seja: dias da semana
                if (salas[salaAtual].verificaElemMatriz(j, 6) == ' '):#6 representa o primeiro horario da noite. se a comparacao for vdd, a sala nesse horario esta vazia
                    salas[salaAtual].addElemento(j, 6, turmas[x[i]]) #adiciono a turma nesse horario 
                    break #quebro o loop do j se a turma for add em um horario
                elif (salas[salaAtual].verificaElemMatriz(j, 7) == ' '):#7 representa o segundo horario da noite. se a comparacao for vdd, a sala nesse horario esta vazia
                    salas[salaAtual].addElemento(j, 7, turmas[x[i]]) #adiciono a turma nesse horario 
                    break #quebro o loop do j se a turma for add em um horario
        del x
        #segundo, avaliar cursos integrais
        # turno manha
        x=list()
        i=0
        #todas as posicoes correspondentes as turmas da manha estao salvas em x
        for i in range(turnos.getTamLista('M')):
            x.append(turnos.getElemLista('M', i))

        #rodar toda a lista de turmas da manha e comparar com a lista de salas para verificar qual delas tem a menor diferença de demanda e lotacao
        i=0
        for i in range(len(x)):
            diferencaAnterior=44
            salaAtual=0
            demanda = turmas[x[i]].get_num_alunos() #pego o valor corresponte ao numero de alunos de uma determinada turma de horario na manha
            for j in range(len(salas)): #percorrer a lista de salas
                tamSala = salas[j].getLotacao()
                diferenca = tamSala - demanda
                if (diferenca < diferencaAnterior and diferenca>=0): #verifico se existe uma sala com a diferenca entre demanda e lotacao melhor que a encontrada em uma iteracao anterior e diferenca positiva
                    salaAtual=j #salvo qual e a posicao da sala que tem a menor diferenca entre a demanda e a lotacao
                    deferencaAnterior=diferenca #salvo a melhor diferenca
            #ja sei qual e a melhor sala para ocupar uma turma
            #agora tenho que verificar os horarios disponiveis para essa sala
            j=0
            for j in range(salas[salaAtual].getTamMatriz()): #vou rodar na matriz de horarios da melhor sala encontrada para alocar uma turma no turno da manha. posso incluir o sabado
                #j vai rodar nas linhas da matriz. ou seja: dias da semana
                if (salas[salaAtual].verificaElemMatriz(j, 0) == ' '):#0 representa o primeiro horario da manha. se a comparacao for vdd, a sala nesse horario esta vazia
                    salas[salaAtual].addElemento(j, 0, turmas[x[i]]) #adiciono a turma nesse horario 
                    break #quebro o loop do j se a turma for add em um horario
                elif (salas[salaAtual].verificaElemMatriz(j, 1) == ' '):#1 representa o segundo horario da manha. se a comparacao for vdd, a sala nesse horario esta vazia
                    salas[salaAtual].addElemento(j, 1, turmas[x[i]]) #adiciono a turma nesse horario 
                    break #quebro o loop do j se a turma for add em um horario
                elif (salas[salaAtual].verificaElemMatriz(j, 2) == ' '):#2 representa o terceiro horario da manha. se a comparacao for vdd, a sala nesse horario esta vazia
                    salas[salaAtual].addElemento(j, 2, turmas[x[i]]) #adiciono a turma nesse horario 
                    break #quebro o loop do j se a turma for add em um horario
        del x

        # turno tarde
        x=list()
        i=0
        #todas as posicoes correspondentes as turmas da tarde estao salvas em x
        for i in range(turnos.getTamLista('T')):
            x.append(turnos.getElemLista('T', i))

        #rodar toda a lista de turmas da tarde e comparar com a lista de salas para verificar qual delas tem a menor diferença de demanda e lotacao
        i=0
        for i in range(len(x)):
            diferencaAnterior=44
            salaAtual=0
            demanda = turmas[x[i]].get_num_alunos() #pego o valor corresponte ao numero de alunos de uma determinada turma de horario na tarde
            for j in range(len(salas)): #percorrer a lista de salas
                tamSala = salas[j].getLotacao()
                diferenca = tamSala - demanda
                if (diferenca < diferencaAnterior and diferenca>=0): #verifico se existe uma sala com a diferenca entre demanda e lotacao melhor que a encontrada em uma iteracao anterior e diferenca positiva
                    salaAtual=j #salvo qual e a posicao da sala que tem a menor diferenca entre a demanda e a lotacao
                    deferencaAnterior=diferenca #salvo a melhor diferenca
            #ja sei qual e a melhor sala para ocupar uma turma
            #agora tenho que verificar os horarios disponiveis para essa sala
            j=0
            for j in range(salas[salaAtual].getTamMatriz()): #vou rodar na matriz de horarios da melhor sala encontrada para alocar uma turma no turno da tarde. posso incluir o sabado
                #j vai rodar nas linhas da matriz. ou seja: dias da semana
                if (salas[salaAtual].verificaElemMatriz(j, 3) == ' '):#3 representa o primeiro horario da tarde. se a comparacao for vdd, a sala nesse horario esta vazia
                    salas[salaAtual].addElemento(j, 3, turmas[x[i]]) #adiciono a turma nesse horario 
                    break #quebro o loop do j se a turma for add em um horario
                elif (salas[salaAtual].verificaElemMatriz(j, 4) == ' '):#4 representa o segundo horario da tarde. se a comparacao for vdd, a sala nesse horario esta vazia
                    salas[salaAtual].addElemento(j, 4, turmas[x[i]]) #adiciono a turma nesse horario 
                    break #quebro o loop do j se a turma for add em um horario
                elif (salas[salaAtual].verificaElemMatriz(j, 5) == ' '):#5 representa o terceiro horario da tarde. se a comparacao for vdd, a sala nesse horario esta vazia
                    salas[salaAtual].addElemento(j, 5, turmas[x[i]]) #adiciono a turma nesse horario 
                    break #quebro o loop do j se a turma for add em um horario
        del x  
        #DEPOIS VERIFICAR A QUESTAO DAS TURMAS QUE NAO FORAM ALOCADAS. GERAR UM ARQUIVO DE SAIDA COM ESSAS INFORMACOES
        i=0
        j=0
        k=0
        for i in range(len(salas)): #percorrendo a lista de salas
            print("========================")
            print("Sala", salas[i].getNome())
            print("========================")
            for j in range(salas[i].getTamMatriz()): #percorrendo a linha da matriz de cada obj Sala salvo na lista de salas
                if j == 0:
                    print("====== \tSegunda-feira\t ======")
                elif j == 1:
                    print("====== \tTerca-feira\t ======")
                elif j == 2:
                    print("====== \tQuarta-feira\t ======")
                elif j == 3:
                    print("====== \tQuinta-feira\t ======")
                elif j == 4:
                    print("====== \tSexta-feira\t ======")
                elif j == 5:
                    print("====== \tSabado\t ======")
                for k in range(salas[i].getTamColuna(j)): #percorrendo a coluna de uma determinada matriz de cada obj Sala salvo na lista de salas
                    if k == 0:
                        if (salas[i].verificaElemMatriz(j, k) == ' '):
                            print("12M: SALA VAZIA")
                        else:
                            print("12M: Curso: ", salas[i].verificaElemMatriz(j, k).get_curso(), "\tDisciplina: ", salas[i].verificaElemMatriz(j, k).get_disciplina())

                    elif k == 1:
                        if (salas[i].verificaElemMatriz(j, k) == ' '):
                            print("34M: SALA VAZIA")
                        else:
                            print("34M: Curso: ", salas[i].verificaElemMatriz(j, k).get_curso(), "\tDisciplina: ", salas[i].verificaElemMatriz(j, k).get_disciplina())

                    elif k == 2:
                        if (salas[i].verificaElemMatriz(j, k) == ' '):
                            print("56M: SALA VAZIA")
                        else:
                            print("56M: Curso: ", salas[i].verificaElemMatriz(j, k).get_curso(), "\tDisciplina: ", salas[i].verificaElemMatriz(j, k).get_disciplina())

                    elif k == 3:
                        if (salas[i].verificaElemMatriz(j, k) == ' '):
                            print("12T: SALA VAZIA")
                        else:
                            print("12T: Curso: ", salas[i].verificaElemMatriz(j, k).get_curso(), "\tDisciplina: ", salas[i].verificaElemMatriz(j, k).get_disciplina())

                    elif k == 4:
                        if (salas[i].verificaElemMatriz(j, k) == ' '):
                            print("34T: SALA VAZIA")
                        else:
                            print("34T: Curso: ", salas[i].verificaElemMatriz(j, k).get_curso(), "\tDisciplina: ", salas[i].verificaElemMatriz(j, k).get_disciplina())

                    elif k == 5:
                        if (salas[i].verificaElemMatriz(j, k) == ' '):
                            print("56T: SALA VAZIA")
                        else:
                            print("56T: Curso: ", salas[i].verificaElemMatriz(j, k).get_curso(), "\tDisciplina: ", salas[i].verificaElemMatriz(j, k).get_disciplina())

                    elif k == 6:
                        if (salas[i].verificaElemMatriz(j, k) == ' '):
                            print("12N: SALA VAZIA")
                        else:
                            print("12N: Curso: ", salas[i].verificaElemMatriz(j, k).get_curso(), "\tDisciplina: ", salas[i].verificaElemMatriz(j, k).get_disciplina())

                    elif k == 7:
                        if (salas[i].verificaElemMatriz(j, k) == ' '):
                            print("34N: SALA VAZIA")
                        else:
                            print("34N: Curso: ", salas[i].verificaElemMatriz(j, k).get_curso(), "\tDisciplina: ", salas[i].verificaElemMatriz(j, k).get_disciplina())
        del turnos
    elif (op==0): #Sair
        print("Saindo...")
        salas.clear() #apagando a lista com as salas do campus
        turmas.clear() #apagando a lista com as turmas
        break #quebra o loop do menu
        
    else: #Opcao invalida
        print("Opcao invalida!")
