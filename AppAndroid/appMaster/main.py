#==================================================================================================================
#codigo de una aplicación básica para conectarse y verificar de forma continua los contenidos de una tabla
#de un servidor remoto, el algoritmo principal fue echo con mysql-connector, todo lo demas solo son 
#declaración de objetos necesarias para la Interfaz Gráfica (que me gustaria que no fuera tan horrible de trabajar)
#en fin, este es un codigo básico que servira para el proposito simple que tenemos que cumplir :p
#==================================================================================================================

#importamos diferentes librearias para el correcto funcionamiento del codigo
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.audio import SoundLoader

import mysql.connector
from plyer import notification
from plyer import vibrator

#clase principal que almacena todos los contenidos de la interfaz gráfica
class AplicacionMYSQLDB(App):
    def __init__(self, **kwargs):
        super(AplicacionMYSQLDB, self).__init__(**kwargs)
        self.ultimaMarcaTiempo = None
        self.notificacionActivada = False

    def build(self):

        #layout principal de la applicación, donde todos los objetos seran puestos
        self.mainLayout = BoxLayout(orientation='vertical', spacing=0)

        #definimos diferentes tamaños para el texto xd
        labelFontSize = 25
        inputFontSize = 25
        textoHeight = 25

        #Creamos todos los widgets y los insertamos en el layout
        self.hostEntry = TextInput(hint_text='Host',multiline=False, font_size=inputFontSize)
        self.mainLayout.add_widget(self.hostEntry) 

        self.userEntry = TextInput(hint_text='User',multiline=False, font_size=inputFontSize)
        self.mainLayout.add_widget(self.userEntry)  

        self.passwordEntry = TextInput(hint_text='Password',password=True, multiline=False, font_size=inputFontSize)
        self.mainLayout.add_widget(self.passwordEntry)  

        self.databaseEntry = TextInput(hint_text='DataBase',multiline=False, font_size=inputFontSize)
        self.mainLayout.add_widget(self.databaseEntry)  

        self.tablaEntry = TextInput(hint_text='Table',multiline=False, font_size=inputFontSize)
        self.mainLayout.add_widget(self.tablaEntry)  

        # Widget del boton que activa la funcion de...... CLICKBOTON genial, aveces me amo mucho
        self.verTablaButton = Button(text='Start', on_press=self.clickBoton, font_size=labelFontSize,background_normal='', background_color=[0.204, 0.745, 0.318, 1], color=[0.22, 0.246, 0.289, 1])
        self.mainLayout.add_widget(self.verTablaButton)

        # Cuadro de texto donde se imprimira el resultado de la query
        self.cuadroTexto = TextInput(multiline=True, font_size=textoHeight, height=450, size_hint_y=None)
        self.mainLayout.add_widget(self.cuadroTexto)

        #Boton que reinicia el sistema de notificación.
        self.resetButton = Button(text='Reset', on_press=self.resetNotificacion, font_size=labelFontSize,background_normal='', background_color=[0.212, 0.976, 0.937, 1], color=[0.22, 0.246, 0.289, 1])
        self.mainLayout.add_widget(self.resetButton)        

        return self.mainLayout #devolvemos el layout

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
            columnNames = [nomCol[0] for nomCol in cursor.fetchall()] #array que contendra todos los nombres de las columnas
            self.cuadroTexto.text += ', '.join(columnNames) + "\n" #imprimimos en el texto (esta linea no la termino de comprender pero funciona, lol)

            cursor.execute(f"SELECT * FROM {tabla_}") #Query que lee los datos de la tabla
            rows = cursor.fetchall() #guardamos los datos en "rows"

            if self.haCambiadoDatos(rows):
                if self.notificacionActivada != True:
                    lugarIncendio = rows[-1][-2]
                    textoLimpio = ''.join(c for c in lugarIncendio if c not in "/n")

                    notification.notify(
                        title='Fire Detected!',
                        message=f'Ubication of fire: {textoLimpio}',
                        app_name='FIRE ALARM',
                        app_icon='logo.jpg',
                    )
                    sonido = SoundLoader.load('alarma.wav')
                    sonido.play()
                    vibrator.vibrate(time=5)
                    self.notificacionActivada = True

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
        self.root.remove_widget(self.hostEntry)
        self.root.remove_widget(self.userEntry)
        self.root.remove_widget(self.passwordEntry)
        self.root.remove_widget(self.databaseEntry)
        self.root.remove_widget(self.tablaEntry)
        self.root.remove_widget(self.verTablaButton)

        def actualizarDatos(dt):
            host_in = self.hostEntry.text #Obtenemos las credenciales desde loscuadros de texto
            user_in = self.userEntry.text
            password_in = self.passwordEntry.text
            database_in = self.databaseEntry.text
            tabla_in = self.tablaEntry.text

            #habilitamos para que el cuadro de texto y el boton de reseteo para que ocupe el especio vacio
            self.cuadroTexto.size_hint_y = 1.0
            self.resetButton.size_hint_y = 1.0

            #yyyyy porfin ejecutamos la funcion mandando las credenciales a la funcion
            self.verTabla(host_in, user_in, password_in, database_in, tabla_in)

        #Intervalo entre llamada a la función    
        Clock.schedule_interval(actualizarDatos, 7)

    def haCambiadoDatos(self, rows):
        if not rows:
            return False #NO hay datos tons es falso
        
        ultimaMarcaTiempoTabla = rows[-1][-1] #la marca temporal se encuentra al final

        if self.ultimaMarcaTiempo is None:
            #es la primera vez que se verifica, actualizamos el valor de la marca temporal
            self.ultimaMarcaTiempo = ultimaMarcaTiempoTabla 
            return False # No hay cambios por ser la primera verificación (creo xd?)
        

        if ultimaMarcaTiempoTabla > self.ultimaMarcaTiempo:
            #si son datos diferentes entonces si hay cambio 
            self.ultimaMarcaTiempo = ultimaMarcaTiempoTabla
            return True #devolvemos verdadero
        
        return False
    
    def resetNotificacion(self, instance):
        try:
            self.notificacionActivada = False
        except Exception as e: #reseteamos la variable que condiciona si sale o no la notificación
            print(f"error al reiniciar la notificacion: {str(e)}")
            
#el equivalente al while True en esta interfaz gráfica, iniciamos el loop que contiene toda la aplicación
if __name__ == '__main__':
    app = AplicacionMYSQLDB()
    app.run()
# demodemodemodemoknight
