import socket
import threading
import pickle

host = '127.0.0.1'
port = 8080


client_list = []
lock = threading.Lock()

#broadcasts the message to all clients except the origin
def broadcast_message(message, origin):
    with lock:
        for client in client_list:
            if client != origin:
                try:
                    client.sendall(message)
                except:
                    client_list.remove(client)

#thread for each client
def client_thread(conn, addr):
    try:
        name = pickle.loads(conn.recv(1024))  
    except Exception as e:
        print(f"Error receiving name from {addr}: {e}")
        return

    welcome_msg = f"{name} has joined the chat!"
    broadcast_message(pickle.dumps(welcome_msg), conn)

    while True:
        try:
            message = pickle.loads(conn.recv(4096))
            if message:
                formatted_message = f"{name}: {message}"  
                broadcast_message(pickle.dumps(formatted_message), conn)  
            else:
                remove(conn)
                break
        except Exception as e:
            print(f"Error: {e}")
            remove(conn)
            break

#removes a client from the list
def remove(connection):
    if connection in client_list:
        with lock:
            client_list.remove(connection)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print("Server started. Listening for connections...")

        while True:
            conn, addr = server_socket.accept()
            with lock:
                client_list.append(conn)
            
            print(f"Connection established with {addr}")
            t = threading.Thread(target=client_thread, args=(conn, addr))
            t.start()

if __name__ == "__main__":
    main()
