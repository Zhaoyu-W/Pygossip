import argparse
from communication.connection import ConnectionPool
from communication.server import GossipServer
from communication.sender import GossipSender
from controller.server_controller import ServerController
from controller.adversarial_controller import AdversarialController


def main(ip_address, tcp_port, initial_state):
    connection_pool = ConnectionPool(
        "GossipPool", cache_limit=3, identifier="{}:{}".format(ip_address, tcp_port))
    adversarial_controller = AdversarialController(connection_pool)

    server = GossipServer(
        ip_address, tcp_port, connection_pool, adversarial_controller, initial_state)
    sender = GossipSender(ip_address, tcp_port, connection_pool)
    server_controller = ServerController(
        ip_address, tcp_port, connection_pool, adversarial_controller)

    server.start()
    sender.start()
    server_controller.run()

    server.join()
    sender.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_address", help="IP address to bind")
    parser.add_argument("tcp_port", type=int, help="tcp port to listen")
    parser.add_argument(
        "initial_state", type=int, help="initial node state")
    args = parser.parse_args()

    main(args.ip_address, args.tcp_port, args.initial_state)
