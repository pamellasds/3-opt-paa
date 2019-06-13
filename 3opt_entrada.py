# -*- coding: utf-8 -*-
import numpy as np
import random
import operator
import itertools

def entrada(nome_arq):
    #Abrir o Arquivo
    arq = open(nome_arq, 'r')
    
    #Recupera o tipo e o tamanho do grafo
    texto = arq.readline()
    split = texto.split()#http://localhost:8888/notebooks/3opt.ipynb#
    N = int(split[0].split('=')[1])
    tipo = int(split[1].split('=')[1])
    
    cidades = np.empty((N,N), dtype = int)
    
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

    return cidades


def custo_caminho_inicial(matriz_cidades):
    custo = 0
    for i in range(0, matriz_cidades.shape[0]-1):
        custo = custo + matriz_cidades[i,i+1]
        if i+1 == matriz_cidades.shape[0]-1:
           custo = custo + matriz_cidades[matriz_cidades.shape[0]-1,0]
    return custo


def escolher_arestas_iniciais(matriz_cidades):
    vertice_x_y_z=[]
    vertice_a_b_c=[]
    vertice = random.randrange(0,matriz_cidades.shape[0], 2)
    vertice_a_b_c.append(vertice)
    while len(vertice_a_b_c)<3:
        vertice = random.randrange(0,matriz_cidades.shape[0], 2) #escolhendo três (n) vértices aleatórios
        if not(vertice in vertice_a_b_c):
            vertice_a_b_c.append(vertice)
    [vertice_x_y_z.append((vertice_a_b_c[i])+1) for i in range(0,3)] #encontrando os vertices próximos (n+1) para formar aresta
    return vertice_a_b_c, vertice_x_y_z 

    
def gerar_combinacoes(matriz_cidades, vertice_a_b_c_aux, vertice_x_y_z_aux):
    distancia=[]
    arestas=[]

    #arestas a serem trocadas
    distancia.append(matriz_cidades[vertice_a_b_c_aux[0], vertice_x_y_z_aux[0]] + matriz_cidades[vertice_a_b_c_aux[1], vertice_x_y_z_aux[1]] + matriz_cidades[vertice_a_b_c_aux[2], vertice_x_y_z_aux[2]])
    arestas.append([[vertice_a_b_c_aux[0], vertice_x_y_z_aux[0]], [vertice_a_b_c_aux[1], vertice_x_y_z_aux[1]], [vertice_a_b_c_aux[2], vertice_x_y_z_aux[2]]])
    #primeira permutação
    distancia.append(matriz_cidades[vertice_a_b_c_aux[0], vertice_x_y_z_aux[2]] + matriz_cidades[vertice_a_b_c_aux[2], vertice_x_y_z_aux[0]] + matriz_cidades[vertice_a_b_c_aux[1], vertice_x_y_z_aux[1]])
    arestas.append([[vertice_a_b_c_aux[0], vertice_x_y_z_aux[2]], [vertice_a_b_c_aux[2], vertice_x_y_z_aux[0]], [vertice_a_b_c_aux[1], vertice_x_y_z_aux[1]]])
    #segunda permutação
    distancia.append(matriz_cidades[vertice_a_b_c_aux[0], vertice_x_y_z_aux[0]] + matriz_cidades[vertice_a_b_c_aux[1], vertice_x_y_z_aux[2]] + matriz_cidades[vertice_a_b_c_aux[2], vertice_x_y_z_aux[1]])
    arestas.append([[vertice_a_b_c_aux[0], vertice_x_y_z_aux[0]], [vertice_a_b_c_aux[1], vertice_x_y_z_aux[2]], [vertice_a_b_c_aux[2], vertice_x_y_z_aux[1]]])
    #terceira permutação
    distancia.append(matriz_cidades[vertice_a_b_c_aux[0], vertice_a_b_c_aux[1]] + matriz_cidades[vertice_x_y_z_aux[0], vertice_x_y_z_aux[1]] + matriz_cidades[vertice_a_b_c_aux[2], vertice_x_y_z_aux[2]])
    arestas.append([[vertice_a_b_c_aux[0], vertice_x_y_z_aux[1]], [vertice_a_b_c_aux[0], vertice_x_y_z_aux[1]], [vertice_a_b_c_aux[2], vertice_x_y_z_aux[2]]])
    #quarta permutação
    distancia.append(matriz_cidades[vertice_a_b_c_aux[0], vertice_a_b_c_aux[1]] + matriz_cidades[vertice_x_y_z_aux[2], vertice_x_y_z_aux[1]] + matriz_cidades[vertice_a_b_c_aux[2], vertice_x_y_z_aux[0]])
    arestas.append([[vertice_a_b_c_aux[0], vertice_x_y_z_aux[1]], [vertice_a_b_c_aux[2], vertice_x_y_z_aux[1]], [vertice_a_b_c_aux[2], vertice_x_y_z_aux[0]]])
    #quinta permutação
    distancia.append(matriz_cidades[vertice_a_b_c_aux[0], vertice_a_b_c_aux[2]] + matriz_cidades[vertice_x_y_z_aux[0], vertice_x_y_z_aux[1]] + matriz_cidades[vertice_x_y_z_aux[2], vertice_a_b_c_aux[1]])
    arestas.append([[vertice_a_b_c_aux[0], vertice_a_b_c_aux[2]], [vertice_x_y_z_aux[0], vertice_x_y_z_aux[1]], [vertice_x_y_z_aux[2], vertice_a_b_c_aux[1]]])
    #sexta permutação
    distancia.append(matriz_cidades[vertice_a_b_c_aux[0], vertice_x_y_z_aux[1]] + matriz_cidades[vertice_x_y_z_aux[2], vertice_x_y_z_aux[0]] + matriz_cidades[vertice_a_b_c_aux[2], vertice_a_b_c_aux[2]])
    arestas.append([[vertice_a_b_c_aux[0], vertice_x_y_z_aux[1]], [vertice_x_y_z_aux[2], vertice_x_y_z_aux[0]], [vertice_a_b_c_aux[2], vertice_a_b_c_aux[2]]])
    #sétima permutação
    distancia.append(matriz_cidades[vertice_a_b_c_aux[0], vertice_x_y_z_aux[1]] + matriz_cidades[vertice_x_y_z_aux[0], vertice_a_b_c_aux[2]] + matriz_cidades[vertice_a_b_c_aux[1], vertice_a_b_c_aux[2]])
    arestas.append([[vertice_a_b_c_aux[0], vertice_x_y_z_aux[1]], [vertice_x_y_z_aux[0], vertice_a_b_c_aux[2]], [vertice_a_b_c_aux[1], vertice_a_b_c_aux[2]]])

    return distancia, arestas

def escolher_melhor_troca(arestas,distancia):
    return arestas[distancia.index(min(distancia))], min(distancia)



print(custo_caminho_inicial(entrada('datasets/tsp10t3_teste.txt')))
vertice_a_b_c_aux, vertice_x_y_z_aux = escolher_arestas_iniciais(entrada('datasets/tsp10t3_teste.txt'))
print(vertice_a_b_c_aux, vertice_x_y_z_aux)
distancia, arestas = gerar_combinacoes(entrada('datasets/tsp10t3_teste.txt'), vertice_a_b_c_aux, vertice_x_y_z_aux)
print(distancia, arestas)
arestas_sub, melhor_distancia = escolher_melhor_troca(distancia, arestas)

