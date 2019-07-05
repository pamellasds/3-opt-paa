# -*- coding: utf-8 -*-
import numpy as np
import random
import operator
import itertools
import time
import pandas as pd
from sklearn import manifold 
import matplotlib.pyplot as plt


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

    
def caminho_inicial(matriz):
    caminho = np.array(range(0, len(matriz)))
    random.shuffle(caminho)
    caminho = np.append(caminho, caminho[0])
    #print (caminho)
    return caminho
    

#caminho_inicial(matriz_dist)

def custo_ver(caminho, matriz):
    soma = 0
    for i in range(0, len(caminho)-1):
        m = caminho[i]
        n = caminho[i+1]
        soma = soma + matriz[m,n]
        #print(caminho)
        #print(matriz)
        #print(m,n)
        #print(matriz[m,n])
    return soma


def kopt(matriz_distancias):
    #Entrada: Matriz de Distancias
    #Saida: Solucao encontrada e custo de caminho

    n = len(matriz_dist)

    #Faz um caminho inicial (TRIVIAL)
    ciclo = caminho_inicial(matriz_distancias)

    
    #Calcula o custo inicial
    custo_ciclo = custo_ver(ciclo, matriz_distancias)
    
    #Define o Numero de Tentativas
    k_max = max(10, int(n/5))
    
    #Repete para o numero de Tentativas
    for Tentativas in range(0, k_max):

        #Seleciona 3 vertices nao adjacentes a,b e c


        #Converte ciclo para list e acha A e o Index de A
        copia_ciclo = ciclo.tolist()
        copia_ciclo.pop(n)
        a = random.choice(range(0, n))
        i_a = copia_ciclo.index(a)

        #print(a, i_a)
        #print(copia_ciclo)

        #Acha as cidades adjacentes de A
        suc_a = copia_ciclo[(i_a + 1)%len(copia_ciclo)]
        ant_a = copia_ciclo[(i_a -1)%len(copia_ciclo)]

        #Remover as cidades adjacentes de A da copia do ciclo

        copia_ciclo.pop(copia_ciclo.index(suc_a))
        copia_ciclo.pop(copia_ciclo.index(ant_a))
        copia_ciclo.pop(copia_ciclo.index(a))

        #print(copia_ciclo)


        #Achar o b e os adjacentes dele

        b = random.choice(copia_ciclo)
        i_b = copia_ciclo.index(b)

        #print(b, i_b)

        suc_b = copia_ciclo[(i_b + 1)%len(copia_ciclo)]
        ant_b = copia_ciclo[(i_b -1)%len(copia_ciclo)]


        #Remover B os Adjacentes
        copia_ciclo.pop(copia_ciclo.index(suc_b))
        copia_ciclo.pop(copia_ciclo.index(ant_b))
        copia_ciclo.pop(copia_ciclo.index(b))

        #print(copia_ciclo)

        c = random.choice(copia_ciclo)
        #print(c)  
        i_c = ciclo.tolist().index(c)


        verti = [i_a, i_b,i_c]
        v1 = min(verti)
        verti.pop(verti.index(v1))
        v2 = min(verti)
        verti.pop(verti.index(v2))
        v3 = min(verti)

        a, b, c = ciclo[v1], ciclo[v2], ciclo[v3]

        
        #Caclular os outros  outros 3 vertices x,y e z

        i_a = ciclo.tolist().index(a)
        i_b = ciclo.tolist().index(b)
        i_c = ciclo.tolist().index(c)
        i_x = (i_a+1)%n
        i_y = (i_b+1)%n
        i_z = (i_c+1)%n


        x = ciclo[(i_a+1)%n]
        y = ciclo[(i_b+1)%n]
        z = ciclo[(i_c+1)%n]

        #print(a,x,b,y,c,z)
        #print(a,b,c,d,e,f)

        #PLotar Arestas AX BY CZ

        #Faz as Permutacoes

        #print(ciclo[:i_a + 1].shape)
        #print(ciclo[i_x : i_b + 1].shape)
        #print(ciclo[i_c : i_y -1 : -1].shape)
        #print(ciclo[i_z:].shape)
 
        copia_ciclo = ciclo.tolist()

        c1 = copia_ciclo[:i_a+1] + copia_ciclo[i_x : i_b+1] + copia_ciclo[i_c : i_y -1 : -1] + copia_ciclo[i_z:] # 2-opt

        c2 = copia_ciclo[:i_a+1] + copia_ciclo[i_b:i_x-1:-1] + copia_ciclo[i_y:i_c+1] + copia_ciclo[i_z:] # 2-opt

        c3 = copia_ciclo[:i_a+1] + copia_ciclo[i_b:i_x-1:-1] + copia_ciclo[i_c:i_y-1:-1] + copia_ciclo[i_z:] # 3-opt

        c4 = copia_ciclo[:i_a+1] + copia_ciclo[i_y:i_c+1]    + copia_ciclo[i_x:i_b+1]    + copia_ciclo[i_z:] # 3-opt

        c5 = copia_ciclo[:i_a+1] + copia_ciclo[i_y:i_c+1]    + copia_ciclo[i_b:i_x-1:-1] + copia_ciclo[i_z:] # 3-opt

        c6 = copia_ciclo[:i_a+1] + copia_ciclo[i_c:i_y-1:-1] + copia_ciclo[i_x:i_b+1]    + copia_ciclo[i_z:] # 3-opt

        c7 = copia_ciclo[:i_a+1] + copia_ciclo[i_c:i_y-1:-1] + copia_ciclo[i_b:i_x-1:-1] + copia_ciclo[i_z:] # 2-opt


        #Acha a menor combinacao e menor custo
        permutacoes = [c1,c2,c3,c4,c5,c6,c7]
        custos = []
        for p in permutacoes:
            custos.append(custo_ver(p, matriz_distancias))
        minimo = min(custos)
        
        #Atualiza CICLO E CUSTO_CICLO se o novo valor for menor que eles
        if(minimo < custo_ciclo):
            ciclo = np.array(permutacoes[custos.index(minimo)])
            custo_ciclo = minimo

        #Plot da NOVA 
        #print(ciclo)
        #print(Tentativas)
    return ciclo, custo_ciclo           

