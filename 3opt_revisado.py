# -*- coding: utf-8 -*-
import numpy as np
import random
import operator
import itertools
import time
import pandas as pd
from sklearn import manifold 
import matplotlib.pyplot as plt

#Geracao de Vertices Validos paras as Combinacoes 3 a 3
#Faz a Geracao Completa, Melhor usar para instancias Rapidas
def Combinacoes(N, s):

    return((i,j,k)
        for i in range(s, N)
            for j in range(i+2, N)
                for k in range(j+2, N+(i>0))    
    )

#Geracao de Vertices Validos para as Combinacoes 3 a 3
#Gera N combinacoes 3a3, espalhadas pelo espaço de combinacoes validas, Usamo mais para instancias Demoradas
def Combinacoes2(N):
    combina = []
    for a in range(N-4):
        #print(a)
        rb = range(a+2, N-2)
        b = random.choice(rb)
        rc = range(b+2, N+(i>0))
        c = random.choice(rc)
        aux = [a, b, c]
        combina.append(aux)
        #print(combina)
    return combina




#Recebe o nome/endereco do Arquivo e Devolve a Matriz de Distancia e Tamanho da Amostra
def entrada(nome_arq):
    #Abrir o Arquivo
    arq = open(nome_arq, 'r')
    
    #Recupera o tipo e o tamanho do grafo
    texto = arq.readline()
    split = texto.split()
    N = int(split[0].split('=')[1])
    tipo = int(split[1].split('=')[1])
    
    cidades = np.empty((N,N), dtype = float)
    
    #Para Tipo = 1
    if tipo == 1:
        for i in range(0, N):
            texto = arq.readline()
            split = texto.split()
            cidades[i,i] = 0
            count = 0
            for j in range(i+1, N):
                cidades[i,j] = int(split[count])
                cidades[j,i] = cidades[i,j]
                count = count + 1  
    
    
    #Para Tipo = 2
    if tipo == 2:
        vetX = np.empty((N,1))
        vetY = np.empty((N,1))
        for i in range(0, N):
            texto = arq.readline()
            split = texto.split()
            
            vetX[i] = float(split[0])
            vetY[i] = float(split[1])   
            
        for i in range(0, N):
            for j in range(0, N):
                                
                x = vetX[i] - vetX[j]
                y = vetY[i] - vetY[j]
                cidades[i,j] = ((x**2) + (y**2))**(1/2)
                
                
    
    
    #Para tipo = 3
    if tipo == 3:
        for i in range(0, N):
            texto = arq.readline()
            split = texto.split()
            for j in range(0, N):
                cidades[i,j] = int(split[j])
    arq.close()

    return cidades, N

#Cria um Caminho Inicial Aleatorio    
def caminho_inicial(matriz):
    caminho = np.array(range(0, len(matriz)))
    random.shuffle(caminho)
    caminho = np.append(caminho, caminho[0])
    return caminho
    
#Dado um Ciclo e uma Matriz de Distancia Avalia o CUSTO do ciclo
def custo_ver(caminho, matriz):
    soma = 0
    for i in range(0, len(caminho)-1):
        m = caminho[i]
        n = caminho[i+1]
        soma = soma + matriz[m,n]

    return soma


#3OPT
def kopt(matriz_distancias):
    #Entrada: Matriz de Distancias
    #Saida: Solucao encontrada e custo de caminho

    #Salva N
    n = len(matriz_dist)

    #Faz um caminho inicial
    ciclo = caminho_inicial(matriz_distancias)

    
    #Calcula o custo inicial
    custo_ciclo = custo_ver(ciclo, matriz_distancias)
    
    #Define o Numero de Tentativas
    k_max = max(10, int(n/5))
    
  
    #Repete para o numero de Tentativas
    for Tentativas in range(0, k_max):
        #Contador pra Limitar o Numero de Combinacoes
        count = 0
        

        #Vasculha as combinações de arestas naquele ciclo, até o limite de count
        #Possuem duas versoes, uma que vasculha todas as combinacoes validas e outra que pega só uma amostra delas
        #for comb in Combinacoes(n, random.choice(range(n))):
        for comb in Combinacoes2(n):
            #testa N combinacoes dispersas de arestas para serem removidas
            
            #A partir dos dados da combinacao atual Identifica as Arestas que vao ser revomvidas
            i_a, i_b,i_c = comb      
            i_x = (i_a+1)%n
            i_y = (i_b+1)%n
            i_z = (i_c+1)%n

            copia_ciclo = ciclo.tolist()

            #Gera as Perturbacoes de vom base nas arestas
            c1 = copia_ciclo[:i_a+1] + copia_ciclo[i_x : i_b+1] + copia_ciclo[i_c : i_y -1 : -1] + copia_ciclo[i_z:] # 2-opt

            c2 = copia_ciclo[:i_a+1] + copia_ciclo[i_b:i_x-1:-1] + copia_ciclo[i_y:i_c+1] + copia_ciclo[i_z:] # 2-opt

            c3 = copia_ciclo[:i_a+1] + copia_ciclo[i_b:i_x-1:-1] + copia_ciclo[i_c:i_y-1:-1] + copia_ciclo[i_z:] # 3-opt

            c4 = copia_ciclo[:i_a+1] + copia_ciclo[i_y:i_c+1]    + copia_ciclo[i_x:i_b+1]    + copia_ciclo[i_z:] # 3-opt

            c5 = copia_ciclo[:i_a+1] + copia_ciclo[i_y:i_c+1]    + copia_ciclo[i_b:i_x-1:-1] + copia_ciclo[i_z:] # 3-opt

            c6 = copia_ciclo[:i_a+1] + copia_ciclo[i_c:i_y-1:-1] + copia_ciclo[i_x:i_b+1]    + copia_ciclo[i_z:] # 3-opt

            c7 = copia_ciclo[:i_a+1] + copia_ciclo[i_c:i_y-1:-1] + copia_ciclo[i_b:i_x-1:-1] + copia_ciclo[i_z:] # 2-opt


            #Acha o ciclo de menor custo
            permutacoes = [c1,c2,c3,c4,c5,c6,c7]
            custos = []
            for p in permutacoes:
                custos.append(custo_ver(p, matriz_distancias))
            minimo = min(custos)
            
            #Atualiza CICLO E CUSTO_CICLO para a proxima tentativa/combinacao se o novo valor for menor que eles
            if(minimo < custo_ciclo):
                ciclo = np.array(permutacoes[custos.index(minimo)])
                custo_ciclo = minimo
            
            #Limite de Combinacoes
            #Espaco de Posibildiades Muito grande, N e K_max geram alguns resultados bons, mas precisa investir muito
            count = count + 1
            if count >= n:
                break
            
    return ciclo, custo_ciclo           

