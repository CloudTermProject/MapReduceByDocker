import socket
import pickle
import logging

class ReducerTask:
    def __init__(self, server_ip, server_port, reduce_task, output_dict):
        self.data = None
        self.inverted_index_output = None
        self.word_count_output = None
        self.map_task = reduce_task
        self.output_dict = output_dict
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_data(self):
        try:
            message_info = self.client_socket.recv(16)

            message_header = self.client_socket.recv(22)
            header = comm_pb2.Header()
            header.ParseFromString(message_header)
            data_len = (header.header.split(":")[0])
            reducer_data = b''
            while len(reducer_data) < int(data_len):
                to_read = int(data_len) - len(reducer_data)
                data = self.client_socket.recv(
                    4096 if to_read > 4096 else to_read
                )
                reducer_data += data
            self.data = pickle.loads(reducer_data)
        except Exception as e:
            logging.error("Reducer received Exception", str(e))
            raise e