def location(cidades, N):
    mds =  manifold.MDS(2, dissimilarity='euclidean')
    coords = mds.fit_transform(cidades)
    x_vertice, y_vertice = coords[:, 0], coords[:, 1]
    x_aresta, y_aresta = coords[:, 0], coords[:, 1];
    cities = []

    for i in range(N):
        cities.append(i)
    
    return x_vertice, y_vertice, x_aresta, y_aresta, cities            

def plot_ciclo_inicial(x_vertice, y_vertice, x_aresta, y_aresta, cities, N):
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(x_vertice, y_vertice, color ='black')
    for i in range(N): 
        ax.annotate(cities[i], (x_vertice[i], y_vertice[i]))
        plt.arrow(x_aresta[i-1], y_aresta[i-1], (x_aresta[i] - x_aresta[i-1]), (y_aresta[i] - y_aresta[i-1]), color ='red', length_includes_head=True)
    plt.show()
    
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
Arquivos = ['datasets/Tsp26t2.txt', 'datasets/Tsp58t1.txt', 'datasets/Tsp280t2.txt', 'datasets/Tsp535t2.txt', 'datasets/Tsp1379t2.txt']

for arq in Arquivos:
    matriz_dist, N = entrada(arq)
    tempos_de_execucao = []
    resultados_obtidos = []
    caminhos_obtidos = []
    melhor_caminho = []
    melhor_resultado = 0
    for i in range(0, 100):
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
    d = {'Resultado': resultados_obtidos, 'Tempo': tempos_de_execucao, 'Caminho': caminhos_obtidos}
    df = pd.DataFrame(data=d)
    dadosPlanilhas.append(df)
    print("Fim do Arquivo: ", arq)


#Tsp26t2.txt
#matriz_dist, N = entrada('datasets/Tsp26t2.txt')   
#ciclo, custo_ciclo = kopt(matriz_dist)
#print(ciclo, custo_ciclo)    
#x_vertice, y_vertice, x_aresta, y_aresta, cities = location(matriz_dist, N)
#plot_ciclo_inicial(x_vertice, y_vertice, x_aresta, y_aresta, cities, N)
#plot_melhor_caminho(x_vertice, y_vertice, x_aresta, y_aresta, cities, N, ciclo)

#Tsp58t1.txt
#matriz_dist, N = entrada('datasets/Tsp58t1.txt')   
#ciclo, custo_ciclo = kopt(matriz_dist)
#print(ciclo, custo_ciclo)    
#x_vertice, y_vertice, x_aresta, y_aresta, cities = location(matriz_dist, N)
#plot_ciclo_inicial(x_vertice, y_vertice, x_aresta, y_aresta, cities, N)
#plot_melhor_caminho(x_vertice, y_vertice, x_aresta, y_aresta, cities, N, ciclo)

#Tsp280t2.txt
#Algumas vezes o plot não dar certo, em outras dar. Vou verificar pq só esse dar certo em alguns caso
#matriz_dist, N = entrada('datasets/Tsp280t2.txt')   
#ciclo, custo_ciclo = kopt(matriz_dist)
#print(ciclo, custo_ciclo)   
#x_vertice, y_vertice, x_aresta, y_aresta, cities = location(matriz_dist, N)
#plot_ciclo_inicial(x_vertice, y_vertice, x_aresta, y_aresta, cities, N)
#plot_melhor_caminho(x_vertice, y_vertice, x_aresta, y_aresta, cities, N, ciclo)

#Tsp535t2.txt
#matriz_dist, N = entrada('datasets/Tsp535t2.txt')   
#ciclo, custo_ciclo = kopt(matriz_dist)
#print(ciclo, custo_ciclo)    
#x_vertice, y_vertice, x_aresta, y_aresta, cities = location(matriz_dist, N)
#plot_ciclo_inicial(x_vertice, y_vertice, x_aresta, y_aresta, cities, N)
#plot_melhor_caminho(x_vertice, y_vertice, x_aresta, y_aresta, cities, N, ciclo) 
    
#tsp10t3.txt
#matriz_dist, N = entrada('datasets/tsp10t3.txt')   
#ciclo, custo_ciclo = kopt(matriz_dist)
#print(ciclo, custo_ciclo) 
#x_vertice, y_vertice, x_aresta, y_aresta, cities = location(matriz_dist, N)
#plot_ciclo_inicial(x_vertice, y_vertice, x_aresta, y_aresta, cities, N)
#plot_melhor_caminho(x_vertice, y_vertice, x_aresta, y_aresta, cities, N, ciclo)

nomes = ['26t2', '58t1', '280t2', '535t2', '1379t2']
i = 0
with pd.ExcelWriter('ResultadosPAA_10_n5.xlsx') as writer:
    for dfr in dadosPlanilhas:        
       dfr.to_excel(writer, sheet_name=nomes[i])
       i = i + 1
        
print("Fim") 

 
        







































