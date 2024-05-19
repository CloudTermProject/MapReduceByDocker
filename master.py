# Master.py
import socket
import threading
import json

MASTER_HOST = 'localhost'
MAPPER_PORT = 9000
REDUCER_PORT = 9001
NUM_MAPPERS = 2
NUM_REDUCERS = 1

class Master:
    def __init__(self):
        self.mapper_results = []
        self.final_results = []

    def mapper_listener(self):
        """Listen for map results and collect them"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((MASTER_HOST, MAPPER_PORT))
            server.listen()
            for _ in range(NUM_MAPPERS):
                conn, addr = server.accept()
                with conn:
                    data = conn.recv(1024)
                    results = json.loads(data.decode())
                    print(f"Received map results from {addr}: {results}")
                    self.mapper_results.extend(results)

    def reducer_listener(self):
        """Listen for final reduce results"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((MASTER_HOST, REDUCER_PORT))
            server.listen()
            for _ in range(NUM_REDUCERS):
                conn, addr = server.accept()
                with conn:
                    data = conn.recv(1024)
                    results = json.loads(data.decode())
                    print(f"Received reduce results from {addr}: {results}")
                    self.final_results.extend(results)

    def distribute_tasks_to_mappers(self, data_chunks):
        """Distribute data chunks to mappers"""
        for i, chunk in enumerate(data_chunks):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((MASTER_HOST, MAPPER_PORT + i + 1))
                client.sendall(json.dumps(chunk).encode())

    def distribute_tasks_to_reducers(self):
        """Distribute map results to reducers"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((MASTER_HOST, REDUCER_PORT + 1))
            client.sendall(json.dumps(self.mapper_results).encode())

    def run(self, data):
        """Run the entire MapReduce process"""
        # Split data into chunks for mappers
        data_chunks = [data[i::NUM_MAPPERS] for i in range(NUM_MAPPERS)]

        # Start listening threads
        mapper_thread = threading.Thread(target=self.mapper_listener)
        reducer_thread = threading.Thread(target=self.reducer_listener)
        mapper_thread.start()
        reducer_thread.start()

        # Distribute tasks to mappers
        self.distribute_tasks_to_mappers(data_chunks)

        # Wait for mapper results
        mapper_thread.join()

        # Distribute tasks to reducers
        self.distribute_tasks_to_reducers()

        # Wait for reducer results
        reducer_thread.join()

        print(f"Final results: {self.final_results}")

if __name__ == "__main__":
    # Example input data
    data = [
        "apple banana apple",
        "banana orange apple",
        "apple orange banana",
        "grape banana apple"
    ]

    master = Master()
    master.run(data)
