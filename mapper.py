# Mapper.py
import socket
import json
from collections import defaultdict

MASTER_HOST = 'localhost'
MAPPER_PORT = 9000
MAPPER_ID = 1  # Change this for each mapper instance

def word_count_mapper(data):
    """ Simple word count mapper function """
    word_count = defaultdict(int)
    for line in data:
        for word in line.strip().split():
            word_count[word] += 1
    return list(word_count.items())

def mapper_service():
    """ Mapper service for processing data """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((MASTER_HOST, MAPPER_PORT + MAPPER_ID))
        server.listen()
        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024)
            input_data = json.loads(data.decode())
            print(f"Received data from {addr}: {input_data}")
            
            # Ensure the data is in the expected format (list of strings)
            if isinstance(input_data, list) and all(isinstance(item, str) for item in input_data):
                mapped_data = word_count_mapper(input_data)
                conn.sendall(json.dumps(mapped_data).encode())
            else:
                print("Invalid data format received")

if __name__ == "__main__":
    mapper_service()
