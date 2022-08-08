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

#DISTRIBUCIÓN PERT
def pert(a, b, c, *, lamb=4):
    r = c - a
    alpha = 1 + lamb * (b - a) / r
    beta = 1 + lamb * (c - b) / r
    return a + betavariate(alpha, beta) * r


#VARIABLES
valores=1000 #probabilidades de bernoulli y poisson
iteracion=10 #probabilidad triangular

#LEER LOS DATOS DE LA SEGUNDA HOJA
df = pd.read_excel('uploads/Riesgo.xlsx')

tipo = df['Tipo']
probabilidad = df['Probabilidad']
n_minimo = df['Minimo']
n_maximo = df['Maximo']
n_mas_probable = df['Mas probable']
riesgo = df['Riesgo']

#DISTRIBUCION DE BERNOULLI Y POISSON
ocurre={}
for i in range(len(probabilidad)):
  if tipo[i]=='single':
    p = probabilidad[i]/100 # parametro de forma 
    bernoulli = stats.bernoulli(p)

    aleatorios = bernoulli.rvs(valores)  # genera aleatorios
    ocurre['prob',i]=aleatorios

  else:
    mu = probabilidad[i] # parametro de forma 
    poisson = stats.poisson(mu) 

    aleatorios = poisson.rvs(valores)
    ocurre['prob',i]=aleatorios

#DISTRIBUCIÓN PERT
matriz={}
for v in range(len(ocurre)):
  total2={}
  for j in range(len(ocurre['prob',0])):
    if ocurre['prob',v][j] == 0:
      total2['dic',j]=[0]*iteracion
    else:
      valor = [pert(n_minimo[v], n_mas_probable[v], n_maximo[v]) for k in range(iteracion)]
      if ocurre['prob',v][j] == 1:
        total2['dic',j]=valor
      else:
        mult_v=[]
        for i in valor:
          mult_v.append(i*ocurre['prob',v][j])
        total2['dic',j]=mult_v

  dic_total2=[]
  for i in range(len(total2)):
    dic_total2=dic_total2+total2['dic',i]
  
  matriz['todo',v]=dic_total2

#SUMA DE TODAS LAS DISTRIBUCIONES 
ntotal=[]
for i in range(len(matriz['todo',0])):
	suma=0
	for j in range(len(matriz)):
		suma+=matriz['todo',j][i]
	ntotal.append(suma)

#DATOS
nmin_total=min(ntotal)
#print('El minimo es:  ', round(nmin_total, 2))
nmedia_total=statistics.mean(ntotal) 
#print('La media es:   ', round(nmedia_total, 2))
nmax_total=max(ntotal)
#print('El maximo es:  ', round(nmax_total, 2))

#SUPERPOSICION DE GRAFICAS
fig = plt.figure(figsize =(10, 6))

ax1 = fig.add_subplot()
ax1.hist(ntotal, bins=40, color="r", alpha=0.75, edgecolor = 'black')
ax1.plot(ntotal, np.full_like(ntotal, -0.01))
plt.xlabel("Precio", fontsize=15)
plt.ylabel("Cantidad", fontsize=15)
plt.title("Costo Total", fontsize=25)
plt.axvline(18500, color='m', linewidth=1)
 
ax2 = ax1.twinx()  
ecdf = ECDF(ntotal)
ax2.plot(ecdf.x, ecdf.y, color="b")
plt.ylabel("Probabilidad", fontsize=15)
ax2.set_yticks([0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
plt.grid(color='k', linestyle='dotted', linewidth=1)
plt.savefig("uploads/Histograma2.png")

#VARIANZA TOTAL
varianza_ntotal=var(ntotal)

#VARIANZA DE CADA ELEMENTO
nvarianza=[]
for i in range(len(n_minimo)):
  nvarianza.append(var(matriz['todo',i]))

porcentaje=[]
for i in range(len(nvarianza)):
  porcentaje.append(nvarianza[i]*100/varianza_ntotal)

#ORGANIZAMOS EL VECTOR (MENOR A MAYOR)
dic = dict(zip(riesgo, porcentaje))
dic_ordenado = sorted(dic.items(), key=operator.itemgetter(1))
nuevo_d=dict(dic_ordenado)

riesgo=[]
for key in nuevo_d:
    riesgo.append(key)

#VARIANZA FINAL
nvarianza=list(nuevo_d.values())

#GRAFICA DE TORNADO
plt.subplots(figsize =(8, 5))
ax=plt.barh(riesgo, nvarianza, facecolor='r', edgecolor = 'black')

for i in range(len(nvarianza)):
  plt.text(nvarianza[i]+0.5, i, f'{round(nvarianza[i],2)} %')

plt.xlabel('% Contribución a la varianza', fontsize=15)
plt.xlim(0, nvarianza[9]+10)
plt.title('Costo Total', fontsize=25)
plt.savefig("uploads/Tornado2.png", bbox_inches='tight')

sys.stdout.flush()