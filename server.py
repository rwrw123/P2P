import socket
import threading
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['p2p']
messages_collection = db.messages

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Received message: {message}")
            #stores message in MongoDB
            if message != "GET_MESSAGES":
                messages_collection.insert_one({"from": str(addr), "message": message})
            else:
                messages = messages_collection.find({})
                for msg in messages:
                    conn.sendall(f"{msg['from']}: {msg['message']}\n".encode('utf-8'))
        except ConnectionResetError:
            break
    conn.close()
    
def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            
if __name__ == "__main__":
    host = 'localhost'
    port = 65432
    start_server(host,port)