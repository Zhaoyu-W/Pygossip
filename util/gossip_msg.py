import socket

from util.constants import GOSSIP_THRESHOLD

def do_gossip(client_socket, client_identifier, server_identifier, connection_pool,):
    data = client_socket.recv(1024)
    if not data:
        print("[GOSSIPER]: %s is adversarial gossiping..." % client_identifier)
    else:
        # remove leading and tailing whitespace
        data = data.decode().strip()
        if data:
            entries = data.split("\n")
            gossip_time = 0
            for entry in entries:
                if gossip_time == GOSSIP_THRESHOLD:
                    print("[GOSSIPER]: Run out of %d times to gossip..." % GOSSIP_THRESHOLD)
                    break
                try:
                    identifier, timestamp, state = entry.split(",")
                    if identifier == server_identifier:
                        continue
                    else:
                        gossip_address, _ = identifier.split(":")
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
                            print("[GOSSIPER]: Gossiped to %s successfully!" % identifier)
                        else:
                            print("[GOSSIPER]: Connection did not recogonize %s..." % identifier)

                except Exception as e:
                    print("[GOSSIPER]: %s is adversarial gossiping due to %s..." % (client_identifier, e))

                gossip_time += 1
        else:
            print("[Gossiper]: %s is adversarial gossiping..." % client_identifier)
