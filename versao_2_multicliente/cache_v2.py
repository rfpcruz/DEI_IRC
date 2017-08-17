################################################################################ 
# Faculdade de Ciências e Tecnologia da Universidade de Coimbra                #
# Departamento de Engenharia Informática                                       #
# Unidade curricular: Introdução às Redes de Comunicação (2.ºAno / 1.º Sem.)   #
# Alunos: Ricardo Cruz e Gilberto Rouxinol                                     #
# Docentes: João P. Vilela e Tiago Cruz                                        #
#                                                                              #
# Projeto 2: Protocolo de Transferência de ficheiros com cache         2015/16 #
#                                                                              #
#                         Módulo "CACHE.PY"                                    #
#                                                                              #
################################################################################
from socket import *
import _thread
import sys
import os

#BEGIN: Estas funcoes sao para colocar no modulo iarc.py
def valida_publico(s):
   # Credenciais automaticas
   username = "Publico"
   password = "Publico"
   cred = username + " " + password + " " + "SERVIDOR"
   s.send(cred.encode('utf-8'))
   return s.recv(1024).decode('utf-8')

def download(s,nf):
   fn = "C:\\Users\\Palikir\\Dropbox\\rcruz-rouxinol\\CACHE\\Publico\\" + nf
   s.send("DOWNLOAD".encode('utf-8'))
   s.send(nf.encode('utf-8'))
   
   sizeFile = s.recv(1024).decode('utf-8')
   print("File size: " + sizeFile + " Bytes")
   
   f2 = open(fn,'wb')
   while True:
      x = s.recv(1024)
      if not x:
         print("Successfully download")
         f2.close()
         break
      f2.write(x)   
   pass

#END: Estas funcoes sao para colocar no modulo iarc.py

# Cria Socket Cache
meu_ender_Ch = ('', 20000)
cacheSocket = socket(AF_INET,SOCK_STREAM)
cacheSocket.bind(meu_ender_Ch)
cacheSocket.listen(10)

def clientthread(connectionSocket):
   print("Cache em modo escutar ...")
   while 1:
      #connectionSocket, addr = cacheSocket.accept()
      command = connectionSocket.recv(1024).decode('utf-8')
      
      #********************************************************************** LIST
      if command == "LIST":
      # Cria Socket na Cache modo Cliente
         ender_S = ('localhost',30000)
         clientSocket_c = socket(AF_INET, SOCK_STREAM)
         clientSocket_c.connect(ender_S) 
     # Cache vai Servidor    
         if valida_publico(clientSocket_c) == "True":
            clientSocket_c.send(command.encode('utf-8'))
            lista = clientSocket_c.recv(1024).decode('utf-8')
            # Cache vai cliente
            connectionSocket.send(lista.encode('utf-8'))
      #******************************************************************** UPLOAD
      elif command == "UPLOAD":
         f_Up = connectionSocket.recv(1024).decode('utf-8')
         n = "C:\\Users\\Palikir\\Dropbox\\rcruz-rouxinol\\CACHE\\Publico\\" + f_Up
         f2 = open(n,'wb')
         while True:
            x = connectionSocket.recv(1024)
            if not x:
               print("Upload concluido")
               f2.close()
               break
            f2.write(x)
      #******************************************************************* DOWLOAD  
      elif command == "DOWNLOAD":
         f_Dn = connectionSocket.recv(1024).decode('utf-8')        
         pf = "C:\\Users\\Palikir\\Dropbox\\rcruz-rouxinol\\CACHE\\Publico\\"
         file_name = pf + f_Dn 
         
         # Verifica existencia de f_Dn em pf
         filenames = os.listdir(pf)
         lista = ' '.join(filenames).split(" ")
         if f_Dn in lista:
            f1 = open(file_name,'rb')
            f1.seek(0,2)
            sizeFile = f1.tell()
            
            f1.seek(0)
            connectionSocket.send(str(sizeFile).encode('utf-8'))         
            for x in f1:
               connectionSocket.send(x)
            f1.close()
         else:
            # Vai servidor
            ender_S = ('localhost',30000)
            clientSocket_c = socket(AF_INET, SOCK_STREAM)
            clientSocket_c.connect(ender_S)
            valida_publico(clientSocket_c)
            download(clientSocket_c,f_Dn)
            
            # Envia Cliente
            f1 = open(file_name,'rb')
            f1.seek(0,2)
            sizeFile = f1.tell()
            f1.seek(0)
            connectionSocket.send(str(sizeFile).encode('utf-8'))         
            for x in f1:
               connectionSocket.send(x)
            f1.close()
      #********************************************************************** QUIT
      elif command == "QUIT":
         pass   
      #else:
         #print("Erro: Sem tarefa para executar")
         #pass
   #connectionSocket.close()
while 1:
   connectionSocket, addr = cacheSocket.accept()
   _thread.start_new_thread(clientthread,(connectionSocket,))  

connectionSocket.close()