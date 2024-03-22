import serial

if __name__ == '__main__':
    serial = serial.Serial(
        port='/dev/ttyS0', #ttyS0 son los pines RX y TX, el puerto de conexión puede variar
        baudrate=9600, #no cambiar, esta sincronizado con el arduino
        timeout=2
    ) #datos de conección UART
    serial.flush()
    #se limpia todo mensaje que exista en ese momento
    try:
        while True:
            if serial.in_waiting > 0:
                #serial.reset_input_buffer()
                #supuestamente es para limpiar el input pero esta linea genera mas problemas
                mensaje = serial.readline().decode('utf-8').rstrip()
                #por partes: se lee la linea recibida, se decodifica y se limpian los espacios en blanco
                print(mensaje)
                if mensaje == "HIGH":
                    serial.write("encender\n".encode('utf-8'))
                    #por partes: se escribe el mensaje con la terminacion \n, se codifica para facilitar la interpretación en el arduino
                    print("Enviado: encender")
                else:
                    serial.write("apagar\n".encode('utf-8'))
                    #lo mismo
                    print("Enviado: apagar")
                    
    finally:
        serial.close()
        #al terminar, o en caso de excepciones, se cierra la coneccion serial