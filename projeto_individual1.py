"""O primeiro passo é criar o grafo com base nos dados do arquivo"""
import random
import math

class Vertice:
    def __init__(self, nome):
        self.nome = nome
        self.vizinhos = []

lista_de_vertices = []    #lista de vértices do grafo
arquivo = open('soc-dolphins.txt', 'r')

for i in range(195):
    achou1 = False   
    achou2 = False
    conteudo = arquivo.readline()
    
    if i > 35:
        #organiza os valores lidos em uma lista
        valores = conteudo.split(" ")
        valores[1] = valores[1].strip('\n')
        
        #checa se o vertice já está na lista de vértices
        for j in lista_de_vertices:
            if j.nome == valores[0]:
                j.vizinhos.append(valores[1])
                achou1 = True   #achou o primeiro valor na lista de vértices
            
            if j.nome == valores[1]:
                j.vizinhos.append(valores[0])
                achou2 = True   #achou o segundo valor na lista de vértices  
        
            
                
        #se o vertice não estava na lista, será instanciado
        if achou1 == False:
            v = Vertice(valores[0])
            v.vizinhos.append(valores[1])
            lista_de_vertices.append(v)
        if achou2 == False:
            v = Vertice(valores[1])
            v.vizinhos.append(valores[0])
            lista_de_vertices.append(v)
            


'''vou transformar a lista de vértices em um dicionário pra representar o grafo como uma lista de adjacências'''
grafo = {}
for i in lista_de_vertices:
    grafo[i.nome] = i.vizinhos

'''Fonte pública --> funções de Bron Kerbosch: https://stackoverflow.com/questions/13904636/implementing-bron-kerbosch-algorithm-in-python'''


'''função Bron Kerbosch sem pivoteamento'''
def BronKerbosch_sem_pivoteamento(P, R=None, X=None):
    P = set(P)
    R = set() if R is None else R
    X = set() if X is None else X
    if not P and not X:
        yield R
    while P:
        v = P.pop()
        yield from BronKerbosch_sem_pivoteamento(
            P.intersection(grafo[v]), R.union([v]), X.intersection(grafo[v]))
        X.add(v)

P = grafo.keys()
'''Gera uma lista contendo todos os cliques maximais, usando a função Bronkerbosch sem
   pivoteamento'''
lista1 = list(BronKerbosch_sem_pivoteamento(P))



'''função Bron Kerbosch com pivoteamento'''
def BronKerbosch_com_pivoteamento(P, R=None, X=None):
    P = set(P)
    R = set() if R is None else R
    X = set() if X is None else X
    if not P and not X:
        yield R
    try:
        u = random.choice(list(P.union(X)))  #o pivô é escolhido aleatóriamente
        S = P.difference(grafo[u])
    # Se a união de p e x está vazia
    except IndexError:
        S = P
    for v in S:
        yield from BronKerbosch_com_pivoteamento(P.intersection(grafo[v]), R.union([v]), X.intersection(grafo[v]))
        P.remove(v)
        X.add(v)
'''Gera uma lista contendo todos os cliques maximais, usando a função Bronkerbosch com
   pivoteamento'''  
lista2 = list(BronKerbosch_com_pivoteamento(P))



'''Agora a função para calcular o coeficiente de aglomeração médio do grafo. Fonte pública --> fórmula do coeficiente de aglomeração: https://edisciplinas.usp.br/pluginfile.php/5685381/mod_resource/content/2/ERS_aula5_handout%20%281%29.pdf'''
def coeficiente_de_aglomeracao_medio(grafo):
    lista_de_coeficientes = []
    for v in grafo:
        d = len(grafo[v]) #d é o número de vizinhos do vértice v


        numero_de_triangulos_com_v = 0 #o numero de triângulos que realmente contém v  
        for i in lista1:                          
            if len(i) == 3 and v in i:
                numero_de_triangulos_com_v += 1
        if d <2:
            c = 0
        else:
            c = numero_de_triangulos_com_v / (math.factorial(d) / (math.factorial(2)*math.factorial(d - 2)))  #é a fração que tem como denominador o número de triângulos possíveis contendo v e como numerador o número de triângulos que realmente existem contendo v.
        lista_de_coeficientes.append(c)  #c é o coeficiente de aglomeração de determinado vértice

    coeficiente_de_aglomeracao_medio = sum(lista_de_coeficientes) / len(grafo)
    return coeficiente_de_aglomeracao_medio
'''armazena o resultado da função que calcula o coeficiente de aglomeração médio em uma variável'''
coeficiente_de_aglomeracao_medio = coeficiente_de_aglomeracao_medio(grafo)


print("Coeficiente médio de aglomeração do grafo:")
print(coeficiente_de_aglomeracao_medio)
print()
print("Bron Kerbosch sem pivoteamento e tamanho do clique:")
print()
for i in lista1:
    print(i, end = ' ')
    print(" -->  " + str(len(i)))
print()
print()
print("Bron Kerbosch com pivoteamento e tamanho do clique:")
print()
for i in lista2:
    print(i, end = ' ')
    print(" -->  " + str(len(i)))
    
    
    


        
  





            
                
                
                
                
    
    
