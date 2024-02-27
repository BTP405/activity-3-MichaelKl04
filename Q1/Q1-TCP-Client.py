import socket
import pickle
import os

host = '127.0.0.1'
port = 8080

def send_file(file_path):
    """Send the file to the server."""
    try:
        with open(file_path, 'rb') as file:
            file_name = os.path.basename(file_path)
            file_data = file.read()
            data = pickle.dumps((file_name, file_data))
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(data)
            print(f"File {file_name} sent to server.")
    except Exception as e:
        print(f"Error sending file: {e}")

def main():
    file_path = input("Enter the path of the file to transfer: ")
    send_file(file_path)

if __name__ == "__main__":
    main()

#Implement a client-server file transfer application where the client sends a file to the server using sockets. 
#Before transmitting the file, pickle the file object on the client side. On the server side, receive the pickled file object, unpickle it, and save it to disk.


#Requirements:
#The client should provide the file path of the file to be transferred.
#The server should specify the directory where the received file will be saved.
            
#Ensure error handling for file I/O operations, socket connections, and pickling/unpickling.





