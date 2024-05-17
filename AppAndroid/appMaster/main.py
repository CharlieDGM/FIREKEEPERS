#==================================================================================================================
#codigo de una aplicación básica para conectarse y verificar de forma continua los contenidos de una tabla
#de un servidor remoto, el algoritmo principal fue echo con mysql-connector, todo lo demas solo son 
#declaración de objetos necesarias para la Interfaz Gráfica (que me gustaria que no fuera tan horrible de trabajar)
#en fin, este es un codigo de prueba para ver como reacciona el codigo en diferentes entornos :P
#==================================================================================================================

#importamos diferentes librearias para el correcto funcionamiento del codigo
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

import mysql.connector
from plyer import notification

#clase principal que almacena todos los contenidos de la interfaz gráfica
class AplicacionMYSQLDB(App):
    def __init__(self, **kwargs):
        super(AplicacionMYSQLDB, self).__init__(**kwargs)
        self.ultima_marca_tiempo = None

    def build(self):

        #layout principal de la applicación, donde todos los objetos seran puestos
        main_layout = BoxLayout(orientation='vertical', spacing=0)

        #definimos diferentes tamaños para el texto xd
        label_font_size = 25
        input_font_size = 25
        textoHeight = 25

        #Creamos todos los widgets y los insertamos en el layout
        main_layout.add_widget(Label(text='Host:', font_size=label_font_size)) # Host
        self.hostEntry = TextInput(multiline=False, font_size=input_font_size)
        main_layout.add_widget(self.hostEntry) 

        main_layout.add_widget(Label(text='Usuario:', font_size=label_font_size))  # Usuario
        self.userEntry = TextInput(multiline=False, font_size=input_font_size)
        main_layout.add_widget(self.userEntry)  

        main_layout.add_widget(Label(text='Contraseña:', font_size=label_font_size))  # Contraseña
        self.passwordEntry = TextInput(password=True, multiline=False, font_size=input_font_size)
        main_layout.add_widget(self.passwordEntry)  

        main_layout.add_widget(Label(text='Database:', font_size=label_font_size))  # Base de Datos
        self.databaseEntry = TextInput(multiline=False, font_size=input_font_size)
        main_layout.add_widget(self.databaseEntry)  

        main_layout.add_widget(Label(text='Tabla:', font_size=label_font_size))  # Tabla
        self.tablaEntry = TextInput(multiline=False, font_size=input_font_size)
        main_layout.add_widget(self.tablaEntry)  

        # Widget del boton que activa la funcion de...... CLICKBOTON genial, aveces me amo mucho
        main_layout.add_widget(Button(text='Ver Tabla', on_press=self.clickBoton, font_size=label_font_size))

        # Cuadro de texto donde se imprimira el resultado de la query
        self.cuadroTexto = TextInput(multiline=True, font_size=textoHeight, height=450, size_hint_y=None)
        main_layout.add_widget(self.cuadroTexto)

        return main_layout #devolvemos el layout

    def verTabla(self, host_, user_, password_, database_, tabla_):
        #funcion principal del codigo, lo mas facil
        try:
            conn = mysql.connector.connect( #intentamos conectarnos a la base de datos con las credenciales ingresadas
                host=host_,
                user=user_,
                password=password_,
                database=database_,
            )

            cursor = conn.cursor() #definimos el objeto "cursor" el cual realizara las consultas y ejecutara las querys
            self.cuadroTexto.text = '' #limpiamos el cuadro de texto donde imprimimos el resultado de las querys

            #===================================
            #amm estas tres lineas sirven para poner los nombres de las columnas como primer linea
            #===================================

            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tabla_}';") #ejecutamos una query con la credencial de la tabla
            column_names = [nomCol[0] for nomCol in cursor.fetchall()] #array que contendra todos los nombres de las columnas
            self.cuadroTexto.text += ', '.join(column_names) + "\n" #imprimimos en el texto (esta linea no la termino de comprender pero funciona, lol)

            cursor.execute(f"SELECT * FROM {tabla_}") #Query que los datos de la tabla
            rows = cursor.fetchall() #guardamos los datos en "rows"

            if self.haCambiadoDatos(rows):
                notification.notify(
                    title='Se ha registrado un incendio!',
                    message='Sigue las instrucciones de las autoridades de tu area',
                )

            for row in rows: #ahora ejecutamos un ciclo que imprimira todos los datos que se encuentren en la tabla
                self.cuadroTexto.text += str(row) + "\n"

        except mysql.connector.Error as err: 
            #Si ocurre un error lo imprimimos en el cuadro de texto, esta función para detectar error se encuentra en la libreria
            self.cuadroTexto.text += f"Error: {err}\n"

        finally: 
            #al terminar todas las funciones debemos de cerrar el cursor y la conección para su correcto funcionamiento
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def clickBoton(self, instance): #funcion que se ejecuta al pulsar el boton
        #función dentro de la función, la llamamos cada 7 segundos
        def actualizarDatos(dt):
            host_in = self.hostEntry.text #Obtenemos las credenciales desde loscuadros de texto
            user_in = self.userEntry.text
            password_in = self.passwordEntry.text
            database_in = self.databaseEntry.text
            tabla_in = self.tablaEntry.text
            
            #borramos los widgets para que la app se vea mas chulis xd
            for widget in self.root.children:
                if widget != self.cuadroTexto:
                    self.root.remove_widget(widget)

            #habilitamos para que el cuadro de texto ocupe el especio vacio
            self.cuadroTexto.size_hint_y = 1.0

            #yyyyy porfin ejecutamos la funcion mandando las credenciales a la funcion
            self.verTabla(host_in, user_in, password_in, database_in, tabla_in)

        #Intervalo entre llamada a la función    
        Clock.schedule_interval(actualizarDatos, 7)

    def haCambiadoDatos(self, rows):
        if not rows:
            return False #NO hay datos tons es falso
        
        ultima_marca_tiempo_tabla = rows[-1][-1] #la marca temporal se encuentra al final

        if self.ultima_marca_tiempo is None:
            #es la primera vez que se verifica, actualizamos el valor de la marca temporal
            self.ultima_marca_tiempo = ultima_marca_tiempo_tabla 
            return False # No hay cambios por ser la primera verificación (creo xd?)
        

        if ultima_marca_tiempo_tabla > self.ultima_marca_tiempo:
            #si son datos diferentes entonces si hay cambio 
            self.ultima_marca_tiempo = ultima_marca_tiempo_tabla
            return True #devolvemos verdadero
        
        return False
            
        

#el equivalente al while True en esta interfaz gráfica, iniciamos el loop que contiene toda la aplicación
if __name__ == '__main__':
    app = AplicacionMYSQLDB()
    app.run()
# demodemodemodemoknight
