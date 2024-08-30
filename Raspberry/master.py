#alright esta es la primera version del codigo que estoy desarrollando para la competencia
#wro de este año, llevo ratos desarrollando pruebas asi que este solo es la union de varios
#codigos ya desarrollados, voy a subir de forma periodica el codigo a github
  
import cv2
import numpy as np
#librerias para opencv/vision artifical
  
import mysql.connector
import RPi.GPIO as GPIO
from datetime import datetime
#para conectarse y actualizar datos en la db (mariaDB)
  
import socket
#comunicación por red
import time
  
class database:
    def anadirDatos(ubicacion):
        fechaActual = datetime.now()
  
        marcaTemporal = fechaActual.strftime('%d-%m-%Y %H:%M:%S') #almacenamos la marcatemporal para anadirla despues
  
        conn = mysql.connector.connect(
            host="localhost", 
            user="piPython", 
            password="pythonistrash", 
            database="prueba01",
        ) #nos conectamos a la base de datos.

        cur = conn.cursor()
        cur.execute("INSERT INTO incendios (ubicacion, hora) values (%s, %s);", (ubicacion, marcaTemporal))
        conn.commit() #realizamos una query a la base de datos para insertar ciertos valores.
        conn.close()
        print(f"Se han ingresado con exito los datos: ", str(ubicacion), ", y la hora: ", str(marcaTemporal))
  
    def borrarTodo():
        conn = mysql.connector.connect(
            host="localhost", 
            user="piPython", 
            password="pythonistrash", 
            database="prueba01", #ingresamos a la base de datos.
        )
  
        cur = conn.cursor()
        cur.execute("DELETE FROM incendios;")
        conn.commit()
        conn.close() #ejecutamos una query que elimina la tabla actuar
        print("Todos los datos se han eliminado de la base de datos.")
  
class camaras:
    def lecture(cam, lowerLimit, nombreVentana):
        _, preFrame = cam.read()
        frame = cv2.flip(preFrame, 0)
        #(lo primero es para obtener un valor que no necesitamos xdd)
        #obtenemos una lectura de la camara y volteamos la imagen porque las camaras estan al reves xdd
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #convertimos los colores a HSV el frame pasado (Hue, Saturation, Value) para su manipulacion
  
        lowerColor = np.array([0, 75, 50])
        upperColor = np.array([30, 255, 255])
        #arrays de colores en hsv, nuestro margen de detección (margen de que punto a que punto vamos a detectar)
  
        mask = cv2.inRange(hsv, lowerColor, upperColor)
        #una "mascara" binaria, en la cual el 1 (blanco) representa si el pixel cumple con el rango establecido y 0 (negro) si no 
  
        numPixels = cv2.countNonZero(mask)
        #contamos la cantidad de pixeles en la mascara que cumplieron con el margen
        totalPixels = mask.shape[0] * mask.shape[1]
        #multiplicamos el ancho por el alto para saber cuantos pixeles hay en la camara
        percentage = (numPixels * 100) / totalPixels
        #formula para obtener porcentaje
  
        #creamos una ventana para poder mostrarla xdd
        cv2.namedWindow(nombreVentana, cv2.WINDOW_NORMAL)
        cv2.imshow(nombreVentana, mask)
          
        if percentage >= lowerLimit:
            return True
        else: 
              return False
           
#creamos y configuramos la conexion a la red del ESP32
   
if __name__ == '__main__':
    ipServer = '192.168.1.2'
    puerto = 80
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((ipServer, puerto))
    cliente.settimeout(10) #configuramos y realizamos una coneccion de red atraves de un socket
    
    cam1 = cv2.VideoCapture(0)
    cam2 = cv2.VideoCapture(2)
    cam3 = cv2.VideoCapture(4)
      
    cams = [cam1, cam2, cam3]
    nombreVentanas = ['Camara 1: Radahn', 'Camara 2: Taehiung', 'Camara 3: Ether']
    respuestas = ["derecha\n", "frente\n", "izquierda\n"]
    #Creamos los diferentes objetos y listas que utilizaremos para facilitar el algoritmo
    
    time.sleep(3.5)
    ultimoEnvio = time.time()
    try:
        while True:
            try:
                tiempoActual = time.time()
                for n in range(3):
                    if camaras.lecture(cams[n], 30, nombreVentanas[n]):
                        mensaje = respuestas[n]
                        if tiempoActual - ultimoEnvio >= 6:
                            cliente.send(mensaje.encode('utf-8'))
                            print(f"Cambio detectado. Camara: {respuestas[n]}")
                            ultimoEnvio = tiempoActual
                mensajeESP = cliente.recv(1024).decode('utf-8').rstrip()
                if mensajeESP:
                    print(f"Mensaje del ESP32: {mensajeESP}")
                    if mensajeESP == "encendido":
                        database.anadirDatos("general")
                        #print(f"Se han anadido los datos a la base de datos")
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    database.borrarTodo()
                    break
                
            except socket.timeout:
                print("Error de conexion. Reconectando esta cosa xdd...")
                cliente.close()
                cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #si hay timeout cerramos y volvemos a abrir el objeto
                cliente.connect((ipServer, puerto)) #realizamos reconeccion
                
            except socket.error as e:
                print(f"Error de socket: {e}")
                cliente.close() #lo mismo pero con algun error estandar de socket
                cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cliente.connect((ipServer, puerto)) #realizamos reconeccion
    finally:
        for cam in cams:
            cam.release()
                  
        cv2.destroyAllWindows()  
        cliente.close()
