import random
import numpy as np
from os import remove
from os import system
#from Servidor import cantidad
import sys

print("Planificador ejecutandose")
#Globales
procesadores = 4
soluciones = 7 #Debe ser impar
#tweets = cantidad
tweets = 2000
fitness = np.zeros(soluciones, dtype=int)
probCruzamiento = .5
probMutacion = .05

#Eliminar asignaciones anteriores
def eliminar():
    for i in range(procesadores):
        arch = 'procesador' + str(i) + '.txt'
        try:
            remove(arch)
        except FileNotFoundError:
            return False
        except IOError:
            return False
    return

#Fitness
def fit():
    for i in range(soluciones):
        pesoProc = np.zeros(procesadores, dtype=int)
        #print(f"\nSolucion {i+1}")
        for j in range(tweets):
            p = 0
            for k in range(2):
                p += (2 * poblacion[i][(j * 2) + k]) ** k  # obtener procesador al que es asignada la ventana de tareas
            if poblacion[i][j * 2] == 0:
                p -= 1  # obtener procesador al que es asignada la ventana de tareas
            pesoProc[p] += 1
        a = 0
        #print(f"El procesador debe realizar entre {u1} y {u2} tareas")
        for j in pesoProc:
            if j >= u1 and j <= u2:
                a += 1  # Número de procesadores que tienen asignada una cantidad de trabajo aceptable
        fitness[i] = a
        #print(fitness[i])
    return

def elitismo():
    poblacion2[0][:] = poblacion[np.argmax(fitness)][:] #Solo la mejor solución
    return

def mutacion(): #Mutacion de cada gen
    for i in range(soluciones):
        p = random.random()
        if p <= probMutacion:
             if poblacion2[i][j] == 0:
               poblacion2[i][j] = 1
             else:
                poblacion2[i][j] = 0
    return

def cruzamiento():#Cruzamiento en un punto
    if random.random() <= probCruzamiento:
        punto = random.randint(1, (tweets * 2) - 2)
        temo = np.zeros((2, tweets * 2), dtype=int) #Cruzado
        for i in range(tweets * 2):
            if i < punto:
                temo[0][i] = poblacion2[individuos][i]
                temo[1][i] = poblacion2[individuos+1][i]
            else:
                temo[0][i] = poblacion2[individuos+1][i]
                temo[1][i] = poblacion2[individuos][i]
        poblacion2[individuos][:] = temo[0][:]
        poblacion2[individuos+1][:] = temo[1][:]
    return

def seleccion(): #Selección por ruleta
    for j in range(2): #Encontrar 2 padres
        p = random.randint(0, sum(fitness)) #Número aleatorio entre 0 - suma fitness
        acumulado = i = 0
        while acumulado < p:  #
            acumulado += fitness[i]
            i += 1
        poblacion2[individuos + j][:] = poblacion[i - 1][:] #Igualar
    cruzamiento()
    return

#XD
eliminar()
poblacion = poblacion2 = np.zeros((soluciones, tweets * 2), dtype=int)
u1 = round(((tweets / procesadores) * .9))  # umbral ligero
u2 = round(((tweets / procesadores) * 1.1))  # umbral pesado
for i in range(soluciones):
    for j in range(tweets * 2):
        poblacion[i][j] = random.randint(0,1)
fit() #Función fitness
solucion = np.zeros((50, tweets * 2), dtype=int) #50 por las generaciones, OJO si se cambian
solucion[0][:] = poblacion[np.argmax(fitness)][:]
indice = 0 #Índice de la fila que guarda la mejor entre todas las soluciones guardadas en solucion
maxs = max(fitness) #Mayor fitness
generaciones = 1

#Algoritmo genético
while generaciones < 50 and maxs != 8: #50 generaciones u 8 procesadores en un marco de trabajo aceptable
    elitismo()
    individuos = 1
    while individuos < soluciones: #Generar 25 soluciones en cada generación
        seleccion()
        individuos += 2
    mutacion()
    poblacion = poblacion2 #Actualizar población
    fit()
    solucion[generaciones][:] = poblacion[np.argmax(fitness)][:] #Guardar todas las mejores soluciones
    if max(fitness) > maxs: #Si hay una mejor solucion
        maxs = max(fitness)
        indice = generaciones
    generaciones += 1

#Resultados
peso = np.zeros(procesadores, dtype=int)
cont = np.zeros(procesadores, dtype=int)
for j in range(tweets): #Obtener asignaciones de las ventanas de tareas en los procesadores
    p = 0
    for k in range(2):
        p += (2 * solucion[indice][(j * 2) + k]) ** k  # obtener procesador al que es asignada la ventana de tareas
    if solucion[indice][j * 2] == 0:
        p -= 1  # obtener procesador al que es asignada la ventana de tareas
    peso[p] += 1
    nombre2 = 'procesador' + str(p) + '.txt'
    with open(nombre2, 'a') as archivo2: #Escribir en el bloc de notas de cada procesador
        archivo2.write(f"{j}\n") #L de ventana y j el número de línea

#Impresión
for i in range(procesadores):
    (f"Procesador {i+1} = {peso[i]} tareas asignadas")
print("\n")

#os.system("Fase4.py")