import socket

esp32IP = '192.168.1.17'
esp32Port = 80

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((esp32IP, esp32Port))

try:
    while True:
        message = "THEEEEEEEE\n"
        clientSocket.send(message.encode('utf-8'))

        response = clientSocket.recv(1024).decode('utf-8')
        print("Respuesta del ESP32: " + response)

finally:
    clientSocket.close()
