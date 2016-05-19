import matplotlib.pyplot as plt
from scipy import stats
from matplotlib import colors,ticker,cm
from scipy.interpolate import griddata
from scipy import interpolate
import numpy as np
import math
import random
import os

saida2= open("/home/usuario/ar2gems/bin/plugins/Geostat/python/plot/saida_hscatter.txt","r")
i = int(saida2.readline())
lagdistance = float(saida2.readline())
saida2.close()
vh, vt = np.loadtxt("/home/usuario/ar2gems/bin/plugins/Geostat/python/plot/saida_hscatter.txt",dtype= float,delimiter="	", usecols=(0,1), skiprows = 2, unpack=True)

slope, intercept, r_value, p_value, std_err = stats.linregress(vh,vt)
plt.title("Hscatter plot for lag: " + str(lagdistance*(i+1)) + " correlation: " + str(r_value))			
plt.plot(vh,vt,'ro',vh,slope*vh+intercept,'b-')
plt.xlabel("variable in head")
plt.ylabel("variable in tail")
plt.show()
