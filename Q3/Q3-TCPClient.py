import socket
import threading
import pickle

host = '127.0.0.1'
port = 8080

def receive_message(sock):
    while True:
        try:
            message = sock.recv(4096)
            if message:
                print(pickle.loads(message))  
            else:
                print("Disconnected from server.")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def send_message(sock):
    while True:
        msg = input("")
        if msg.lower() == "exit":
            print("Disconnected from server.")
            break
        try:
            sock.sendall(pickle.dumps(msg))  
        except Exception as e:
            print(f"Failed to send message: {e}")
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        
        print("Connected to the chat server.")
        name = input("Enter your name: ")
        try:
            client_socket.sendall(pickle.dumps(name))  
        except Exception as e:
            print(f"Failed to send name: {e}")
            return

        thread_recv = threading.Thread(target=receive_message, args=(client_socket,))
        thread_recv.start()

        send_message(client_socket)

if __name__ == "__main__":
    main()
