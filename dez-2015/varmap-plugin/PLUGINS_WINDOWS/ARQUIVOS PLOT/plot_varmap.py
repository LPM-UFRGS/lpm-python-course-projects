import matplotlib.pyplot as plt
from matplotlib import colors,ticker,cm
from scipy.interpolate import griddata
from scipy import interpolate
import numpy as np
import math
import random
import os

arquivo2 = open("saida_varmap.txt","r")
gdiscrete = int(arquivo2.readline())
ncontour = int(arquivo2.readline())
arquivo2.close()
azimute_adm, lag_adm, continuidade = np.loadtxt("saida_varmap.txt",dtype= float,delimiter="	", skiprows = 2, usecols=(0,1,2), unpack=True)

gdiscrete = 40
ncontour = 40

x = np.array(lag_adm)*np.sin(np.array(azimute_adm))
y = np.array(lag_adm)*np.cos(np.array(azimute_adm))

maximo = 0
if (max(x) > max(y)):
	maximo = max(x)
else:
	maximo = max(y)


Xi = np.linspace(-maximo,maximo,gdiscrete)
Yi = np.linspace(-maximo,maximo,gdiscrete)




#make the axes
f = plt.figure()
left, bottom, width, height= [0,0.1, 0.7, 0.7]
ax  = plt.axes([left, bottom, width, height])
pax = plt.axes([left, bottom, width, height],
		projection='polar',
		axisbg='none')

pax.set_theta_zero_location("N")
pax.set_theta_direction(-1)


ax.set_aspect(1)
ax.axis('Off')


# grid the data.
Vi = griddata((x, y), np.array(continuidade), (Xi[None,:], Yi[:,None]), method='linear')	
cf = ax.contourf(Xi,Yi,Vi, ncontour, cmap=plt.cm.jet)


gradient = np.linspace(1,0, 256)
gradient = np.vstack((gradient, gradient))


cax = plt.axes([0.7, 0.05, 0.05, 0.8])
cax.xaxis.set_major_locator(plt.NullLocator())
cax.yaxis.tick_right()
cax.imshow(gradient.T, aspect='auto', cmap=plt.cm.jet)
cax.set_yticks(np.linspace(0,256,len(cf.get_array())))
cax.set_yticklabels(map(str, cf.get_array())[::-1])

plt.show()
plt.close()
