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
        1. !: list all the connections in csv format
        2. ?: list all the connections in identifier --> state format
        3. +identifier: connect to new client
        4. digit[0-9]: change the server state
        """
        print("Start (%s) controller..." % (self.identifier))
        for command in sys.stdin:
            command = command.strip()
            # skip empty command 
            if not command:
                print("[CONTROLLER]: Invalid empty input...")
                continue

            if command == '!':
                entries = self.connection_pool.get_all_entries()
                for entry in entries:
                    print(entry)
            elif command == '?':
                entries = self.connection_pool.get_all_entries()
                for entry in entries:
                    identifier, _, state = entry.split(",")
                    print("{} --> {}".format(identifier, state))
            elif command == 'Y' or command == 'N':
                self.adversarial_controller.toggle_adversarial(command)
            elif command.isdigit():
                self.update_server_state(int(command))
            elif command[0] == '+':
                try:
                    client_address, _ = command[1:].split(":")
                    socket.inet_aton(client_address)
                except Exception:
                    print("[CONTROLLER]: Input %s is invalid..." % command)
                    continue

                do_gossip(
                    command[1:], self.identifier, self.connection_pool, support_blacklist=True)
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
            print("{} --> {}".format(self.identifier, state))
        else:
            print("[CONTROLLER]: Invalid state input %s, state should be between 0 and 9..." % state)
