import random as rd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
from regresion import regresion


def arboles(cantidad=4):
    celda =[]
    for _ in range(cantidad):
        cArbol = rd.randint(1, 1000)
        celda.append(cArbol)
    return celda
 

def poblacion(individuos = 100, tipos=4, delg=16, cArboles=1000, optimo=None)-> list:
    pob = []
    for individuo in range(individuos):
        pob.append([])
        for _ in range(delg):
            celda = arboles() 
            pob[individuo].append(celda)
    if optimo != None:
        pob.append(optimo)
    if len(pob) > 100:
        pob.pop(rd.randint(0,98))
    return pob

def matarIndividuos(poblacion, optimo, delg = 16):
    pobTemp = deepcopy(poblacion)
    while len(pobTemp)> 40:
        pobTemp.pop(rd.randint(0, len(pobTemp)-1))
    for i in range(len(poblacion)-40):
        temp = []
        for delegacion in range(delg):
            celda = arboles()
            temp.append(celda)
        pobTemp.append(temp)
    pobTemp.append(optimo)
    return pobTemp


def cruzaPunto(padre, madre):
    corte = rd.randint(0, len(padre)-1)
    for indice in range(corte, len(padre)):
        aux_1 = padre[indice]
        aux_2 = madre[indice]
        padre[indice] = aux_2
        madre[indice] = aux_1
    return [padre, madre]


def torneoCruza(poblacion, optimo):
    ganador = deepcopy(poblacion)
    while len(ganador)>1:
        indice_local = rd.randint(0, len(ganador)-1)
        indice_visitante = rd.randint(0, len(ganador)-2)
        indice_visitante = indice_visitante if indice_local != indice_visitante else rd.randint(0, len(ganador)-2)
        partido = rd.choice(['local','visitante'])
        if ganador[indice_local] == optimo:
            partido = rd.choice(['local','local','visitante'])
        if ganador[indice_visitante] == optimo:
            partido = rd.choice(['visitante','visitante','local'])
        if partido == 'local':
            ganador.pop(indice_visitante)
        else:
            ganador.pop(indice_local)
    return ganador[0]


def cruza(poblacion, pCruza, opt, tam=100 ,tipos=4, delg=16, cArboles=1000):
    pobTemp = []
    while len(pobTemp)<pCruza:
        padre = torneoCruza(poblacion, opt)
        madre = torneoCruza(poblacion, opt)
        hijos = cruzaPunto(padre, madre)
        for hijo in hijos:
            pobTemp.append(hijo)
    for _ in range(tam - len(pobTemp)):
        individuo = []
        for _ in range(delg):
            celda = arboles()
            individuo.append(celda)
        pobTemp.append(individuo)
    return pobTemp

def mutacion(pobTemp, pMut, cArboles=1000, delg=16):
    poblacion = deepcopy(pobTemp)
    for _ in range(pMut):
        inMutar = rd.randint(0, len(poblacion)-1)
        moneda = rd.choice(['modificar','modificar','modificar','modificar', 'noModificar'])
        if moneda == 'modificar':
            for i in range(3):
                celda = rd.randint(0, delg-1)
                poblacion[inMutar][celda] = arboles()
    return poblacion

def equivalencia(pobTemp, tipos=4, celda = False):
    porAbsorcion = [0.00802, 0.0506, 0.0581, 0.00541]
    pob= deepcopy(pobTemp)
    if celda == False:
        porPob = []
        for individuo in pob:
            porInd = [[] for _ in range(len(individuo))]
            for arbol in range(tipos):
                indice = 0
                for celda in individuo:
                    porInd[indice].append(np.power(celda[arbol],0.333)*porAbsorcion[arbol])
                    indice+=1
            porPob.append(porInd)
        return porPob
    else:
        for arbol in range(len(pob)):
            pob[arbol] = np.power(pob[arbol],0.333)* porAbsorcion[arbol]
        return pob

def penalizacion(poblacion, cArbol=4, limite=10000):
    penalizados = []
    for indice in range(len(poblacion)):
        sumaParcial = [0 for i in range(4)]
        for arbol in range(4):
            for celda in poblacion[indice]:
                sumaParcial[arbol] += celda[arbol]
        for s in sumaParcial:
            if s > limite:
                penalizados.append(indice)

    return penalizados


