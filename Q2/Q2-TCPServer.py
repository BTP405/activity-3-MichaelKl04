import socket
import pickle
import marshal
import types

host = '127.0.0.1'
port = 8080

#Most of the documentation in this file is for my own personal use, to come back and understand what I did in order    
#to implement it in future code later down the line

def execute_task(task_data):
    try:
        #unpickle the function
        function_marshaled = pickle.loads(task_data)[0]
        #unpickle the arguments [1] and [2] are the arguments and keyword arguments
        args = pickle.loads(task_data)[1]
        kwargs = pickle.loads(task_data)[2]

        #deserialize the code object
        code = marshal.loads(function_marshaled)

        # Create a function object from the de-serialized code object
        function = types.FunctionType(code, globals(), "function")

        result = function(*args, **kwargs)

        return result
    
    except Exception as e:
        return f"Error executing task: {e}"

def main():
    #create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #bind the socket to the host and port
        s.bind((host, port))
        s.listen()
        print(f"Worker listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(4096)
                if not data:
                    break
                result = execute_task(data)
                conn.sendall(pickle.dumps(result))

if __name__ == "__main__":
    main()
