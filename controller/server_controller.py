import sys
import socket
import time

from util.gossip_msg import do_gossip


class ServerController:
    def __init__(
        self,
        ip_address,
        tcp_port,
        connection_pool,
        adversarial_controller,
    ):
        self.ip_address = ip_address
        self.tcp_port = tcp_port
        self.identifier = "{}:{}".format(self.ip_address, self.tcp_port)
        self.connection_pool = connection_pool
        self.adversarial_controller = adversarial_controller

    def run(self):
        """Once run the controller, the main process will simultaneously read
        input commands and make decision based on the following 3 senarios:
        1. ?: list all the live connections in csv format
        2. +identifier: connect to new client
        3. digit[0-9]: change the server state
        """
        print("Start (%s) controller..." % (self.identifier))
        for command in sys.stdin:
            command = command.strip()
            # skip empty command 
            if not command:
                print("[CONTROLLER]: Invalid empty input...")
                continue

            if command == '?':
                connections = self.connection_pool.get_all_entries()
                for connection in connections:
                    print(connection)
            elif command == 'Y' or command == 'N':
                self.adversarial_controller.toggle_adversarial(command)
            elif command.isdigit():
                self.update_server_state(int(command))
            elif command[0] == '+':
                ip_address, tcp_port = command[1:].split(":")
                self.establish_new_connection(ip_address, int(tcp_port))
            else:
                print("[CONTROLLER]: Input %s is invalid..." % command)

    def update_server_state(self, state):
        """Update server state

        Args:
            state (int): state to udpate
        """
        if state > 0 and state <= 9:
            self.connection_pool.update_connection(self.identifier, state, int(time.time()))
            print("[CONTROLLER]: Updated %s state to %s" % (self.identifier, state))
        else:
            print("[CONTROLLER]: Invalid state input %s, state should be between 0 and 9..." % state)

    def establish_new_connection(self, ip_address, tcp_port):
        """Connect to new client and update the client information
        in connection pool

        Args:
            ip_address (String): clietn ip address
            tcp_port (int): client port
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)
        client_identifier = "{}:{}".format(ip_address, tcp_port)

        try:
            client_socket.connect((ip_address, int(tcp_port)))
            do_gossip(
                client_socket, client_identifier, self.identifier, self.connection_pool)
            client_socket.close()
        except Exception as e:
            self.connection_pool.block_connection(client_identifier)
            print("[CONTROLLER]: Connect to %s failed due to %s..." % (client_identifier, e))
