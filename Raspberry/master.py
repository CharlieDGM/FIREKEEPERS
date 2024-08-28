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
  
class dataBase:
    def addData(ubication):
        actualDate = datetime.now()
  
        temporalMark = actualDate.strftime('%d-%m-%Y %H:%M:%S')
  
        conn = mysql.connector.connect(
            host="localhost", 
            user="piPython", 
            password="pythonistrash", 
            database="prueba01",
        )

        cur = conn.cursor()
        cur.execute("INSERT INTO incendios (ubicacion, hora) values (%s, %s);", (ubication, temporalMark))
        conn.commit()
        conn.close()
        print(f"Se han ingresado con exito los datos", str(ubication), "y la hora: ", str(temporalMark))
  
    def deleteAllData():
        conn = mysql.connector.connect(
            host="localhost", 
            user="piPython", 
            password="pythonistrash", 
            database="prueba01",
        )
  
        cur = conn.cursor()
        cur.execute("DELETE FROM incendios;")
        conn.commit()
        conn.close()
        print("Se han eliminado todos los datos de la tabla.")
  
class camaras:
    def camaraLecture(cam, lowerLimit, nombreVentana):
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
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('192.168.1.17', 80))
    cliente.settimeout(10)
    
    alreadyActivated = False
      
    cam1 = cv2.VideoCapture(0)
    cam2 = cv2.VideoCapture(2)
    cam3 = cv2.VideoCapture(4)
      
    cams = [cam1, cam2, cam3]
    nombreVentanas = ['Camara 1: Radahn', 'Camara 2: Taehiung', 'Camara 3: Ether']
      
    try:
        while True:

            if cv2.waitKey(1) & 0xFF == ord('q'):
                dataBase.deleteAllData()
                break
    finally:
        for cam in cams:
            cam.release()
                  
        cv2.destroyAllWindows()  
        cliente.close()
