import socketserver
import socket
import os
import threading
## Python 3.7

# Direccion y puerto local
host = "localhost"
# Puertos enviar respuestas
lsPuerto = [9999, 9998, 9997] 

# # Direccion y puerto local, comuncacion servidor intermedio
# host = "localhost"
# puerto = 9998
# puertoSuma = "9997"
# operacion = "suma"

# # Creamos los socket
# socket2 = socket.socket()
# # Establecemos conexion con servidor intermedio
# socket2.connect((host, puerto))
# listaDir = []
# # Agregamos a lista
# listaDir.append(host)
# listaDir.append(puertoSuma)
# listaDir.append(operacion)
# # Convertimos de lista a string
# listaStringDir = ' '.join(listaDir)
# socket1.send(listaStringDir.encode("UTF-8"))

# Clase socket servidor	Suma
class miHandler(socketserver.BaseRequestHandler):

	def handle(self):

		# Recibe 2 numeros, de a 1024 datos
		self.numeros = str(self.request.recv(1024).decode("UTF-8"))
		print("los numeros recibidos son: ", self.numeros)

		# Convertimos a lista
		self.listaNum = self.numeros.split()
		# Convertimos a enteros para operar
		self.num1 = int(self.listaNum[0])
		self.num2 = int(self.listaNum[1])
		self.ope = (self.listaNum[2])

		# Llamamos la funcion resta y Convertimos a String el resultado de la suma
		self.sumar = str(suma(self.num1, self.num2))
		print("La suma es =", self.sumar)

		# Enviamos el resultado
		self.request.send(self.sumar.encode("UTF-8"))


#Creando hilo para servidor
class serverThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		print("\n\t\tTaller 5 \nservidor intermedio listado dinámico descentralizado\n")
		print("\n\t Servidor Suma escuchando...\n")
		print("Conexion establecida con cliente ...")
		host2 = "localhost"
		# Llamamos la clase socket servidor con los parametros de direccion y puerto
		server1 = socketserver.TCPServer((host2, lsPuerto[0]), miHandler)
		# Mantenemos al servidor en estado de escucha
		server1.handle_request()
		

def menu():
   print("___________________________________________________")
   print("\t\t*MENU DE OPERACIONES*")
   print("1. SUMA")
   print("2. RESTA")
   print("3. MULTIPLICACION")
   print("4. DIVISION")
   print("5. POTENCIACION")
   print("6. LOGARITMACION")
   print("0. PARA SALIR")

# Funcion que recibe los datos digitados
def digitarNumero():
   x = (input("ingrese el primer numero: "))
   y = (input("Ingrese el segundo numero: "))

   return x, y

def suma(numero1, numero2):
	return int(numero1) + int(numero2)    

def conexionSerFinal(n1, n2, op, nh, np): #nh nuevo host, np nuevo puerto
	# Conectamos con el servidor
	socket2 = socket.socket()
	socket2.connect((nh, np))

	listaN = []
	# Agregamos a lista
	listaN.append(n1)
	listaN.append(n2)
	listaN.append(op)
	# Convertimos de lista a string
	listaStringN = ' '.join(listaN)

	# Enviamos los 2 valores a operar al servidor 
	socket2.send(listaStringN.encode("UTF-8"))
	# Recibimos el resultado del servidor
	res = str(socket2.recv(1024).decode("UTF-8"))

	return res  

def conexionSerInter(op):
	# Creamos los socket
	socket1 = socket.socket()
	# Establecemos conexion con servidor intermedio
	socket1.connect((host, lsPuerto[2]))

	# Enviamos el socket con los datos de operacion a servidor intermedio
	socket1.send(op.encode("UTF-8"))
	# Recibimos la direccion del servidor multi del servidor intermedio
	dirServidorE = socket1.recv(1024).decode("UTF-8")

	# Convertimos a lista
	listaDir = dirServidorE.split()
	host1 = listaDir[0]
	# Convertimos el puerto a entero
	puerto1 = int(listaDir[1])

	return host1, puerto1

# Principal
class serverThread2(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		menu()
		while True:
			opcion = (input("Digite la operacion a realizar: "))

			if opcion == "1":
				# Llamamos la funcion que nos entrega los numeros digitados
				numero1, numero2 = digitarNumero()

				# Llamamos la funcion suma
				resultadoSuma = (suma(numero1, numero2))
				print("\nNumero 1 = "+ numero1 + ", Numero 2 = " + numero2 + ", Operacion = ", opcion)
				print("\nEl resultado de la suma es =", resultadoSuma)
				print("\n")
				
			if opcion == "2":
				# Llamamos la funcion que nos enterga los numeros digitados
				numero1, numero2 = digitarNumero()

				# Llamamos la funcion conexion con Servidor Final
				resultadoResta = conexionSerFinal(numero1, numero2, opcion, host, lsPuerto[1])
				print("\nNumero 1 = "+ numero1 + ", Numero 2 = " + numero2 + ", Operacion = ", opcion)
				print("\nEl resultado de la resta es =", resultadoResta)
				print("\n")
							
			if opcion == "3": 
                # Llamamos la funcion que nos enterga los numeros digitados
				numero1, numero2 = digitarNumero()

				# Llamamos la funcion conexion con Servidor Final
				resultadoMulti = conexionSerFinal(numero1, numero2, opcion, host, lsPuerto[2])
				print("\nNumero 1 = "+ numero1 + ", Numero 2 = " + numero2 + ", Operacion = ", opcion)
				print("\nEl resultado de la multiplicacion es =", resultadoMulti)
				print("\n")
			
			if opcion == "4": 
                # Llamamos la funcion que nos enterga los numeros digitados
				numero1, numero2 = digitarNumero()
				
				# Llamamos la funcion conexion con Servidor Intermedio
				nuevoHost, nuevoPuerto = conexionSerInter(opcion)
				print("\nLa direccion del servidor suma es: ", nuevoHost, nuevoPuerto)

				# Llamamos la funcion conexion con Servidor Final
				resultadoDivi = conexionSerFinal(numero1, numero2, opcion, nuevoHost, nuevoPuerto)
				print("\nNumero 1 = "+ numero1 + ", Numero 2 = " + numero2 + ", Operacion = ", opcion)
				print("\nEl resultado de la division es =", resultadoDivi)
				print("\n")
				
			if opcion == "5":
                # Llamamos la funcion que nos enterga los numeros digitados
				numero1, numero2 = digitarNumero()

				# Llamamos la funcion conexion con Servidor Final
				resultadoPot = conexionSerFinal(numero1, numero2, opcion, host, lsPuerto[4])
				print("\nNumero 1 = "+ numero1 + ", Numero 2 = " + numero2 + ", Operacion = ", opcion)
				print("\nEl resultado de la potencia es =", resultadoPot)
				print("\n")
				
			if opcion == "6":	
				# Llamamos la funcion que nos enterga los numeros digitados
				numero1, numero2 = digitarNumero()

				# Llamamos la funcion conexion con Servidor Final
				resultadoLog = conexionSerFinal(numero1, numero2, opcion, host, lsPuerto[5])
				print("\nNumero 1 = "+ numero1 + ", Numero 2 = " + numero2 + ", Operacion = ", opcion)
				print("\nEl resultado del logaritmo es =", resultadoLog)
				print ("\n")

hiloServer = serverThread()
hiloServer.start()
hiloCliente = serverThread2()
hiloCliente.start()		
