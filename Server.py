import socket
import threading

host=socket.gethostbyname(socket.gethostname())
port=(5050)
ADDR=(host, port)

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

def handle(client):
    while True:
        try:
            message=client.recv(2048).decode('utf-8')
            if message=="quit":
                client.close()
        except:
            client.close()


def receive():
    while True:
        client, address=server.accept()
        thread=threading.Thread(target=handle, args=(client,))
        thread.start()


receive()