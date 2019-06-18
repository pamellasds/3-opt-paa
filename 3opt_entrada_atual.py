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
    split = texto.split()
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


def caminho_inicial(matriz_cidades):
    custo = 0
    caminho=[]
    for i in range(0, matriz_cidades.shape[0]-1):
        custo = custo + matriz_cidades[i,i+1]
        caminho.append([i,i+1])
        if i+1 == matriz_cidades.shape[0]-1:
           caminho.append([matriz_cidades.shape[0]-1,0])
           custo = custo + matriz_cidades[matriz_cidades.shape[0]-1,0]
    return custo, caminho

def escolher_arestas_iniciais_(matriz_cidades, caminho):
    n_arestas=[]
    arestas=[]    
    while len(n_arestas) < 3:
        aleat = random.randrange(0,matriz_cidades.shape[0], 2) #escolhendo três (n) vértices aleatórios (pares)
        if not (aleat in n_arestas):
            n_arestas.append(aleat) 
            arestas.append(caminho[aleat])    
    return arestas

def custo_inicial(matriz_cidades, arestas):
    custo_ini = 0
    for i in range(0, 3):
        custo_ini = custo_ini + matriz_cidades[arestas[i][0], arestas[i][1]]

    return custo_ini
    


def gerar_combinacoes_(matriz_cidades, arestas):
    distancia=[]
    arestas_sub=[]

    #primeira troca
    distancia.append(matriz_cidades[arestas[0][0], arestas[2][0]] + 
    matriz_cidades[arestas[1][1], arestas[1][0]] + 
    matriz_cidades[arestas[0][1], arestas[2][1]])
   
    arestas_sub.append([[arestas[0][0], arestas[2][0]], 
    [arestas[1][1], arestas[1][0]], 
    [arestas[0][1], arestas[2][1]]])

    #segunda troca
    distancia.append(matriz_cidades[arestas[0][0], arestas[0][1]] + 
    matriz_cidades[arestas[1][0], arestas[2][0]] + 
    matriz_cidades[arestas[1][1], arestas[2][1]])
   
    arestas_sub.append([[arestas[0][0], arestas[0][1]], 
    [arestas[1][0], arestas[2][0]], 
    [arestas[1][1], arestas[2][1]]])

    #terceira troca
    distancia.append(matriz_cidades[arestas[0][0], arestas[1][0]] + 
    matriz_cidades[arestas[0][1], arestas[1][1]] + 
    matriz_cidades[arestas[2][0], arestas[2][1]])
   
    arestas_sub.append([[arestas[0][0], arestas[1][0]], 
    [arestas[0][1], arestas[1][1]], 
    [arestas[2][0], arestas[2][1]]])

    #quarta troca
    distancia.append(matriz_cidades[arestas[0][0], arestas[1][0]] + 
    matriz_cidades[arestas[0][1], arestas[2][0]] + 
    matriz_cidades[arestas[1][1], arestas[2][1]])
   
    arestas_sub.append([[arestas[0][0], arestas[1][0]], 
    [arestas[0][1], arestas[2][0]], 
    [arestas[1][1], arestas[2][1]]])

    #quinta troca
    distancia.append(matriz_cidades[arestas[0][0], arestas[2][0]] + 
    matriz_cidades[arestas[1][1], arestas[0][1]] + 
    matriz_cidades[arestas[1][0], arestas[2][1]])
   
    arestas_sub.append([[arestas[0][0], arestas[2][0]], 
    [arestas[1][1], arestas[0][1]], 
    [arestas[1][0], arestas[2][1]]])

    #sexta troca
    distancia.append(matriz_cidades[arestas[0][0], arestas[1][1]] + 
    matriz_cidades[arestas[2][0], arestas[1][0]] + 
    matriz_cidades[arestas[0][1], arestas[2][1]])
   
    arestas_sub.append([[arestas[0][0], arestas[1][1]], 
    [arestas[2][0], arestas[1][0]], 
    [arestas[0][1], arestas[2][1]]])

    #sétima troca
    distancia.append(matriz_cidades[arestas[0][0], arestas[1][1]] + 
    matriz_cidades[arestas[2][0], arestas[0][1]] + 
    matriz_cidades[arestas[1][0], arestas[2][1]])
   
    arestas_sub.append([[arestas[0][0], arestas[1][1]], 
    [arestas[2][0], arestas[0][1]], 
    [arestas[1][0], arestas[2][1]]])

    return distancia, arestas_sub           

