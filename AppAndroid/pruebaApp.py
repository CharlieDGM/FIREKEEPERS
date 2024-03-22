import mysql.connector
import tkinter as tk

def verTabla(host_, user_, password_, database_, tabla_, cuadroTexto):
    try:
        conn = mysql.connector.connect(
            host=host_,
            user=user_,
            password=password_,
            database=database_,
        )

        cursor = conn.cursor()
        cuadroTexto.delete(1.0, tk.END) 
        
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = '" + tabla_ + "';") 
        nombresCol = cursor.fetchall()
        colNamesPrint = [nomCol[0] for nomCol in nombresCol]
        cuadroTexto.tag_configure("header", foreground="blue", font=("Arial", 15, "bold"))
        cuadroTexto.insert(tk.END, ', '.join(colNamesPrint) + "\n", "header")

        cursor.execute("SELECT * FROM " + tabla_)
        rows = cursor.fetchall()
        cuadroTexto.tag_configure("list", foreground="black", font=("Arial", 12, "bold"))
        for row in rows:
            cuadroTexto.insert(tk.END, str(row) + "\n", "list")

    except mysql.connector.Error as err:
        cuadroTexto.insert(tk.END, f"Error: {err}\n")

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def clickBoton():
    def actualizarDatos():
        hostIn = host_entry.get()
        userIn = user_entry.get()
        passwordIn = password_entry.get()
        databaseIn = database_entry.get()
        tablaIn = tabla_entry.get()

        verTabla(hostIn, userIn, passwordIn, databaseIn, tablaIn, cuadroTexto)

        app.after(5000, actualizarDatos)
    
    actualizarDatos()

def on_resize(event):
    update_layout()

def update_layout():
    window_width = app.winfo_width()
    window_height = app.winfo_height()

    entry_width = window_width // 6
    entry_height = window_height // 10

    host_entry.config(width=entry_width)
    user_entry.config(width=entry_width)
    password_entry.config(width=entry_width)
    database_entry.config(width=entry_width)
    tabla_entry.config(width=entry_width)

    font_size = max(10, entry_height // 4)
    font = ("Arial", font_size)

    host_entry.config(font=font)
    user_entry.config(font=font)
    password_entry.config(font=font)
    database_entry.config(font=font)
    tabla_entry.config(font=font)

    text_width = window_width // 8
    text_height = window_height // 24
    text_font_size = max(8, text_height // 3)
    text_font = ("Arial", text_font_size)
    cuadroTexto.config(font=text_font, width=text_width, height=text_height)

    button_width = window_width // 16
    button_height = window_height // 200
    button_font_size = max(12, button_height // 3)
    button_font = ("Arial", button_font_size)
    button.config(width=button_width, height=button_height, font=button_font)


app = tk.Tk()
app.title("Tabla AutoActualizable - Query Automatico")

app.update_idletasks()
app.geometry("350x700")

tk.Label(app, text="Host:").grid(row=0, column=0)
host_entry = tk.Entry(app)
host_entry.grid(row=0, column=1)

tk.Label(app, text="Usuario:").grid(row=1, column=0)
user_entry = tk.Entry(app)
user_entry.grid(row=1, column=1)

tk.Label(app, text="Contraseña:").grid(row=2, column=0)
password_entry = tk.Entry(app, show="*")
password_entry.grid(row=2, column=1)

tk.Label(app, text="Database:").grid(row=3, column=0)
database_entry = tk.Entry(app)
database_entry.grid(row=3, column=1)

tk.Label(app, text="Tabla:").grid(row=4, column=0)
tabla_entry = tk.Entry(app)
tabla_entry.grid(row=4, column=1)

cuadroTexto = tk.Text(app, height=10, width=40)
cuadroTexto.grid(row=5, column=0, columnspan=2)

button = tk.Button(app, text="Ver Tabla!1!!!", command=clickBoton)
button.grid(row=6, column=0, columnspan=2)

app.bind("<Configure>", on_resize)

for i in range(7):
    app.rowconfigure(i, weight=1)
app.columnconfigure(1, weight=1)

app.mainloop()