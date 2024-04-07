import socket
import threading
from pymongo import MongoClient

# MongoDB setup to store recieved messgaes
client = MongoClient('localhost', 27017)
db = client['p2p']
message_collection = db.messages

# Peers list
peers = [
    ('localhost', 65432), #default
    ('192.168.1.5', 65432),
]

def send_message(to_host, to_port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((to_host, to_port))
            s.sendall(message.encode('utf-8'))
            if message == "GET_MESSAGES":
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                    print("Received: ", data.decode('utf-8'))
        except ConnectionRefusedError:
            print(f"Connection to {to_host}:{to_port} failed.")

def handle_incoming_messages(conn, addr):
    print(f"Connection from {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        print(f"Receieved messafe: {message}")
    conn.close()
    
def start_peer_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Listening for incoming messages on {host}:{port}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_incoming_messages, args=(conn, addr))
            thread.start()
            
if __name__ == "__main__":
    server_thread = threading.Thread(target=start_peer_server, args=('localhost', 65433))
    server_thread.start()
    
    for host, port in peers:
        send_message(host, port, "Hello, my friend!")
    
    if peers: send_messages(peers[0][0], peers[0][1], "GET_MESSGAES")
                    