import socket
import threading

# Prompt user for a nickname
nickname = input("Enter your nickname: ")

# Establish connection to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Function to receive messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            print(f"Connection error: {e}")
            client.close()
            break

# Function to send messages to the server
def send():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode('utf-8'))

# Start threads for receiving and sending messages
threading.Thread(target=receive, daemon=True).start()
threading.Thread(target=send, daemon=True).start()
