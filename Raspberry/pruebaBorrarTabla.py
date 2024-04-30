import mysql.connector

def borrarTodo():
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

borrarTodo()