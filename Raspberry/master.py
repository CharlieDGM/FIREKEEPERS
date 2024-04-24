#alright esta es la primera version del codigo que estoy desarrollando para la competencia
#wro de este año, llevo ratos desarrollando pruebas asi que este solo es la union de varios
#codigos ya desarrollados, voy a subir de forma periodica el codigo a github

import cv2
import numpy as np
#librerias para opencv/vision artifical

import mysql.connector
import RPi.GPIO as GPIO
from datetime import datetime
#(todavia no agregado) para conectarse y actualizar datos en la db (mariaDB)

import serial
#comunicación serial

class dataBase:
    def addData(state, ubication):
        actualDate = datetime.now()

        temporalMark = actualDate.strftime('%d-%m-%Y %H:%M:%S')

        conn = mysql.connector.connect(
            host="localhost", 
            user="piPython", 
            password="pythonistrash", 
            database="prueba01",
        )

        cur = conn.cursor()
        cur.execute("INSERT INTO ////// (ubication, state, time) values (%s, %s, %s);", (ubication, state,temporalMark))
        conn.commit()
        conn.close()
        print(f"Se han ingresado con exito los datos", str(ubication), "y ", str(state))

    def deleteAllData():
        conn = mysql.connector.connect(
            host="localhost", 
            user="piPython", 
            password="pythonistrash", 
            database="prueba01",
        )

        cur = conn.cursor()
        cur.execute("DELETE * FROM //////;")
        conn.commit()
        conn.close()
        print("Se han eliminado todos los datos de la tabla.")

class camaras:
    def camara1Lecture():
        _, frame = cam1.read()
        #(lo primero es para obtener un valor que no necesitamos) obtenemos una lectura de la camara
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #convertimos los colores a HSV (Hue, Saturation, Value) para su manipulacion

        lower_color = np.array([40, 50, 50])
        upper_color = np.array([80, 255, 255])
        #arrays de colores en hsv, nuestro margen de detección (margen de que punto a que punto vamos a detectar)

        mask = cv2.inRange(hsv, lower_color, upper_color)
        #una "mascara" binaria, en la cual el 1 (blanco) representa si el pixel cumple con el rango establecido y 0 (negro) si no 

        num_pixels = cv2.countNonZero(mask)
        #contamos la cantidad de pixeles en la mascara que cumplieron con el margen
        total_pixels = mask.shape[0] * mask.shape[1]
        #multiplicamos el ancho por el alto para saber cuantos pixeles hay en la camara
        percentage = (num_pixels * 100) / total_pixels
        #formula para obtener porcentaje

        #cv2.imshow('Original', frame)
        cv2.imshow('Mask', mask)
        return percentage
    
    def camara2Lecture():
        _, frame = cam2.read()
        #(lo primero es para obtener un valor que no necesitamos) obtenemos una lectura de la camara
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #convertimos los colores a HSV (Hue, Saturation, Value) para su manipulacion

        lower_color = np.array([40, 50, 50])
        upper_color = np.array([80, 255, 255])

        mask = cv2.inRange(hsv, lower_color, upper_color) 

        num_pixels = cv2.countNonZero(mask)
        total_pixels = mask.shape[0] * mask.shape[1]
        percentage = (num_pixels * 100) / total_pixels

        cv2.imshow('Mask', mask)
        return percentage
    
    def camara3Lecture():
        _, frame = cam3.read()
        #(lo primero es para obtener un valor que no necesitamos) obtenemos una lectura de la camara
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #convertimos los colores a HSV (Hue, Saturation, Value) para su manipulacion

        lower_color = np.array([40, 50, 50])
        upper_color = np.array([80, 255, 255])

        mask = cv2.inRange(hsv, lower_color, upper_color) 

        num_pixels = cv2.countNonZero(mask)
        total_pixels = mask.shape[0] * mask.shape[1]
        percentage = (num_pixels * 100) / total_pixels

        cv2.imshow('Mask', mask)
        return percentage
    
    def camara4Lecture():
        _, frame = cam4.read()
        #(lo primero es para obtener un valor que no necesitamos) obtenemos una lectura de la camara
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #convertimos los colores a HSV (Hue, Saturation, Value) para su manipulacion

        lower_color = np.array([40, 50, 50])
        upper_color = np.array([80, 255, 255])

        mask = cv2.inRange(hsv, lower_color, upper_color) 

        num_pixels = cv2.countNonZero(mask)
        total_pixels = mask.shape[0] * mask.shape[1]
        percentage = (num_pixels * 100) / total_pixels

        cv2.imshow('Mask', mask)
        return percentage

class serialCom:
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
        print(f"Enviado: {mensajeToSend}")
        
if __name__ == '__main__':
    cam1 = cv2.VideoCapture(0)
    #cam2 = cv2.VideoCapture(2)
    #cam3 = cv2.VideoCapture(4)
    #cam4 = cv2.VideoCapture(6)
    
    serial = serial.Serial(
        port='/dev/ttyS0', #ttyS0 son los pines RX y TX, el puerto de conexión puede variar
        baudrate=9600, #no cambiar, esta sincronizado con el arduino
        timeout=2
    ) #datos de conección UART
    serial.flush()
    #se limpia todo mensaje que exista en ese momento
    try:
        while True:
            camaras.camara1Lecture()
            serialCom.serialLecture()
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam1.release()
        #cam2.release()
        #cam3.release()
        #cam4.release()
        
        cv2.destroyAllWindows()
        
        serial.close()