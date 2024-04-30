import mysql.connector
import RPi.GPIO as GPIO
from datetime import datetime

def AñadirDatos(ubication)
    fechaActual = datetime.now()
    
    marcaTemporal = fechaActual.strftime('%d-%m-%Y %H:%M:%S')
    
    conn = mysql.connector.connect(
        host="localhost",
        user="piPython",
        password="pythonistrash",
        database="prueba01",
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO incendios (ubicacion, hora) values (%s, %s);", (ubication,marcaTemporal))
    conn.commit()
    conn.close()
    print("Dato ingresado!")
    return 0

ubication = input("Ingresa el nombre de tu animal: ")

AñadirDatos(ubication)
