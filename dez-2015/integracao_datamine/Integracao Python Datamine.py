#DEFINICAO DA CLASSE E FUNCOES DO SERVIDOR E IMPORTACAO DAS BIBLIOTECAS
class vizinhos:
  _public_methods_ = [ 'infoproto', 'calcvizinhos' ]
  _reg_progid_ = "CalcVizinhos"
  _reg_desc_ = "Python Test COM Server"
  import pythoncom
  _reg_clsid_ = str(pythoncom.CreateGuid()) # e.g. "{4D93DCBC-DE99-4D5A-ACFC-44F82BDB9889}"

  #ESTA FUNCAO RECEBE COMO ARGUMENTO O NUMERO DE BLOCOS EM Y E EM Z E O VALOR DO IJK DO ULTIMO BLOCO A PARTIR
  #DO JAVASCRIPT E RETORNA O MAXIMO I, J E K POSSIVEIS
  def infoproto(self,ny,nz,ijkultimobloco):
    import math

    #TRANSFORMA EM NUMERO OS ARGUMENTOS STRING QUE FORAM RECEBIDOS DO JAVASCRIPT
    ny = int(ny)
    nz = int(nz)
    ijkultimobloco = int(ijkultimobloco)

    #CALCULO DO MAXIMO I, J E K POSSIVEL
    imax = math.floor(ijkultimobloco/(ny * nz)) + 1
    jmax = math.floor((ijkultimobloco - (imax - 1) * ny * nz)/ nz) + 1
    kmax = ijkultimobloco - ((imax - 1) * ny * nz) - ((jmax - 1) * nz) + 1

    #ARMAZENA OS CALCULOS EM UM VETOR E RETORNA O MESMO PARA O JAVASCRIPT
    ijkmax=[imax,jmax,kmax]
    return str(ijkmax)

  #ESTA FUNCAO RECEBE COMO ARGUMENTO O NUMERO DE BLOCOS EM Y E EM Z E UM VETOR CONTENDO TODOS OS IJK DO MODELO
  #DE BLOCOS E RETORNA OS VIZINHOS DE CADA UM DOS MODELOS
  def calcvizinhos(self,ny,nz,vetorijk2,ijkmax2):
    import math

    #TRANSFORMA EM NUMERO E VETOR OS ARGUMENTOS RECEBIDOS DO JAVASCRIPT
    vetorijk = eval(vetorijk2)
    ijkmax = eval(ijkmax2)
    imax = int(ijkmax[0])
    jmax = int(ijkmax[1])
    kmax = int(ijkmax[2])
    ny = int(ny)
    nz = int(nz)

    ijkvizinhos = []
    for ijkbloco in vetorijk:
      #CALCULA O I, J E K DO BLOCO EM ANALISE, PARA CASO ELE SEJA DE BORDA DESCONSIDERE POSSIVEIS VIZINHOS INEXISTENTES
      ibloco = math.floor(ijkbloco/(ny * nz)) + 1
      jbloco = math.floor((ijkbloco - (ibloco - 1) * ny * nz)/ nz) + 1
      kbloco = ijkbloco - ((ibloco - 1) * ny * nz) - ((jbloco - 1) * nz) + 1

      #RESETA OS VALORES DOS IJK DOS VIZINHOS PARA A PROXIMA ITERACAO
      vizinhonorte = -99
      vizinhosul = -99
      vizinholeste = -99
      vizinhooeste = -99
      vizinhoemcima = -99
      vizinhoembaixo = -99

      #CALCULA O IJK DOS VIZINHOS, RESPEITANDO AS SITUACOES DE BLOCOS DE BORDA
      if(jbloco != jmax):
        vizinhonorte = ijkbloco + nz
      if(jbloco != 1):
        vizinhosul = ijkbloco - nz
      if(ibloco != imax):
        vizinholeste = ijkbloco + (ny * nz)
      if(ibloco != 1):
        vizinhooeste = ijkbloco - (ny * nz)
      if(kbloco != kmax):
        vizinhoemcima = ijkbloco + 1
      if(kbloco != 1):
        vizinhoembaixo = ijkbloco - 1

      #ARMAZENA NO FINAL DO VETOR O IJK DOS VIZINHOS
      ijkvizinhos.append(vizinhonorte)
      ijkvizinhos.append(vizinhosul)
      ijkvizinhos.append(vizinholeste)
      ijkvizinhos.append(vizinhooeste)
      ijkvizinhos.append(vizinhoemcima)
      ijkvizinhos.append(vizinhoembaixo)

    #RETORNA O VETOR DE VIZINHOS PARA O JAVASCRIPT
    return str(ijkvizinhos)

#REGISTRO DO SERVIDOR NO SISTEMA
if __name__ == "__main__":
  # use 'python com.py' to register the COM server
  # use 'python com.py --unregister' to unregister it
  print "Registering COM server..."
  import win32com.server.register
  win32com.server.register.UseCommandLine(vizinhos)