import multiprocessing
import socket
import time


class GossipServer(multiprocessing.Process):
    def __init__(
        self,
        ip_address,
        tcp_port,
        connection_pool,
        adversarial_controller,
        initial_state,
    ):
        multiprocessing.Process.__init__(self)
        self.ip_address = ip_address
        self.tcp_port = tcp_port
        self.identifier = "{}:{}".format(ip_address, tcp_port)
        self.connection_pool = connection_pool
        self.adversarial_controller = adversarial_controller
        self.state = initial_state
        self._server_lock = multiprocessing.Lock()

    def run(self):
        """Once run the server, the subprocess will listen to the client
        socket, and response a csv-formatted entry table containing the
        live members from its view
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip_address, self.tcp_port))
        server_socket.listen(5)
        self.connection_pool.update_connection(
            self.identifier, self.state, int(time.time()))
        print("Started (%s) server..." % self.identifier)

        while True:
            try:
                self._server_lock.acquire()
                client_socket, client_address = server_socket.accept()
                client_ip, client_port = client_address
                client_identfier = "{}:{}".format(client_ip, client_port)
                self.adversarial_controller.response(client_socket, client_identfier)
                self._server_lock.release()
            except Exception as e:
                print(
                    "[SERVER]: Failed to response to (%s) server due to %s..." % (client_socket, e))
