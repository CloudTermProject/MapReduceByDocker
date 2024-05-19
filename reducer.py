# Reducer.py
import socket
import json
from collections import defaultdict

MASTER_HOST = 'localhost'
REDUCER_PORT = 9001
REDUCER_ID = 1  # Change this for each reducer instance

def word_count_reducer(data):
    """ Simple word count reducer function """
    combined_count = defaultdict(int)
    for key, value in data:
        combined_count[key] += value
    return list(combined_count.items())

def reducer_service():
    """ Reducer service for processing map results """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((MASTER_HOST, REDUCER_PORT + REDUCER_ID))
        server.listen()
        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024)
            mapped_data = json.loads(data.decode())
            print(f"Received map results from {addr}: {mapped_data}")
            
            # Ensure the data is in pairs
            if isinstance(mapped_data, list) and all(isinstance(item, list) and len(item) == 2 for item in mapped_data):
                reduced_data = word_count_reducer(mapped_data)
                conn.sendall(json.dumps(reduced_data).encode())
            else:
                print("Invalid data format received")

if __name__ == "__main__":
    reducer_service()
