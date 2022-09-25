import ipaddress
import socket

from util.constants import BUFF_SIZE
from util.constants import GOSSIP_THRESHOLD

def do_gossip(
    client_identifier,
    server_identifier,
    connection_pool,
    support_blacklist=False,
):
    """Gossip to the client node and read its buffer table.
    If server node knows the table nodes, update its
    live member mapping. If not, continuously gossip to the
    new node
    Args:
        client_identifier (String): client identifier
        server_identifier (String): server identifier
        connection_pool (ConnectionPool): server connection pool
        support_blacklist (bool): update blacklist connection failed.
                                  Defaults to False.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)
        client_ip_address, client_port = client_identifier.split(":")
        client_socket.connect((client_ip_address, int(client_port)))
        data = yield_lines(client_socket).decode().strip().split("\n")
        client_socket.close()
    except Exception as e:
        if support_blacklist:
            connection_pool.block_connection(client_identifier)
            print("[CONTROLLER]: Connect to %s failed due to %s..." % (client_identifier, e))
        else:
            print("[GOSSIPER]: Gossip to %s failed due to %s..." % (client_identifier, e))
        return

    propagate_nodes = []
    gossip_time = 0

    for entry in data:
        if gossip_time == GOSSIP_THRESHOLD:
            print("[GOSSIPER]: Run out of %d times to gossip..." % GOSSIP_THRESHOLD)
            break
        # remove leading and tailing whitespace
        try:
            identifier, timestamp, state = entry.split(",")
            gossip_address, _ = identifier.split(":")
            if identifier == server_identifier:
            # or ipaddress.ip_address(gossip_address).is_private
                continue
            else:
                # check ip address
                socket.inet_aton(gossip_address)
                # check state
                state = int(state)
                if state < 0 or state > 10:
                    print("[GOSSIPER]: Identifier %s has invalid state %d..." % (identifier, state))
                    continue

                if identifier == client_identifier or \
                    connection_pool.check_existence(identifier):
                    connection_pool.update_connection(
                        identifier, int(state), int(timestamp))
                else:
                    print("[GOSSIPER]: %s is a new node, propagate it then..." % identifier)
                    propagate_nodes.append(identifier)
        except Exception as e:
            print("[GOSSIPER]: %s is adversarial gossiping due to %s..." % (client_identifier, e))

        gossip_time += 1
    print("[GOSSIPER]: Finished gossiping to %s..." % client_identifier)

    for node in propagate_nodes:
        do_gossip(node, server_identifier, connection_pool)

def yield_lines(client_socket):
    """Yield buffer lines

    Args:
        client_socket (Socket): client socket

    Returns:
        byte: buffer lines
    """
    data = b''
    while True:
        line = client_socket.recv(BUFF_SIZE)
        data += line
        if len(line) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data
