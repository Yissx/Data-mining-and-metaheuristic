import socket

host = "LocalHost" #Especifica el servidor
port = 5656 #Especifica el puerto
objsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se crea el socket que permite la conexión (Protocolo IPv4, socket tipo Stream)
objsocket.connect((host,port)) #Conectar
print("Iniciamos cliente \n ")
i = 0

while True: #loop infinito
    enviar = input("Cliente: ") #Esperando a que el cliente ingrese algo
    objsocket.send(enviar.encode(encoding="ascii", errors="ignore"))  #Enviar msj anterior
    recibido = objsocket.recv(1024) #Recibir msj del servidor
    print("Servidor", recibido.decode(encoding="ascii", errors="ignore")) #Imprimir msj recibido
objsocket.close() #Cerra conexión