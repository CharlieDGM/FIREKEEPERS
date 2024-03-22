import mysql.connector
import RPi.GPIO as GPIO
from datetime import datetime

def AñadirDatos(nombre, edad):
    fechaActual = datetime.now()
    
    marcaTemporal = fechaActual.strftime('%d-%m-%Y %H:%M:%S')
    
    conn = mysql.connector.connect(
        host="localhost",
        user="piPython",
        password="pythonistrash",
        database="prueba01",
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO pruebaTabla (especie, edad, hora) values (%s, %s, %s);", (nombre, edad,marcaTemporal))
    conn.commit()
    conn.close()
    print("Dato ingresado!")
    return 0

nombreIngresada = input("Ingresa el nombre de tu animal: ")
edadIngresada = int(input("Ingresa la edad de tu animal: "))

AñadirDatos(nombreIngresada, edadIngresada)