def vida(celdaTemp):
    celda = deepcopy(celdaTemp)
    for _ in range(2):
        arbolAleatorio = rd.randint(0, len(celda)-1)
        arbolEliminar = rd.randint(0,celda[arbolAleatorio]//3)
        celda[arbolAleatorio] = celda[arbolAleatorio] - arbolEliminar 
    return celda
    
def verificarGeneracion(evaluacion, aptitudOptima):
    contador = 0
    for aptitud in evaluacion:
        if aptitudOptima == aptitud:
            contador += 1
    return contador/len(evaluacion)

def encontrarMax(porcentaje):
    minimo= min(porcentaje)
    indice= porcentaje.index(minimo)
    return indice

# @jit(nopython=True)
def principal(generaciones=100, cantidadInd = 100, probCruza = 0.85, probMutacion = 0.2, cArboles=10000):
    pob = poblacion(cArboles=cArboles)
    param = ['O3','WSP', 'RH']
    porcentajeMax = []
    individuoOptimo = []
    arbolesPlantados = []
    elitismo = []
    pp=[]
    for generacion in range(generaciones):
        pobTemporal = deepcopy(pob)
        verificarPoblacion = penalizacion(pob)
        pp.append(len(verificarPoblacion))
        porcentajePoblacion = equivalencia(pob)
        resultados = []
        for individuo in range(len(pob)):
            reduccion = 0
            for estacion in range(16):
                archivoConcentracion = pd.read_csv('promedios/'+str(estacion)+'.csv')
                for dia in range(365):
                    temporal=[]
                    for parametro in param:
                        temporal.append(archivoConcentracion[parametro][dia])
                    concentracion = regresion(temporal, pob[individuo][estacion])
                    if dia%91 == 0:
                        pob[individuo][estacion] = vida(list(pob[individuo][estacion]))
                    reduccion+=concentracion
            resultados.append(reduccion)
        if len(verificarPoblacion) != 0:
            for penalizar in verificarPoblacion:
                resultados[penalizar] = rd.uniform(0.6, 0.8) * resultados[penalizar]
        indice_maximo = encontrarMax(resultados)
        mGeneracion = resultados[indice_maximo]
        if len(elitismo)==0:
            elitismo.append(resultados[indice_maximo])
            individuoOptimo.append(pob[indice_maximo])
            arbolesPlantados.append(pobTemporal[indice_maximo])
        else:
            if elitismo[-1] > mGeneracion:
                elitismo.append(mGeneracion)
                individuoOptimo.append(pob[indice_maximo])
                arbolesPlantados.append(pobTemporal[indice_maximo])
            else:
                elitismo.append(min(elitismo))
                individuoOptimo.append(individuoOptimo[-1])
                arbolesPlantados.append(arbolesPlantados[-1])
        if len(elitismo) != 0:
            c=-1
            comprobarOptimo = verificarGeneracion(resultados,elitismo[-1])
            if comprobarOptimo > 0.5:
                pob = matarIndividuos(deepcopy(pobTemporal), deepcopy(pobTemporal[indice_maximo]))
                print('entre')
            if len(elitismo)>30:
                for i in elitismo:
                    if elitismo[-1] == i:
                        c += 1
                if c/len(elitismo)>0.4:
                    pob = matarIndividuos(deepcopy(pobTemporal), deepcopy(pobTemporal[indice_maximo]))
                    print('entre al siguiente')
        pob_k = cruza(deepcopy(pob), int(cantidadInd*probCruza),opt=deepcopy(pobTemporal[indice_maximo]), cArboles=cArboles)
        mutar = mutacion(deepcopy(pob_k), int(cantidadInd*probMutacion), cArboles=cArboles)
        pob = mutar
        print(generacion)
    progreso = [i for i in range(generaciones)]
    
    
    valoresOptimos ={'arboles plantados': arbolesPlantados,
                    'arboles sobrevivientes': individuoOptimo, 
                    'resultadoOptimo': elitismo,
                    'cantidadPenalizados': pp, 
                    'progreso':progreso}
    return valoresOptimos

#geneticoooooo = principal()

#data_frame = pd.DataFrame(geneticoooooo)
#data_frame.to_csv('resultado_con_1000_gen.csv', index=False)
#fig, ax = plt.subplots()
#ax.plot(geneticoooooo['progreso'], geneticoooooo['resultadoOptimo'])
#ax.set_title('Search for the minimum amount of concentration PM10')
#ax.set_xlabel('Generations')
#ax.set_ylabel('Total concentration per year (g)')
#plt.show()
