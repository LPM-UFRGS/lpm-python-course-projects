#!/bin/python
import sgems
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import os 



"""
VARIOGRAM OPTIMIZATION
"""

class   automatic_fitting2:
    def _init_(self):
        caminho = "DADOS"
        numero_variogramas = 1
        numero_estruturas = 1
        azimute_direcao_principal = 0
        dip_direcao_principal = 0
        numero_interacoes = 0
        pass 
    def initialize(self,params):
        self.params = params
        return True
    def execute(self):

	# DEFINA AS VARIAVEIS DA ROTINA
        caminho = str(self.params['endereco_arquivo']['value'])
        numero_variogramas = int(self.params['N_variogramas']['value'])
        numero_estruturas = int(self.params['N_estruturas']['value'])
        numero_interacoes =int(self.params['N_interacoes']['value'])
	
	set_maximumrange = int(self.params['set_maximumrange']['value'])
	set_minrange = int(self.params['set_minrange']['value'])
	set_verticalrange = int(self.params['set_verticalrange']['value'])
	
        if (set_maximumrange ==1):
		azimute_direcao_principal =float(self.params['Azimute_dp']['value'])
        	dip_direcao_principal = float(self.params['Dip_dp']['value'])

	if (set_minrange == 1):
		azimute_direcao_secundaria = float(self.params['Azimute_dm']['value'])
		dip_direcao_secundaria = float(self.params['Dip_dm']['value'])
	
	if (set_verticalrange == 1):
		azimute_direcao_vertical = float(self.params['Azimute_dv']['value'])
		dip_direcao_vertical = float(self.params['Dip_dv']['value'])

	restriction = int(self.params['restriction']['value'])
	nlags = int(self.params['nlags']['value'])
	nvariables = int(self.params['nvariables']['value'])
	min_npairs = int(self.params['min_npairs']['value'])
	
	if (restriction == 1):	
		min_contribution = float(self.params['min_contribution']['value'])
		max_contribution = float(self.params['max_contribution']['value'])
		min_nugget = float(self.params['min_nugget']['value'])
		max_nugget = float(self.params['max_nugget']['value'])
		if (set_maximumrange == 1):
			min_range_max = float(self.params['min_range_max']['value'])
			max_range_max = float(self.params['max_range_max']['value'])
		if (set_minrange ==1):
			min_range_min = float(self.params['min_range_min']['value'])
			max_range_min = float(self.params['max_range_min']['value'])
		if (set_verticalrange == 1):
			min_range_vert = float(self.params['min_range_vert']['value'])
			max_range_vert = float(self.params['max_range_vert']['value'])
		
	else:
		min_contribution = 0
		max_contribution = 0
		min_nugget = 0
		max_nugget =0
		min_range_max = 0
		max_range_max = 0
		min_range_min = 0
		max_range_min = 0
		min_range_vert = 0
		max_range_vert = 0

        # ROTINA PARA LEITURA DE DADOS DO ARCHIVO XML DO GSLIB
       
        # INICIO DA LEITURA
        try:
		arquivo = open (caminho, "r")
        except:
                print("Could not open the file! Please try again!")
        
	size_of_matriz = math.sqrt(nvariables)


	
	azimuteVV =[]
	dipVV =[]
	variogramasV =[]
	dipsV =[]
	lagsV =[]
	paresV=[]
	indice_head =[]
	indice_tail =[]
	tipo = []
	
	for p in range(0,nvariables):	
			
		# LEIA OS CABECALHOS DESNECESSARIOS
		# LEIA PRIMEIRA VARIAVEL 
		linha = arquivo.readline() 
		indice_head.append(int(linha))       
		# LEIA SEGUNDA VARIAVEL
	        linha = arquivo.readline()
		indice_tail.append(int(linha))
		
		
		# LEIA O CABECALHO
		linha = arquivo.readline()
	        # DEFINA O VETOR DO AZIMUTE E DO DIP E OS PARAMETROS DOS VARIOGRAMAS VARIOGRAMAS
	        azimuteV = []
	        dipV = []
	        variogramas =[]
	        dips = []
	        lags = []
	        pares =[]
	        # PARA UM NUMERO DE VARIOGRAMAS NO ARCHIVO FACA
	        for i in range(0,numero_variogramas):
		    variograma =[]
	            lag = []
	            par =[]
		    for j in range(0, nlags):
	            	linha = arquivo.readline()
	            	linhasplit = linha.split()
			if(int(linhasplit[4]) >= min_npairs):
		    		if (j ==0):
					azimuteV.append(float(linhasplit[0]))
					dipV.append(float(linhasplit[1]))
		    		lag.append(float(linhasplit[2]))
		    		variograma.append(float(linhasplit[3]))
		    		par.append(int(linhasplit[4]))
		    variogramas.append(variograma)
		    lags.append(lag)
		    pares.append(par)
		azimuteVV.append(azimuteV)
		dipVV.append(dipV)
		variogramasV.append(variogramas)
		lagsV.append(lags)
		paresV.append(pares)

        arquivo.close()

        # DETERMINE O INDICE DA DIRECAO PRINCIPAL SEGUNDO OS VETORES INFORMADOS
        I_dir_principal = -0.5
	I_dir_secundario = -0.5
	I_dir_vertical = --0.5

	informado_principal = False
	informado_secundario = False
	informado_vertical = False

        indice = 0
	interacoes = len(azimuteV)
        for i in range(0,interacoes):
	    if (set_maximumrange ==1):
		    if (azimuteV[i] == azimute_direcao_principal and dipV[i] == dip_direcao_principal):
		    	I_dir_principal = indice
			informado_principal = True
	    if (set_minrange == 1):
		    if (azimuteV[i] == azimute_direcao_secundaria and dipV[i] == dip_direcao_secundaria):
		    	I_dir_secundario = indice
			informado_secundario = True
	    if (set_verticalrange == 1):  
		    if (azimuteV[i] == azimute_direcao_vertical and dipV[i] == dip_direcao_vertical):
		    	I_dir_vertical = indice
			informado_vertical = True
	    indice = indice + 1
	
	
	    
        #...............................................................................
        # Funcoes para o calculo dos pesos das distancias
        def pesos_distancia(distancia):
            #DEFINA A SOMA ACUMULADA DO INVERSO DA DISTANCIA
            soma = 0
            pesos =[]
            for i in distancia:
                inverso = 1/i
                soma = soma + inverso
            for i in distancia:
                pesos.append((1/i)/soma)
            return pesos
        
	


        #...............................................................................
        # Funcoes para o calculo dos pesos dos pares
        def pesos_pares(par):
            #DEFINA A SOMA ACUMULADA DOS PARES)
	    soma =0
            pesos = []
            for i in range(0,len(par)):
                soma = soma + par[i]
            for j in range(0, len(par)):
                pesos.append(float(par[j])/soma)
            return pesos


        # ..............................................................................

        # FUNCAO PARA O CALCULO DOS VALORES VARIOGRAMAS PARA CADA TIPO
        def modelo_variogama(range_estruturas, sill_estruturas, modelos_estruturas, lags, tamanho_lags, tamanho_estruturas):
            valor_variograma_estrutura = []
            n_estruturas = len(modelos_estruturas)
            n_lags = len(lags)
            for i in range(0, n_estruturas):
                valor_variograma = []
                for j in range(0, n_lags):
                    if modelos_estruturas[i] == 0:
                        if lags[j] < range_estruturas[i]:
                            valor_variograma.append(sill_estruturas[i]*(1.5*lags[j]-0.5*pow((lags[j]/range_estruturas[i]),3)))
                        else:
                            valor_variograma.append(sill_estruturas[i])
                    elif modelos_estruturas[i] == 1:
                        valor_variograma.append(sill_estruturas[i]*(1-math.exp(-3*lags[j]/range_estruturas[i])))
                    elif modelos_estruturas[i] == 2:
                        valor_variograma.append(sill_estruturas[i]*(1-math.exp(-3*pow((lags[j]/range_estruturas[i]),2))))
                valor_variograma_estrutura.append(valor_variograma)
            return valor_variograma_estrutura

        #...............................................................................
        # FUNCAO PARA O DESVIO MEDIO QUADRADICO
        def desvio_quad(variograma, modelo_variograma, tamanho_variograma, tamanho_estruturas, efeito_pepita, pesos_distancia, pesos_pares):
            soma_desvio = 0
            for i in range(0, tamanho_estruturas):
                diferenca = 0
                m = list(modelo_variograma[i])
                for j in range(0, tamanho_variograma):
                    diferenca = pesos_distancia[j]*pesos_pares[j]*math.pow((m[j]-variograma[j]-efeito_pepita),2)/tamanho_variograma + diferenca
                soma_desvio = soma_desvio + diferenca
                soma_desvio = math.fabs(soma_desvio)
            return soma_desvio
        #....................................................................................
 			
	def otimizacao(I_dir_principal, variogramasV, lagsV, paresV, nvariables, tipo, numero_estruturas,restriction,min_contribution,max_contribution,min_nugget,max_nugget,min_range,max_range, modeling, direcao, pepm, sillm): 
		count = 0
		check_LMC = False
		check_LMC2 = False
		while (check_LMC == False and check_LMC2 == False):
			check_LMC = False
			check_LMC2 = False
			residuoV =[]
			rangeV =[]
			sillV =[]
			testerV =[]
			pepV = [] 

			for n in range(0,nvariables):

				variogramas = variogramasV[n]
				pares = paresV[n]
				lags = lagsV[n]
		
				# DEFINA O PESO PARA OS PARES DE AMOSTRAS		
	
				p_pares = []
				p_pares = pesos_pares(pares[I_dir_principal][:])
		

				# DEFINA O PESO PARA AS DISTANCIAS
				p_distancia =[]
				p_distancia = pesos_distancia(lags[I_dir_principal][:])
			
				# DETERMINACAO DOS PARAMETROS INICIAIS
				# 1) SILL DE CADA ESTRUTURA
				# 2) EFEITO PEPI
				# 3) RANGE DE CADA ESTRUTURA
				#..................................
				#1) SILL DE CADA ESTRUTURA
				sill_estruturas = []       
				sill_medio = 0
				soma = 0
				n = 0
				resultado_pepita = 0 

				# FACA PARA A DIRECAO PRINCIPAL        
				for i in variogramas[I_dir_principal]:
				    soma = soma + i
				    n = n + 1
				sill_medio = float(soma/(n*numero_estruturas))
				if (count > 1):
					sill_medio = float(soma/(n*numero_estruturas))
				
				# SE AS RESTRICOES ESTIVEREM SELECIONADAS FACA O SILL MEDIO COMO UMA DIFERENCA DA MAX E MIN CONTR
				if (restriction == 1):
					sill_medio = (max_contribution - min_contribution)/numero_estruturas				
				for i in range(0,numero_estruturas):
				    sill_estruturas.append(sill_medio )
				#2) EFEITO PEPITA
				resultado_pepita = 0.1*sill_medio

				# SE AS RESTRICOES ESTIVEREM SELECIONADAS FACA O EFEITO PEPITA IGUAL AO MIN NUGGET
				if(restriction == 1):
					resultado_pepita = min_nugget
				#3) RANGE DE CADA ESTRUTURA
				range_estruturas = []
				max_range_2 = float(max(lags[I_dir_principal])/2)
				
				for i in range(0, numero_estruturas):
				    range_estruturas.append(float(max_range_2/numero_estruturas)*(i+1))
				
				# SE AS RESTRICOES ESTIVEREM SELECIONADAS FACA O RANGE INICIAL DENTRO DOS LIMITES
				if (restriction ==1):
					max_range_2 = (max_range - min_range)/numero_estruturas
					range_estruturas = []
					for i in range(0, numero_estruturas):
						range_estruturas.append(float(max_range_2*(i+1) + min_range))				


				#4) TIPO DE CADA ESTRUTURA
				tipo_estrutura = []
				for i in range(0,numero_estruturas):
				    tipo_estrutura.append(0)
				n = 0
	
				#....................................................................
				# INICIE O PROCEDIMENTO DE OTIMIZACAO
				# DEFINA OS VALORES DE VARIOGRAMA PARA AS DIRECOES NECESSARIAS

				variograma = []	       
				variograma = variogramas[I_dir_principal]
				# DEFINA OS VALORES DE LAG PARA A DIRECAO DE MAXIMA CONTINUIDADE
	
				lag = []     
				lag = lags[I_dir_principal]
	
				# DEFINA O NUMERO DE PONTOS DO VARIOGRAMA

				numero_variogramas = len(variograma)

				# DEFINA O MAXIMO PATAMAR

				max_patamar = max(variograma)

				# DEFINA O MINIMO PATAMAR

				min_patamar = min(variograma)

				# DEFINA O MAXIMO LAG

				max_lag = max(lag)

				#  DEFINA O MINIMO LAG

				min_lag = min(lag)

				# DEFINA O NUMERO DE LAGS DO VARIOGRAMA
		
				numero_lags = len(lag)

	
				# DEFINA NUMERO DE PARAMETROS
				# N SILL DAS ESTRUTURAS, N RANGES DAS ESTRUTURAS, MODELO DAS ESTRUTURAS, EFEITO PEPITA
				numero_de_parametros = numero_estruturas*4
				# CALCULE O PRIMEIRO VALOR DE RESIDUO BASEADO NOS IMPUTS PRIMARIOS
				# DEFINA O MODELO DAS ESTRUTURAS
	
				modelo_estruturas = []	
				modelo_estruturas = modelo_variogama(range_estruturas[:], sill_estruturas[:], tipo_estrutura[:], lag[:], numero_lags, numero_estruturas)    			
				#DEFINA O PRIMEIRO RESIDUO
		
				residuo = 0	
				residuo = desvio_quad(variograma, modelo_estruturas[:], numero_lags, numero_estruturas, resultado_pepita,p_distancia[:],p_pares[:])

				# DEFINA A LISTA DE PARAMETROS MODIFICADA

				range_estruturas_modficado = []
				sill_estruturas_modficado = []
				tipo_estruturas_modificado =[]
				pepita_modificado = 0
	

				# COPIE O VALOR INICIAL
		 
				range_estruturas_modificado = range_estruturas[:]
				sill_estruturas_modificado = sill_estruturas[:]
				tipo_estruturas_modificado = tipo_estrutura[:]
				pepita_modificado = resultado_pepita

				# FACA UMA COPIA DOS VALORES MEDIOS COMO UM VALOR DE RETORNO
				range_estruturas_inicial = []
				sill_estruturas_inicial = []
				tipo_estruturas_inicial =[]
				pepita_inicial = 0

				range_estruturas_inicial = range_estruturas[:]
				sill_estruturas_inicial = sill_estruturas[:]
				tipo_estruturas_inicial = tipo_estrutura[:]
				pepita_inicial = resultado_pepita

				# DEFINA AS VARIAVEIS DE SAIDA

				resultado_residuo = 0
				resultado_range = []
				resultado_estruturas =[]
				resultado_sill = []

				# DEFINA O PARAMETRO DE MODIFICACAO

				range_estrutura = 0
				sill_estrutura  =0
				modelo_estrutura =0

				# CONDICAO DE SOLUCAO ENCONTRADA

				convergencia_solucao = False

				# OTIMIZE A DIRECAO PRINCIPAL 
				#........................................................................................
				# FACA PARA O NUMERO DE INTERACOES ESTIPULADO
				for i in range(0,numero_interacoes):
				    # DEFINA UM NUMERO ALEATORIO PARA O PARAMETRO DO VARIOGRAMA A SER MODIFICADO
				    aleatorio_parametro = random.randint(0,numero_de_parametros)
				    # DEFINA SE O INCREMENTO SERA POSITIVO OU NEGATIVO
				    aleatorio_sinal  = random.choice([-1,1])
				    # SEGUNDO O NUMERO DO PARAMETRO ALEATORIO MODIFIQUE EM 7.5% O VALOR INICIAL
				    if (aleatorio_parametro < numero_estruturas):
					range_estrutura = range_estruturas[aleatorio_parametro]
					range_estrutura = range_estrutura + 0.075*aleatorio_sinal*range_estrutura
					if(restriction == 1):
						if (range_estrutura < min_range):				
							range_estrutura = min_range
						if (range_estrutura > max_range):
							range_estrutura = max_range
					range_estruturas_modificado[aleatorio_parametro] = range_estrutura
				    if (aleatorio_parametro >= numero_estruturas and aleatorio_parametro < 2*numero_estruturas):
					sill_estrutura = sill_estruturas[(aleatorio_parametro-numero_estruturas)]
					sill_estrutura = sill_estrutura + 0.075*aleatorio_sinal*sill_estrutura
					if (restriction == 1):
						if(sill_estrutura > max_contribution):
							sill_estrutura = max_contribution
						if(sill_estrutura < min_contribution):
							sill_estrutura = min_contribution
					sill_estruturas_modificado [(aleatorio_parametro - numero_estruturas)] = sill_estrutura
				    # DEFINA UM MODELO ALEATORIO PARA A ESTRUTURA
				    if (aleatorio_parametro >= 2*numero_estruturas and aleatorio_parametro < 3*numero_estruturas):
					aleatorio_modelo = random.randint(0,2)
					tipo_estruturas_modificado[aleatorio_parametro - 2*numero_estruturas] = aleatorio_modelo
				
				   
					
				    # DEFINA O SILL TOTAL
				    sill_total = 0
				    for j in range(0, numero_estruturas):
					sill_total = sill_total + sill_estruturas_modificado[j]
				    #  DEFINA UM EFEITO PEPITA
				    if (aleatorio_parametro >= 3*numero_estruturas and aleatorio_parametro < 4*numero_estruturas):
					pepita_modificado = math.fabs(pepita_modificado + 0.075*aleatorio_sinal*pepita_modificado)
					if (restriction == 1):
						if (pepita_modificado < min_nugget):
							pepita_modificado = min_nugget
						if (pepita_modificado > max_nugget):
							pepita_modificado = max_nugget
									   
				    # CALCULE O SILL TOTAL VERDADEIRO
		    
			 	    sill_total = sill_total + pepita_modificado
		    
				    range_estruturas_modificado.sort()
			   	    sill_estruturas_modficado.sort()
				    # DEFINA OS MODELOS PARA AS ESTRUTURAS VIGENTES
				    modelo_estruturas = modelo_variogama(range_estruturas_modificado[:], sill_estruturas_modificado[:], tipo_estruturas_modificado[:], lag[:], numero_lags, numero_estruturas)
				    residuo_modificado = desvio_quad(variograma,modelo_estruturas, numero_lags, numero_estruturas, pepita_modificado, p_distancia, p_pares)
				    #  ACEITAR OU REJEITAR MODIFICACAO BASEADO NA DIMINUICAO DO RESIDUO MEDIO QUADRADICO
				    if (residuo_modificado < residuo):
					if ((sill_total < max_patamar) and (sill_total > min_patamar)):
						convergencia_solucao = True
						r_range = []
						r_sill = []
						r_testr = []
						r_residuo = residuo_modificado
						r_range = range_estruturas_modificado[:]
						r_sill = sill_estruturas_modificado[:]
						r_testr = tipo_estruturas_modificado[:]		                
						r_pep = pepita_modificado
						residuo = residuo_modificado
					
				if (convergencia_solucao == True):
				    residuoV.append(r_residuo)
				    rangeV.append(r_range)
				    sillV.append(r_sill)
				    testerV.append(r_testr)
				    pepV.append(r_pep)

			
				#........................................................................................
				
				

		

			# TESTE DO LMC ---- SOMA DOS VARIOGRAMAS CRUZADOS DEVE SER MENOR QUE A SOMA DOS VARIOGRAMAS DIRETOS
			# TESTE EQUIVALENTE AO DETERMINANTE 

			soma_diretos =0
			soma_cruzados = 0
			
			#CRIE A MATRIZ DE CONTRIBUICOES
			indice = int(math.sqrt(nvariables))
			
			matriz_contr = []
			determ = []
			sillV_new = []
			for p in range(0,numero_estruturas):
				matriz = np.zeros((indice,indice))			
				for x in range(0,len(sillV)):
					
					sill_t = []
					sill_v = []				
					sill_t = sillV[x]
					sill_v = sill_t[p]
				
					i = indice_head[x]						
					j = indice_tail[x]
					i = i - 1
					j = j - 1					
					
					matriz[i][j] = sill_v
				
				#REGULARIZE A MATRIZ DE DE CONTRIBUICOES

				matriz_new = np.zeros((indice,indice))
				for i in range(0,int(math.sqrt(nvariables))):
					for j in range(0,int(math.sqrt(nvariables))):
						if (i==j):
							matriz_new[i][j] = matriz[i][j]
						else:
							matriz_new[i][j] = (matriz[i][j] + matriz[j][i])/2
				
				#DEFINA A CONTRIBUICAO PARA A ESTRUTURA
				sill_t_new =[]
				for i in range(0,int(math.sqrt(nvariables))):
						for j in range(0,int(math.sqrt(nvariables))):
							sill_t_new.append(matriz_new[i][j])
				sillV_new.append(sill_t_new)			
				determinante = np.linalg.det(matriz_new)
				determ.append(determinante)
				matriz_contr.append(matriz_new)

			

			#DEFINA AS ESTRUTURAS PARA CADA CONTRIBUICAO 

	
			for p in range(0,numero_estruturas):
				for x in range(0,nvariables):
					sillV[x][p] = sillV_new[p][x]
		
			
			def verif(v):
				for i in v:
					if i>0:
						pass
					else:
						return False
				return True
			
			if (determ > 0):
				check_LMC = verif(determ)

			#NORMALIZE OS EFEITOS PEPITAS -> VARIAVEL 12 = VARIAVEL 21
			

			#CRIE A MATRIZ DE EFEITOS PEPITA 
				
			matriz2 = np.zeros((indice,indice))			
			for x in range(0,len(pepV)):
				
				pep_t = []
				pep_v = []				
				pep_v = pepV[x]
				
			
				i = indice_head[x]						
				j = indice_tail[x]
				i = i - 1
				j = j - 1					
					
				matriz2[i][j] = pep_v

			#NORMALIZE OS EFEITOS PEPITAS -> VARIAVEL 12 = VARIAVEL 21
			
			matriz2_new = np.zeros((indice,indice))
			for i in range(0,int(math.sqrt(nvariables))):
				for j in range(0,int(math.sqrt(nvariables))):
					if (i==j):
						matriz2_new[i][j] = matriz2[i][j]
					else:
						matriz2_new[i][j] = (matriz2[i][j] + matriz2[j][i])/2

			#DEFINA O EFEITO PEPITA NORMALIZADO 
				
			pep_v_new =[]
			for i in range(0,int(math.sqrt(nvariables))):
				for j in range(0,int(math.sqrt(nvariables))):
					pep_v_new.append(matriz2[i][j])
					

			determ2 = np.linalg.det(matriz2_new)
		
			if (determ2 > 0):
				check_LMC2 = True
			
			count = count + 1
			if (count == 200):
				print("LMC not found")
				check_LMC = True
				check_LMC2 = True

		# FACA O RANGE MEDIO DAS VARIAVEIS 
	
		
		rangemedio = [0 for i in range(0,len(rangeV[0]))]		
		for m in rangeV:				
			for i in range(0,len(m)):
				rangemedio[i] = rangemedio[i] + m[i]/len(rangeV)
			
		
			
		# ADOTE O MODELO DA VARIAVEL PRIMARIA PARA TODOS OS TIPOS			
			
		modelo_adotado = []			
		modelo_adotado = testerV[0] 
			
		for i in range(0, len(testerV)):
			testerV[i] = modelo_adotado

		# ADOTE A MESMA CONTRIBUICAO E PEPITA E MODELO DA DIRECAO PRINCIPAL 

		if (direcao > 1):
			pepV = pepm
			testerV = modeling
			sillV = sillm
			
		if (direcao ==1):	
			print("Variogram parameters")
			print(".............................................................................")
			print("model = 0 -> spherical, model = 1 -> exponencial, model =2 -> gaussian")
			print(".............................................................................")					
			print("sills:" + str (matriz_contr)) 
			print("models:" + str(testerV[0]))
			print("nugget:" + str(matriz2_new))
			print("range: da direcao "+str(direcao) +"  "+ str(rangemedio))
		else:
			print("range: da direcao "+str(direcao) +"  "+ str(rangemedio))
			print(".............................................................................")
		

		# PLOTAGEM DE VERIFICACAO
		#CRIAR FUNCAO PARA PLOTAGEM
		
		
		arquivo2 = open("./ar2gems/bin/plugins/Geostat/python/plot/saida_automatic_fitting.txt","w")
		arquivo2.write(str(direcao)+"\n")
		arquivo2.write(str(nvariables)+"\n")
		arquivo2.write(str(nlags)+"\n")
		for n in range(0,nvariables):
			arquivo2.write(str(indice_head[n]) + "	"+str(indice_tail[n])+"\n")



		for n in range(0,nvariables):
			r_sill = sillV[n]
			r_range = rangemedio[0]
			r_pep = pepV[n]
			r_testr = testerV[n]
			variogramas = variogramasV[n]
			lags = lagsV[n]
			variograma = variogramas[I_dir_principal]
			lag = lags[I_dir_principal]

			funcao = []
			for i in np.linspace(0, max(lag), len(lag)):
		    		valor_variograma = 0
		    		for j in range(0, numero_estruturas):
		        		if (r_testr[j] == 0):
		            			if (i <= r_range):
		                			valor_variograma = valor_variograma + r_sill[j]*(1.5*i/r_range-0.5*math.pow((i/r_range),3))
		            			else:
		                			valor_variograma = valor_variograma + r_sill[j]
		        		elif (r_testr[j] == 1):
		            			valor_variograma = valor_variograma + r_sill[j]*(1-math.exp(-3*i/r_range))
		        		elif (r_testr[j] == 2):
		            			valor_variograma = valor_variograma + r_sill[j]*(1-math.exp(-3*pow(i/r_range,2)))
		    		valor_variograma = valor_variograma + r_pep
		    		funcao.append(valor_variograma)
			limite = np.linspace(0, max(lag),len(lag))

			# SALVAR ARQUIVO EM TXT COM OS DADOS

			for i in range(0,len(lag)):
				arquivo2.write(str(lag[i])+"	"+str(variograma[i])+"	"+str(limite[i])+"	"+str(funcao[i]) +"\n")
		arquivo2.close()
		os.system("python ./ar2gems/bin/plugins/Geostat/python/plot/plot_automatic_fitting.py")
		
		
		
		
		return testerV, pepV, sillV	

		
	if (set_maximumrange == 1 and set_minrange == 0 and set_verticalrange == 0):		
		pepV =[]		
		saida, pepV, sillV = otimizacao(I_dir_principal,variogramasV, lagsV, paresV, nvariables, tipo, numero_estruturas, restriction,min_contribution,max_contribution,min_nugget,max_nugget,min_range_max,max_range_max, -1, 1, -1, [] )
	if (set_maximumrange == 1 and set_minrange == 1 and set_verticalrange == 0):
		pepV =[]
		saida, pepV, sillV = otimizacao(I_dir_principal,variogramasV, lagsV, paresV, nvariables, tipo, numero_estruturas, restriction,min_contribution,max_contribution,min_nugget,max_nugget,min_range_max,max_range_max, -1, 1, -1, [] )
		saida2, pepd, sillV = otimizacao(I_dir_secundario,variogramasV, lagsV, paresV, nvariables, tipo, numero_estruturas, restriction,min_contribution,max_contribution,min_nugget,max_nugget,min_range_min,max_range_min, saida, 2, pepV, sillV )
	if (set_verticalrange == 1 and set_maximumrange ==1 and set_minrange == 1 ):  	
		pepV =[]
		saida, pepV, sillV = otimizacao(I_dir_principal,variogramasV, lagsV, paresV, nvariables, tipo, numero_estruturas, restriction,min_contribution,max_contribution,min_nugget,max_nugget,min_range_max,max_range_max, -1, 1, -1, [] )
		saida2, pepd, sillV = otimizacao(I_dir_secundario,variogramasV, lagsV, paresV, nvariables, tipo, numero_estruturas, restriction,min_contribution,max_contribution,min_nugget,max_nugget,min_range_min,max_range_min, saida, 2, pepV, sillV )	
		saida3, pepe, sillV = otimizacao(I_dir_vertical,variogramasV, lagsV, paresV, nvariables, tipo, numero_estruturas, restriction,min_contribution,max_contribution,min_nugget,max_nugget,min_range_vert,max_range_vert, saida, 3, pepV, sillV )     	

	# CORRECAO PROVISORIA DO BUG DE IMPORTACAO DO MATPLOTLIB NO SGEMS - INSERCAO DE UM LOOP INFINITO 

	running = True 
	while running:
		pass
	
		

    def finalize(self):
        print "Finalize optimizing_variogram"
        return True
    def name(self):
        return "automatic_fitting2"
##############################################
def get_plugins():
    return["automatic_fitting2"]