#Plotagem
def location(cidades, N):
    mds =  manifold.MDS(2, dissimilarity='euclidean')
    coords = mds.fit_transform(cidades)
    x_vertice, y_vertice = coords[:, 0], coords[:, 1]
    x_aresta, y_aresta = coords[:, 0], coords[:, 1];
    cities = []

    for i in range(N):
        cities.append(i)
    
    return x_vertice, y_vertice, x_aresta, y_aresta, cities            

#Plotagem
def plot_ciclo_inicial(x_vertice, y_vertice, x_aresta, y_aresta, cities, N):
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(x_vertice, y_vertice, color ='black')
    for i in range(N): 
        ax.annotate(cities[i], (x_vertice[i], y_vertice[i]))
        plt.arrow(x_aresta[i-1], y_aresta[i-1], (x_aresta[i] - x_aresta[i-1]), (y_aresta[i] - y_aresta[i-1]), color ='red', length_includes_head=True)
    plt.show()

#Plotagem    
def plot_melhor_caminho(x_vertice, y_vertice, x_aresta, y_aresta, cities, N, ciclo):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(x_vertice, y_vertice, color ='black') 
 
    for i in range(N):  
        ax.annotate(cities[i], (x_vertice[i], y_vertice[i])) 
        
        if i == 0: 
            plt.arrow(x_aresta[ciclo[N - 1]], y_aresta[ciclo[N - 1]], (x_aresta[ciclo[i]] - x_aresta[ciclo[N - 1]]), (y_aresta[ciclo[i]] - y_aresta[ciclo[N - 1]]), color ='blue', length_includes_head=True)
        else: 
            plt.arrow(x_aresta[ciclo[i - 1]], y_aresta[ciclo[i - 1]], (x_aresta[ciclo[i]] - x_aresta[ciclo[i - 1]]), (y_aresta[ciclo[i]] - y_aresta[ciclo[i - 1]]), color ='blue', length_includes_head=True)
    plt.show()    
            


#Etapa de Geração dos Saidas Medias
dadosPlanilhas = []
Arquivos = ['datasets/tsp10t3.txt','datasets/tsp12t2.txt','datasets/Tsp26t2.txt','datasets/Tsp58t1.txt','datasets/Tsp280t2.txt','datasets/Tsp535t2.txt']

#Roda os Arquivos N vezes e armazena os resultados para por na planilha
for arq in Arquivos:
    matriz_dist, N = entrada(arq)
    tempos_de_execucao = []
    resultados_obtidos = []
    caminhos_obtidos = []
    melhor_caminho = []
    melhor_resultado = 0
    for i in range(0, 5):
        start = time.time()
        ciclo, custo_ciclo = kopt(matriz_dist)
        end = time.time()
        if(i == 0):
            melhor_resultado = custo_ciclo
            melhor_caminho = ciclo
        if(custo_ciclo < melhor_resultado):
            melhor_resultado = custo_ciclo
            melhor_caminho = ciclo
        tempos_de_execucao.append(end-start)
        resultados_obtidos.append(custo_ciclo)
        caminhos_obtidos.append(ciclo)
        print('Concluido Round: ', i, 'do arquivo: ', arq)
        print('Melhor resultado ate o momento: ', melhor_resultado)
        print(' ')
    d = {'Resultado': resultados_obtidos, 'Tempo': tempos_de_execucao, 'Caminho': caminhos_obtidos}
    df = pd.DataFrame(data=d)
    dadosPlanilhas.append(df)
    print("Fim do Arquivo: ", arq)


#Salva os dados na Planilha
nomes = ['10', '12', '26', '58', '280', '535']
i = 0
with pd.ExcelWriter('teste_paa.xlsx') as writer:
    for dfr in dadosPlanilhas:        
       dfr.to_excel(writer, sheet_name=nomes[i])
       i = i + 1
        
print("Fim") 

 
        







































