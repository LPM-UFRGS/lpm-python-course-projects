import matplotlib.pyplot as plt
from matplotlib import colors,ticker,cm
from scipy.interpolate import griddata
from scipy import interpolate
import numpy as np
import math
import random
import os

arquivo2 = open("/home/usuario/ar2gems/bin/plugins/Geostat/python/plot/saida_automatic_fitting.txt","r")
direcao = int(arquivo2.readline())
nvariables = int(arquivo2.readline())
nlags = int(arquivo2.readline())
indice_head =[]
indice_tail =[]


for n in range(0,nvariables):
	linha = arquivo2.readline()
	linha_split =[]
	linha_split = linha.split()
	indice_head.append(int(linha_split[0]))
	indice_tail.append(int(linha_split[1]))

for n in range(0, nvariables):
	lag =[]
	variograma =[]
	limite =[]
	funcao =[]
	for i in range(0, nlags):
		linha = arquivo2.readline()
		linha_split =[]
		linha_split = linha.split()
		lag.append(float(linha_split[0]))
		variograma.append(float(linha_split[1]))
		limite.append(float(linha_split[2]))
		funcao.append(float(linha_split[3]))

	plt.subplot(math.sqrt(nvariables),math.sqrt(nvariables),n+1)			
	plt.plot(lag,variograma,'g^--',limite, funcao)

	if (direcao == 1):
		plt.title( "\n \n Principal"+str(indice_head[n]) +" " +str(indice_tail[n]))	
	if (direcao == 2):
		plt.title( "\n \n Secondary"+str(indice_head[n]) +" " +str(indice_tail[n]))
	if (direcao == 3):
		plt.title( "\n \n Vertical" +str(indice_head[n]) +" " +str(indice_tail[n]))

plt.show()

