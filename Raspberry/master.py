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
  
import serial
#comunicación serial
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
  
def serialLecture():
    if serial.in_waiting > 0:
        #serial.reset_input_buffer()
        #supuestamente es para limpiar el input pero esta linea genera mas problemas
        mensaje = serial.readline().decode('utf-8').rstrip()
        #por partes: se lee la linea recibida, se decodifica y se limpian los espacios en blanco
        print(mensaje)
        return mensaje
              
def serialSend(mensajeToSend):
    if type(mensajeToSend) != str:
        str(mensajeToSend)
    mensaje = f"{mensajeToSend}\n"
    serial.write(mensaje.encode('utf-8'))
    time.sleep(0.003)
    serial.write(mensaje.encode('utf-8'))
    time.sleep(0.003)
    serial.write(mensaje.encode('utf-8'))
    time.sleep(0.003)
    serial.write(mensaje.encode('utf-8'))
    print(f"Enviado: {mensajeToSend}")
          
if __name__ == '__main__':
    alreadyActivated = False
      
    cam1 = cv2.VideoCapture(0)
    cam2 = cv2.VideoCapture(2)
    cam3 = cv2.VideoCapture(4)
      
    cams = [cam1, cam2, cam3]
    nombreVentanas = ['cam1', 'cam2', 'cam3']
      
    serial = serial.Serial(
        port='/dev/ttyS0', #ttyS0 son los pines RX y TX, el puerto de conexión puede variar
        baudrate=9600, #no cambiar, esta sincronizado con el ESP32
        timeout=2
    ) #datos de conección UART
    serial.flush()
    #se limpia todo mensaje que exista en ese momento
    try:
        while True:
            for n in range(3):
                if camaras.camaraLecture(cams[n], 15, nombreVentanas[n]):
                    print(f"Camara {n+1} True.")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                dataBase.deleteAllData()
                break
    finally:
        for cam in cams:
            cam.release()
                  
        cv2.destroyAllWindows()  
        serial.close()