def escolher_melhor_troca(distancia, arestas_sub):
    return min(distancia), arestas_sub[distancia.index(min(distancia))]

def subst(caminho, arestas, arestas_sub):
    caminho[caminho.index(arestas[0])] = arestas_sub[0]
    caminho[caminho.index(arestas[1])] = arestas_sub[1]
    caminho[caminho.index(arestas[2])] = arestas_sub[2]
    
    return caminho

    
matriz_dist = entrada('datasets/tsp12t2.txt')
custo, caminho = caminho_inicial(matriz_dist)
print("CAMINHO: {} | CUSTO: {}".format(caminho, custo))

i=0
while(i <= len(matriz_dist[0])/5):
    arestas = escolher_arestas_iniciais_(matriz_dist, caminho)
    custo_ini = custo_inicial(matriz_dist, arestas)

    print("Arestas a serem trocadas: {}".format(arestas), custo_ini)
    distancia, combinacoes = gerar_combinacoes_(matriz_dist, arestas)
    melhor_troca, arestas_sub = escolher_melhor_troca(distancia, combinacoes)

    if melhor_troca > custo_ini:
        melhor_troca = custo_ini
        arestas_sub = arestas

    print("Arestas com melhor custo: {}".format(arestas_sub), melhor_troca)

    custo = custo - custo_ini + melhor_troca


    caminho = subst(caminho, arestas, arestas_sub)
    print("CAMINHO: {} | CUSTO: {}".format(caminho, custo))
    i += 1


def caminho_inicial(matriz):
    caminho = np.array(range(0, len(matriz)))
    caminho = np.append(caminho, 0)
    #print (caminho)
    return caminho
    

#caminho_inicial(matriz_dist)

def custo_ver(caminho, matriz):
    soma = 0
    for i in range(0, len(caminho)-1):
        m = caminho[i]
        n = caminho[i+1]
        soma = soma + matriz[m,n]
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
    k_max = max(5, int(n/10))
    
    #Repete para o numero de Tentativas
    for Tentativas in range(0, k_max):

        print(Tentativas)


        #Seleciona 3 vertices nao adjacentes a,b e c

        #Converte ciclo para list e acha A e o Index de A
        copia_ciclo = ciclo.tolist()
        copia_ciclo.pop(n)
        a = random.choice(range(0, n))
        i_a = copia_ciclo.index(a)

        print(a, i_a)
        print(copia_ciclo)

        #Acha as cidades adjacentes de A
        suc_a = copia_ciclo[(i_a + 1)%len(copia_ciclo)]
        ant_a = copia_ciclo[(i_a -1)%len(copia_ciclo)]

        #Remover as cidades adjacentes de A da copia do ciclo

        copia_ciclo.pop(copia_ciclo.index(suc_a))
        copia_ciclo.pop(copia_ciclo.index(ant_a))
        copia_ciclo.pop(copia_ciclo.index(a))

        print(copia_ciclo)


        #Achar o b e os adjacentes dele

        b = random.choice(copia_ciclo)
        i_b = copia_ciclo.index(b)

        print(b, i_b)

        suc_b = copia_ciclo[(i_b + 1)%len(copia_ciclo)]
        ant_b = copia_ciclo[(i_b -1)%len(copia_ciclo)]


        #Remover B os Adjacentes
        copia_ciclo.pop(copia_ciclo.index(suc_b))
        copia_ciclo.pop(copia_ciclo.index(ant_b))
        copia_ciclo.pop(copia_ciclo.index(b))

        print(copia_ciclo)

        c = random.choice(copia_ciclo)
        print(c)     

        
        #Caclular os outros  outros 3 vertices x,y e z

        i_a = ciclo.tolist().index(a)
        i_b = ciclo.tolist().index(b)
        i_c = ciclo.tolist().index(c)

        x = ciclo[(i_a+1)%n]
        y = ciclo[(i_b+1)%n]
        z = ciclo[(i_c+1)%n]

        #print(a,b,c,x,y,z)

        #PLotar Arestas AX BY CZ

        #Faz as Permutacoes
        c1 = [a,x,b,c,y,z,a]
        c2 = [a,b,x,y,c,z,a]
        c3 = [a,b,x,c,y,z,a]
        c4 = [a,y,c,x,b,z,a]
        c5 = [a,y,c,b,x,z,a]
        c6 = [a,c,y,x,b,z,a]
        c7 = [a,c,y,b,x,z,a]

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
        print(ciclo)
    return ciclo, custo_ciclo           

            
        
print(kopt(matriz_dist))
        
        


        

 
        







































