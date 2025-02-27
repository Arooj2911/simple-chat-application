
import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 55555

# Initialize the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Function to send a message to all connected clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            remove_client(client)

# Function to handle communication with a specific client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            remove_client(client)
            break

# Function to remove a disconnected client
def remove_client(client):
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        broadcast(f"{nickname} has left the chat.".encode('utf-8'))
        clients.pop(index)
        nicknames.pop(index)
        client.close()

# Function to accept incoming connections
def receive():
    while True:
        client, address = server.accept()
        print(f"New connection: {address}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname assigned: {nickname}")
        broadcast(f"{nickname} has joined the chat.".encode('utf-8'))
        client.send("You are connected to the server!".encode('utf-8'))

        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

print("Server is running and listening for connections...")
receive()
