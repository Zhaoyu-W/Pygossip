import multiprocessing
import random
import socket
import time
from util.constants import GOSSIP_INTERVAL

from util.gossip_msg import do_gossip


class GossipSender(multiprocessing.Process):
    def __init__(
        self,
        ip_address,
        tcp_port,
        connection_pool,
    ):
        multiprocessing.Process.__init__(self)
        self.ip_address = ip_address
        self.tcp_port = tcp_port
        self.identifier = "{}:{}".format(self.ip_address, self.tcp_port)
        self.connection_pool = connection_pool

    def run(self):
        """Once run the sender, the subprocess will periodically select
        a random live member from the connection map, and try to set up a
        connection to the selected node to attempt a gossip
        """
        last_time = time.time()*1000
        print("Started (%s) sender..." % self.identifier)

        while True:
            cur_time = time.time()*1000
            if cur_time - last_time >= GOSSIP_INTERVAL*1000:
                live_members = self.connection_pool.get_live_members()
                live_members.remove(self.identifier)

                if not live_members:
                    print("[SENDER]: Cannot find live members to gossip...")
                else:
                    client_identifier = live_members[random.randint(0, len(live_members)-1)]
                    do_gossip(client_identifier, self.identifier, self.connection_pool)

                # update to currrent time
                last_time = cur_time
