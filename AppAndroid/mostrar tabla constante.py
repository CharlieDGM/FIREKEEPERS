#gotta be honest, hice esto por enero y no recuerdo su funcionamiento exacto
import mysql.connector 

def verTabla(host_, user_, password_, database_, tabla_):
    try:
        conn = mysql.connector.connect(
            host=host_,
            user=user_,
            password=password_,
            database=database_,
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + tabla_ + "")

        rows = cursor.fetchall()

        for row in rows:
            print(row)
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

hostIn = input("Ingresa el host de la base de datos: ")
userIn = input("Ingresa tu usuario: ")
passwordIn = input("Ingresa tu contraseña: ")
databaseIn = input("Ingresa la DataBase a utilizar: ")
tablaIn = input("Ingresa la tabla a utilizar: ")

while True:
    verTabla(hostIn, userIn, passwordIn, databaseIn, tablaIn)