################################################################################ 
# Faculdade de Ciências e Tecnologia da Universidade de Coimbra                #
# Departamento de Engenharia Informática                                       #
# Unidade curricular: Introdução às Redes de Comunicação (2.ºAno / 1.º Sem.)   #
# Alunos: Ricardo Cruz e Gilberto Rouxinol                                     #
# Docentes: João P. Vilela e Tiago Cruz                                        #
#                                                                              #
# Projeto 2: Protocolo de Transferência de ficheiros com cache         2015/16 #
#                                                                              #
#                         Módulo "SERVIDOR.PY"                                 #
#                                                                              #
################################################################################
from socket import *
import _thread
import sys
import os

raiz_Dir = "C:\\Users\\Palikir\\Dropbox\\rcruz-rouxinol\\"

def valida_UserPass(utilizador,password):
   name = raiz_Dir + "SERVIDOR\\registosClientes.txt"
   f = open(name, 'r',encoding = 'utf-8')
   registos = f.readlines()
   f.close()
   list_up = []
   for i in registos:
      aux = i[:].split(',')
      list_up.append(aux)
   list_u = []
   list_p = []
   for i in range(len(list_up)):
      aux = list_up[i][0][:-1]
      if aux == "BEGIN":
         for j in range(i+1,len(list_up)):
            aux_u = list_up[j][0]
            if aux_u != "END":
               list_u.append(aux_u)
               aux_p = list_up[j][1][1:-1]
               list_p.append(aux_p)
   dic = {}
   dic = dict(zip(list_u,list_p))
   for i in range(len(list_u)):
      if utilizador == list_u[i]:    
         p = dic.get(utilizador)
         if password == p:            
            a = "True"
            break
         else:
            a = "False"
      else:
         a = "False"
   return a

# Cria Socket Servidor
meu_ender_S = ('',30000)
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(meu_ender_S)
serverSocket.listen(10)

def clientthread(connectionSocket):
   print('Servidor em modo escutar ...')
   while 1:
      cred = connectionSocket.recv(1024).decode('utf-8')
      u, p, d = cred.split()[0], cred.split()[1], cred.split()[2]
      print(cred)
      aut = valida_UserPass(u, p)
      connectionSocket.send(aut.encode('utf-8'))
      
      comando = connectionSocket.recv(1024).decode('utf-8')
      #******************************************************************** LIST
      if comando == 'LIST':
         filenames = os.listdir(raiz_Dir + d + "\\" + u)
         lista = ' '.join(filenames)
         connectionSocket.send(lista.encode('utf-8'))
       #***************************************************************** UPLOAD
      elif comando == 'UPLOAD':
         f_Up = connectionSocket.recv(1024).decode('utf-8')
         n = "C:\\Users\\Palikir\\Dropbox\\rcruz-rouxinol\\SERVIDOR\\" + u + "\\" + f_Up
         f2 = open(n,'wb')
         while True:
            x = connectionSocket.recv(1024)
            if not x:
               print("Upload concluido")
               f2.close()
               break
            f2.write(x)
       #*************************************************************** DOWNLOAD
      elif comando == "DOWNLOAD":
         f_Dn = connectionSocket.recv(1024).decode('utf-8')
         file_name = "C:\\Users\\Palikir\\Dropbox\\rcruz-rouxinol\\SERVIDOR\\" + u  + "\\" + f_Dn 
         try:
            f1 = open(file_name,'rb')
         except NameError as txt_error:
            print("\nErro: Ficheiro inexistente !\n\n" + txt_error)
            
         f1.seek(0,2)
         sizeFile = f1.tell()
         f1.seek(0)
         connectionSocket.send(str(sizeFile).encode('utf-8'))
         
         for x in f1:
            connectionSocket.send(x)
         print("Successfully dowload")
         f1.close()
      #******************************************************************** QUIT
      elif comando == "QUIT":
         pass
      #else: 
       #  print("Erro: Sem tarefa para executar")

while 1:
   connectionSocket, addr = serverSocket.accept()
   _thread.start_new_thread(clientthread,(connectionSocket,))   
   
connectionSocket.close()