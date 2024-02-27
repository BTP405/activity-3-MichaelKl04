import socket
import pickle
import os

host = '127.0.0.1'
port = 8080
SAVE_DIR = 'received_files'  # Directory to save received files

def save_file(file_name, file_data):
    with open(os.path.join(SAVE_DIR, file_name), 'wb') as file:
        file.write(file_data)

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()

        with conn:
            print(f"Connected by {addr}")
            data = b""
            while True:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet
            
            try:
                file_name, file_data = pickle.loads(data)
                save_file(file_name, file_data)
                print(f"File {file_name} received and saved.")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
