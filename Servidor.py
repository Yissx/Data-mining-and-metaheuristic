import socket
import sys
import os

#Conectar
host = "LocalHost" #Especifica el servidor
port = 5656 #Especifica el puerto
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se crea el socket que permite la conexión (Protocolo IPv4, socket tipo Stream)
server.bind((host,port)) #Indicar el servidor usado
server.listen(1)
print("Servidor en espera de conexiones")
active, addr = server.accept()

while True:
    recibido=active.recv(1024)
    print("Cliente: ", recibido.decode(encoding="ascii", errors="ignore"))
    #nombre = 'procesador' + recibido.decode(encoding="ascii", errors="ignore") + '.txt'
    #print(nombre)
    cantidad = int(recibido.decode(encoding="ascii", errors="ignore"))
    i = 0
    #print(cantidad)
    os.system("Planificador.py")
    os.system("Fase4.py")
    print("Planificador ejecutandose")
    print("Preprocesando datos")
    with open("Preprocesados/56-1.csv", 'rb') as f:
        while i < cantidad:
            data = f.read(1024)
            active.sendall(data)
            i += 1
        #data = f.read(1024)"""
    enviar = input("Server: ")
    active.send(enviar.encode(encoding="ascii", errors="ignore"))
active.close()
