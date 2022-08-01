#LIBRERIAS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import statistics
import operator
import sys
from scipy import stats 
from statistics import mode
from matplotlib import style
from numpy import var
from random import betavariate
from statsmodels.distributions.empirical_distribution import ECDF
from PIL import Image

#VARIABLE
iteraciones = 10000

#LEER LOS DATOS DE LA PRIMERA HOJA
file = "uploads/Incertidumbre.xlsx"
df = pd.read_excel(file)

minimo = df['Minimo']
maximo = df['Maximo']
mas_probable = df['Mas probable']
elementos = df['Elementos']

#DISTRIBUCIÓN PERT
def pert(a, b, c, *, lamb=4):
    r = c - a
    alpha = 1 + lamb * (b - a) / r
    beta = 1 + lamb * (c - b) / r
    return a + betavariate(alpha, beta) * r

dicc={}
for i in range(len(minimo)):
	arr = [pert(minimo[i], mas_probable[i], maximo[i]) for _ in range(iteraciones)]
	dicc['trg',i]=arr

#SUMA DE TODAS LAS DISTRIBUCIONES 
total=[]
for i in range(len(dicc['trg',0])):
	suma=0
	for j in range(len(minimo)):
		suma+=dicc['trg',j][i]
	total.append(suma)

#DATOS 
min_total=min(total)
#print('El minimo es:  ', round(min_total, 2))
media_total=statistics.mean(total) 
#print('La media es:   ', round(media_total, 2))
max_total=max(total)
#print('El maximo es:  ', round(max_total, 2))

#SUPERPOSICION DE GRAFICAS
fig = plt.figure(figsize =(10, 6))

ax1 = fig.add_subplot()
ax1.hist(total, bins=40, color="r", alpha=0.75, edgecolor = 'black')
ax1.plot(total, np.full_like(total, -0.01))
plt.xlabel("Precio", fontsize=15)
plt.ylabel("Cantidad", fontsize=15)
plt.title("Costo Total", fontsize=25)
valor_base=sum(mas_probable)
plt.axvline(valor_base, color='m')
 
ax2 = ax1.twinx()  
ecdf = ECDF(total)
ax2.plot(ecdf.x, ecdf.y, color="b")
plt.grid(color='k', linestyle='dotted', linewidth=1)
ax2.set_yticks([0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
plt.ylabel("Probabilidad", fontsize=15)
plt.savefig("uploads/Histograma.png")

#VARIANZA TOTAL
varianza_total=var(total)

#VARIANZA DE CADA ELEMENTO
varianza=[]
for i in range(len(minimo)):
  varianza.append(var(dicc['trg',i]))

porcentaje=[]
for i in range(len(varianza)):
  porcentaje.append(varianza[i]*100/varianza_total)

#ORGANIZAMOS EL VECTOR (MENOR A MAYOR)
dic = dict(zip(elementos, porcentaje))
dic_ordenado = sorted(dic.items(), key=operator.itemgetter(1))
nuevo_d=dict(dic_ordenado)

elementos=[]
for key in nuevo_d:
    elementos.append(key)

#VARIANZA FINAL
varianza=list(nuevo_d.values())

#GRAFICA DE TORNADO
plt.subplots(figsize =(10, 6))
ax=plt.barh(elementos, varianza, facecolor='r', edgecolor = 'black')

for i in range(len(varianza)):
  plt.text(varianza[i]+0.5, i, f'{round(varianza[i],2)} %')

plt.xlabel('% Contribución a la varianza', fontsize=15)
plt.xlim(0,varianza[7]+5)
plt.title('Costo Total', fontsize=25)
plt.savefig("uploads/Tornado.png")

sys.stdout.flush()