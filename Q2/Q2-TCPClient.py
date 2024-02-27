import socket
import pickle
import marshal

host = '127.0.0.1'
port = 8080

def add_numbers(x, y):
    z = 0
    for i in range (20000):
        z += x ** i
    return x + y

def send_task(task_func, *args, **kwargs):
    try: 
        #marshal the function (serialize the object into a byte stream)
        marshaled_func = marshal.dumps(task_func.__code__)
        #pickle the task data
        task_data = pickle.dumps((marshaled_func, args, kwargs))
    except Exception as e:
        return f"Error pickling task: {e}"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(task_data)
            result_data = s.recv(4096)
            result = pickle.loads(result_data)
            return result
    except Exception as e:
        return f"Error communicating with server: {e}"

if __name__ == "__main__":
    result = send_task(add_numbers, 5, 3)
    print("Result:", result)
