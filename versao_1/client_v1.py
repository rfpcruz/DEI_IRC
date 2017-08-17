################################################################################ 
# Faculdade de Ciências e Tecnologia da Universidade de Coimbra                #
# Departamento de Engenharia Informática                                       #
# Unidade curricular: Introdução às Redes de Comunicação (2.ºAno / 1.º Sem.)   #
# Alunos: Ricardo Cruz e Gilberto Rouxinol                                     #
# Docentes: João P. Vilela e Tiago Cruz                                        #
#                                                                              #
# Projeto 2: Protocolo de Transferência de ficheiros com cache         2015/16 #
#                                                                              #
#                         Módulo "CLIENTE.PY"                                  #
#             (Módulo dependente do módulo "iarc.py")                          #
################################################################################
import sys
import os
import getpass
from socket import *



def escolha():
   print("\nIntroduzir: LIST")
   print("            DOWNLOAD + <filename> ")
   print("            UPLOAD   + <filename> ")
   print("            QUIT")
   inCl = input("")
   return inCl

def cabecalho():
   print(" _________________________________________________________ ")
   print("|             SERVIDOR DE TRANSFERENCIA DE FICHEIROS      |")
   print("|_________________________________________________________|")
   print("\nIntroduzir: 0 (Sem autenticar)")
   print("            1 (Autenticar   ")
   print("         QUIT (Sair)")
   o = input("")
   return o

def listar(s):
   s.send("LIST".encode('utf-8'))
   print(s.recv(1024).decode('utf-8')) 

def upload(s,nf):
   fn = "C:\\Users\\Palikir\\Dropbox\\rcruz-rouxinol\\CLIENTE\\" + nf
   s.send("UPLOAD".encode('utf-8'))
   s.send(nf.encode('utf-8'))
   
   try:
      f1 = open(fn,'rb')
   except NameError as txt_error:
      print("\nError: Not file exist\n\n" + txt_error)
      
   f1.seek(0,2)
   sizeFile = f1.tell()
   f1.seek(0)
   print("File size: " , sizeFile, " Bytes")
   
   for x in f1:
      s.send(x)
   print("Successfully upload")
   f1.close()

def download(s,nf):
   fn = "C:\\Users\\Palikir\\Dropbox\\rcruz-rouxinol\\CLIENTE\\" + nf
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

def valida_cliente(s):
   # Cliente fornece credenciais
   username = input("Username: ")
   password = input("Password: ") #password = getpass.getpass("Pass: ")
   cred = username + " " + password + " " + "SERVIDOR"
   s.send(cred.encode('utf-8'))
   return s.recv(1024).decode('utf-8')


cliente_em_atividade = 1

opcao = cabecalho()
if opcao == "QUIT":
   cliente_em_atividade = -1
   print ('\nExit ... \n')

while cliente_em_atividade > 0:
   if opcao == "0": #CLIENTE PUBLICO CLIENTE PUBLICO CLIENTE PUBLICO CLIENTE PUB
      # Cria Socket Cliente
      ender_Ch = ('localhost', 12000)
      clientSocket = socket(AF_INET, SOCK_STREAM)
      clientSocket.connect(ender_Ch)
      
      # Opcao do Cliente
      input_Cl = escolha()
      command = input_Cl.split()[0]
      if command == "LIST":
         listar(clientSocket)
      elif command == "UPLOAD":
         fup = input_Cl.split()[1]
         upload(clientSocket,fup)
      elif command == "DOWNLOAD":
         fdow = input_Cl.split()[1]
         download(clientSocket,fdow)
      elif command == "QUIT":
         clientSocket.send("QUIT".encode('utf-8'))
         cliente_em_atividade = -1       
         clientSocket.close()
      else:
         print ("Option not found")
         escolha()   
   
   elif opcao == '1': #CLIENTE PRIVADO CLIENTE PRIVADO CLIENTE PRIVADO CLIENTE P
      # Cria Socket Cliente
      ender_Sv = ('localhost', 12005)
      clientSocket = socket(AF_INET, SOCK_STREAM)
      clientSocket.connect(ender_Sv)
      
      if valida_cliente(clientSocket) == "True":
         print("\nSuccessfully Login")
         # Opcao do Cliente logado
         input_Cl = escolha()
         command = input_Cl.split()[0]
         if command == "LIST":            
            listar(clientSocket)
         elif command == "UPLOAD":
            fup = input_Cl.split()[1]
            upload(clientSocket,fup)            
         elif command == "DOWNLOAD": 
            fdow = input_Cl.split()[1]
            download(clientSocket,fdow)
         elif command == "QUIT":
            clientSocket.send("QUIT".encode('utf-8'))
            cliente_em_atividade = -1       
            clientSocket.close()         
         else:
            print("Erro: Sem tarefa para ordenar")  
      else: 
         print("Invalid username or password, Goodbye.")
         cliente_em_atividade = -1
         clientSocket.close()
   else:
      print ("Opcao invalida")
      cabecalho()
print ('\nA sair ... \n')