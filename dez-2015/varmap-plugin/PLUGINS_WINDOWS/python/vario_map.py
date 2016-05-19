#!/bin/python
import sgems
import matplotlib.pyplot as plt
from matplotlib import colors,ticker,cm
from scipy.interpolate import griddata
from scipy import interpolate
import numpy as np
import math
import random
import os



"""
VARIOMAP
"""

class   vario_map:
    def _init_(self):
        pass 
    def initialize(self,params):
        self.params = params
        return True
    def execute(self):
	print self.params
	# ESTABELECA OS PARAMETROS INICIAIS
	head_property= self.params['head_prop']['property']
	head_grid = self.params['head_prop']['grid']
	tail_property = self.params['tail_prop']['property']
	tail_grid= self.params['tail_prop']['grid']
	C_variogram = int(self.params['C_variogram']['value'])
	C_covariance= int(self.params['C_covariance']['value'])
	nlags= int(self.params['nlags']['value'])
	lagdistance = float(self.params['lagdistance']['value'])
	lineartolerance= float(self.params['lineartolerance']['value'])
	htolerance = float(self.params['htolangular']['value'])
	vtolerance = float(self.params['vtolangular']['value'])
	hband = float(self.params['hband']['value'])
	vband = float(self.params['vband']['value'])
	dip = float(self.params['Dip']['value'])
	azimute = float(self.params['Azimute']['value'])
	gdiscrete = int(self.params['Gdiscrete']['value'])
	ncontour = int(self.params['ncontour']['value'])
	Remove = float(self.params['Remove']['value'])	

	def retire_nan (x,y,z,v):
		xn =[]
		yn =[]
		zn =[]
		vn =[]
		for i in range(0,len(v)):
			if (v[i] > -99999999999999999):
				
				xn.append(x[i])
				yn.append(y[i])
				zn.append(z[i])
				vn.append(v[i])
		return xn, yn, zn, vn
			


	xh = []
	yh = []
	zh = [] 
	vh = []
	
	xh1 = sgems.get_property(head_grid, "_X_")
	yh1 = sgems.get_property(head_grid, "_Y_")
	zh1 = sgems.get_property(head_grid, "_Z_")
	vh1 = sgems.get_property(head_grid, head_property)	

	xh, yh, zh, vh = retire_nan(xh1,yh1,zh1,vh1)


	xt = []
	yt = []
	zt = []	
	vt = []

	xt1 = sgems.get_property(tail_grid, "_X_")
	yt1 = sgems.get_property(tail_grid, "_Y_")
	zt1 = sgems.get_property(tail_grid, "_Z_")
	vt1 = sgems.get_property(tail_grid, tail_property)

	xt, yt, zt, vt = retire_nan(xt1,yt1,zt1,vt1)		

	# VERIFIQUE O NUMERO DE DIMENSOES DO PROBLEMA
	
	# VERIFICACAO DAS DIMENSOES DO HEAD

	cdimensaoxh = False
	cdimensaoyh = False
	cdimensaozh = False

	for x in range(0,len(xh)):
		if (xh[x] != 0):
			cdimensaoxh = True


	for y in range(0,len(yh)):
		if (yh[y] != 0):
			cdimensaoyh = True


	for z in range(0,len(zh)):
		if (zh[z] != 0):
			cdimensaozh = True

	# VERIFICACAO DAS DIMENSOES DO TAIL

	cdimensaoxt = False
	cdimensaoyt = False
	cdimensaozt = False

	for x in range(0,len(xt)):
		if (xt[x] != 0):
			cdimensaoxt = True

	for y in range(0,len(yt)):
		if (yt[y] != 0):
			cdimensaoyt = True


	for z in range(0,len(zt)):
		if (zt[z] != 0):
			cdimensaozt = True

	if ((cdimensaoxt == cdimensaoxh) and (cdimensaoyt == cdimensaoyh) and (cdimensaozt == cdimensaozh)):
		


		# DEFINA A MAXIMA DISTANCIA PERMISSIVEL
		
		dmaximo = (nlags + 0.5)*lagdistance
		
		#CONVERTA TOLERANCIAS SE ELAS FOREM IGUAIS A ZERO 
		if (htolerance == 0):
			htolerance= 45
		if (vtolerance == 0):
			vtolerance = 45
		if (hband == 0):
			hband = lagdistance/2
		if (vband == 0):
			vband = lagdistance/2
		if (lagdistance == 0):		
			lagdistance = 100
		if (lineartolerance == 0):
			lineartolerance = lagdistance/2
		
		
		
	
		#CONVERTA OS VALORES DE TOLERANCIA EM RADIANOS
		htolerance = math.radians(htolerance)
		vtolerance = math.radians(vtolerance)	

		# DETERMINE AS PROJECOES DO DIP E DO AZIMUTE 
		htolerance = math.cos(htolerance)
		vtolerance = math.cos(vtolerance)

		
		xhrot =[]
		yhrot =[]
		zhrot =[]
		xttrot =[]
		yttrot=[]
		zttrot=[]		
		
		for i in range(0, len(xh)):

		    # ROTACIONE PRIMEIRAMENTE NO AZIMUTE

		    xrot = math.cos(math.radians(azimute))*xh[i] - math.sin(math.radians(azimute))*yh[i]
		    yrot = math.sin(math.radians(azimute))*xh[i] + math.cos(math.radians(azimute))*yh[i]
		    yrot2 = math.cos(math.radians(dip))*yrot - math.sin(math.radians(dip))*zh[i]
		    zrot = math.sin(math.radians(dip))*yrot + math.cos(math.radians(dip))*zh[i]

		    xhrot.append(xrot)
		    yhrot.append(yrot2)
		    zhrot.append(zrot)

		    # ROTACIONE EM SEGUIDA NO MERGULHO

		    xtrot = math.cos(math.radians(azimute))*xt[i] - math.sin(math.radians(azimute))*yt[i]
		    ytrot = math.sin(math.radians(azimute))*xt[i] + math.cos(math.radians(azimute))*yt[i]
		    ytrot2 = math.cos(math.radians(dip))*ytrot - math.sin(math.radians(dip))*zt[i]
		    ztrot = math.sin(math.radians(dip))*ytrot + math.cos(math.radians(dip))*zt[i]

		    xttrot.append(xtrot)
		    yttrot.append(ytrot2)
		    zttrot.append(ztrot)


		#CONVERTA OS VALORES DE TOLERANCIA EM RADIANOS
		htolerance = math.radians(htolerance)
		vtolerance = math.radians(vtolerance)

		# DETERMINE AS PROJECOES DO DIP E DO AZIMUTE
		htolerance = math.cos(htolerance)
		vtolerance = math.cos(vtolerance)

		# DEFINA TODAS AS DISTANCIAS EUCLIDIANAS POSSIVEIS

		cabeca = []
		rabo = []
		cabeca2 =[]
		rabo2 =[]
		distanciah =[]
		distanciaxy =[]
		distanciax =[]
		distanciay = []
		distanciaz = []
		for t in range(0, len(yt)):
		    for h in range(t, len(yh)):
					
			
			dx = xhrot[h]-xttrot[t]
			dy= yhrot[h]-yttrot[t]
			dz = zhrot[h]-zttrot[t]
			dh = math.sqrt(math.pow(dy,2) + math.pow(dx,2) + math.pow(dz,2))
			
			if (dh <dmaximo):
				cabeca.append(vh[h])
				cabeca2.append(vt[h])
				rabo2.append(vt[t])
				rabo.append(vh[t])
			
				distanciay.append(dy)
				distanciax.append(dx)
				distanciaz.append(dz)
				distanciah.append(dh)
				distanciaxy.append(math.sqrt(math.pow(dy,2) + math.pow(dx,2)))
		
		# CALCULE TODOS OS VALORES DE COS E SENO ADMISSIVEIS AO AZIMUTE		
		

		cos_Azimute = []
		sin_Azimute = []
		flutuante_d = 0
		
		
		for a in range(0,360,20):
			diferenca = a 
			cos_Azimute.append(math.cos(math.radians(90-diferenca)))
			sin_Azimute.append(math.sin(math.radians(90-diferenca)))
			cos_Dip = math.cos(math.radians(90))
			sin_Dip = math.sin(math.radians(90))
	
		distancias_admissiveis = []
		azimute_admissiveis = []
		dip_admissiveis =[]
		v_valores_admissiveis_h =[]
		v_valores_admissiveis_t =[]
		v_valores_admissiveis_h2 =[]
		v_valores_admissiveis_t2 =[]
		pares = []		

		

		# CALCULE OS PONTOS ADMISSIVEIS 
		for a in xrange(0,18):	
			# reestabelca o valor do norte retirando novamente o azimute
			azm = math.radians(a*20)
			for l in xrange(0, nlags):			
				valores_admissiveis_h = []
				valores_admissiveis_t = []
				valores_admissiveis_h2 =[]
				valores_admissiveis_t2 =[]
				distancia_admissivel = []
				azimute_admissivel =[]
				dip_admissivel=[]
				lag= lagdistance*(l+1)
				par= 0 
				limitemin = lag - lineartolerance
				limitemax = lag + lineartolerance
				for p in xrange(0,len(distanciah)):	
					if (distanciah[p] > limitemin and distanciah[p] < limitemax):						
						if (distanciaxy[p] > 0.000): 				
							check_azimute = (distanciax[p]*cos_Azimute[a] +distanciay[p]*sin_Azimute[a])/distanciaxy[p]
						else:
							check_azimute = 1
						check_azimute = math.fabs(check_azimute)
						if (check_azimute >= htolerance):								
							check_bandh = (cos_Azimute[a]*distanciay[p]) - (sin_Azimute[a]*distanciax[p])
							check_bandh = math.fabs(check_bandh)
							if (check_bandh < hband):								
								if(distanciah[p] > 0.000):
									check_dip = (math.fabs(distanciaxy[p])*sin_Dip + distanciaz[p]*cos_Dip)/distanciah[p]
								else:
									check_dip = 0.000
								check_dip = math.fabs(check_dip) 
								if (check_dip >= vtolerance):
									check_bandv = sin_Dip*distanciaz[p] - cos_Dip*math.fabs(distanciaxy[p])
									check_bandv = math.fabs(check_bandv)
									if (check_bandv < vband):
											valores_admissiveis_h.append(cabeca[p])
											valores_admissiveis_t.append(rabo[p])
											valores_admissiveis_h2.append(cabeca2[p])
											valores_admissiveis_t2.append(rabo2[p])
											distancia_admissivel.append(distanciah[p])
											par = par + 1	
											azimute_admissivel.append(azm)							
				if (len(valores_admissiveis_h) > 0 and len(valores_admissiveis_t) > 0):	
					if (par > 0):		
						v_valores_admissiveis_h.append(valores_admissiveis_h)
						v_valores_admissiveis_h2.append(valores_admissiveis_h2)
						v_valores_admissiveis_t2.append(valores_admissiveis_t2)
						v_valores_admissiveis_t.append(valores_admissiveis_t)
						distancias_admissiveis.append(distancia_admissivel)
						pares.append(par)
						azimute_admissiveis.append(azimute_admissivel)	
		

		# CALCULE AS FUNCOES DE CONTINUIDADE ESPACIAL SEGUNDO OS VALORES ADMISSIVEIS	

		# CALCULE O VARIOGRAMA 
		
		if (C_variogram == 1): 		
			continuidade =[]
			lag_adm =[]
			azimute_adm =[]
			for i in xrange(0,len(v_valores_admissiveis_h)):
				flutuantet =[]
				flutuanteh =[]
				flutuanteh2 = []
				flutuantet2 =[]
				flutuanted =[]
				flutuantea=[]
				flutuantedip=[]
				par_var = 0
				flutuanteh = v_valores_admissiveis_h[i][:]
				flutuanteh2= v_valores_admissiveis_h2[i][:]
				flutuantet = v_valores_admissiveis_t[i][:]
				flutuantet2 = v_valores_admissiveis_t2[i][:]
				flutuanted = distancias_admissiveis[i][:]
				flutuantea= azimute_admissiveis[i][:]
				par_var= pares[i]
				soma = 0
				lagmedio =0
				agmedio =0 
				dgmedio = 0
				for j in xrange(0, len(flutuanteh)):
					soma = soma + (flutuanteh[j] - flutuantet[j])*(flutuanteh2[j]-flutuantet2[j])/(2*pares[i])
				for z in xrange(0, len(flutuanted)):
					lagmedio = lagmedio + flutuanted[z]/len(flutuanted)
				for g in xrange(0, len(flutuantea)):
					agmedio = agmedio + flutuantea[g]/len(flutuantea)
				if (soma <= Remove):
					continuidade.append(soma)
					azimute_adm.append(agmedio)
					lag_adm.append(lagmedio)

		# CALCULE O COVARIOGRAMA 
		if (C_covariance == 1): 		
			continuidade =[]
			lag_adm =[]
			azimute_adm =[]
			for i in xrange(0,len(v_valores_admissiveis_h)):
				flutuantet =[]
				flutuanteh =[]
				flutuanted =[]
				flutuantea=[]
				par_var = 0
				flutuanteh = v_valores_admissiveis_h[i]
				flutuantet = v_valores_admissiveis_t[i]
				flutuanted = distancias_admissiveis[i]
				flutuantea= azimute_admissiveis[i]
				par_var= pares[i]
				soma = 0
				lagmedio =0
				agmedio =0 
				dgmedio = 0
				somah = 0
				somat = 0 
				mediah = 0
				mediat =0
				for d in range (0, len(flutuanteh)):
					somah = somah + flutuanteh[d]
				mediah = float(somah/len(flutuanteh))
				for t in range (0, len(flutuantet)):
					somat = somat + flutuantet[t]
				mediat = float(somat/len(flutuantet))
				for j in xrange(0, len(flutuanteh)):		
						soma = soma + float(((flutuanteh[j] - mediah)*(flutuantet[j] - mediat))/(par_var))
				for z in xrange(0, len(flutuanted)):
					lagmedio = lagmedio + flutuanted[z]/len(flutuanted)
				for g in xrange(0, len(flutuantea)):
					agmedio = agmedio + flutuantea[g]/len(flutuantea)
				if (soma <= Remove):				
					continuidade.append(soma)
					azimute_adm.append(agmedio)
					lag_adm.append(lagmedio)
		print ("OK")
	
		# RECORD FILE 

		
		arquivo2 = open("saida_varmap.txt","w")
		arquivo2.write(str(gdiscrete)+"\n")
		arquivo2.write(str(ncontour)+"\n")
		for i in range(0, len(azimute_adm)):
			arquivo2.write(str(azimute_adm[i])+"	"+str(lag_adm[i])+ "	"+str(continuidade[i]) + "\n")
		arquivo2.close()


		# PLOTE O MAPA DE VARIOGRAMAS INTERPOLADO
		
		os.system("python plot_varmap.py")
	
    def finalize(self):
        print "Finalize program"
        return True
    def name(self):
        return "vario_map"
##############################################
def get_plugins():
    return["vario_map"]


