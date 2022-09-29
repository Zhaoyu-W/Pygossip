from multiprocessing import Lock
from multiprocessing import Manager
import time

from util.constants import SERVER_STATE, TIMESTAMP


class ConnectionPool:
    def __init__(self, connection_pool_type, cache_limit=3, identifier=None, adversarial=False):
        self.connection_pool_type = connection_pool_type
        self._connections = Manager().dict()
        self._black_list = Manager().list()
        self._pool_lock = Lock()
        self.cache_limit = cache_limit
        self.identifier = identifier

    def toggle_adversarial(self, command):
        if command == 'Y':
            self.adversarial = True
            print("[ADVERSARIAL]: Turn on adversarial gossip...")
        else:
            self.adversarial = False
            print("[ADVERSARIAL]: Turn off adversarial gossip...")

    def update_connection(self, identifier, state, update_time):
        """Add the identifier with its connection to connection pool

        Args:
            identifier (String): unique identifier
            state (int): update state
            update_time (int): update time
        """
        if update_time > time.time():
            print("[CONNECTIONPOOL]: Ignore future update on %s..." % identifier)
            return

        self._pool_lock.acquire()
        # update connection state
        if identifier in self._connections:
            # check old update
            if update_time < self._connections[identifier][TIMESTAMP]:
                print("[CONNECTIONPOOL]: Ignore older update on %s...(pool: %s)"
                      % (identifier, self))
                self._pool_lock.release()
                return

            self._connections[identifier] = {
                SERVER_STATE: state,
                TIMESTAMP: update_time,
            }
            self._pool_lock.release()
            print("[CONNECTIONPOOL]: Updated connection %s (pool: %s)"
                  % (identifier, self))
        # discard blocked connection
        elif identifier in self._black_list:
            self._pool_lock.release()
            print("[CONNECTIONPOOL]: Connection %s blocked already (pool: %s)"
                  % (identifier, self))
        # add new connection
        else:
            self._connections[identifier] = {
                SERVER_STATE: state,
                TIMESTAMP: update_time,
            }
            print("[CONNECTIONPOOL]: Added new connection %s (pool: %s)"
                  % (identifier, self))
            self._pool_lock.release()

    def _maintain_connections(self):
        """Maintain connections to meet the cache limit
        """
        if len(self._connections) > self.cache_limit+1:
            self._pool_lock.acquire()
            connections = self._connections.keys()
            connections.remove(self.identifier)
            connections.sort(
                key=lambda x: self._connections[x][TIMESTAMP], reverse=True)
            connections_to_remove = connections[self.cache_limit:]
            self._pool_lock.release()

            for connection in connections_to_remove:
                self.remove_connection(connection)
                print("[CONNECTIONPOOL]: Connection maintainer kills: %s (pool: %s)"
                      % (connection, self))

    def remove_connection(self, identifier):
        """Remove existing identifier from connection pool

        Args:
            identifier (String): unique identifier to find 
            the connection
        """
        self._pool_lock.acquire()
        removed_connection = self._connections.pop(identifier, None)
        self._pool_lock.release()

        if removed_connection:
            print("[CONNECTIONPOOL]: Removed connection %s (pool: %s)"
                  % (identifier, self))

    def get_all_entries(self):
        """List all live connections in csv format

        Returns:
            list: List of "identifier,timestamp,state"
        """
        entries = []
        self._pool_lock.acquire()
        for identifier in self._connections.keys():
            connection = self._connections.get(identifier)
            timestamp = connection[TIMESTAMP]
            state = connection[SERVER_STATE]
            entries.append(
                "{},{},{}".format(identifier, timestamp, state))
        self._pool_lock.release()

        return entries

    def get_live_members(self):
        """Get the live member list

        Returns:
            list: list of indetifiers of live member
        """
        self._pool_lock.acquire()
        live_members = self._connections.keys()
        self._pool_lock.release()

        if live_members:
            return live_members
        else:
            print("[CONNECTIONPOOL]: Cannot find live members...")

    def check_existence(self, idetifier):
        """Check identifier existing in connection pool

        Args:
            identifier (String): unique identifier
        """
        self._pool_lock.acquire()
        existence = idetifier in self._connections
        self._pool_lock.release()
        return existence

    def block_connection(self, identifier):
        """Add connection to black list

        Args:
            identifier (String): unique identifier to find the connection
        """
        self._pool_lock.acquire()
        if identifier in self._black_list:
            print("[CONNECTIONPOOL]: %s already blocked (pool: %s)"
                  % (identifier, self))
        else:
            self._black_list.append(identifier)
            print("[CONNECTIONPOOL]: Blocked connection %s (pool: %s)"
                  % (identifier, self))
        self._pool_lock.release()

    # def get_connection(self, identifier):
    #     """Get the connection from pool by identifier

    #     Args:
    #         identifier (String): unique identifier to find the connection

    #     Returns:
    #         Socket: connection socket
    #     """

    #     self._pool_lock.acquire()
    #     connection = self._connections.get(identifier, None)
    #     self._pool_lock.release()

    #     if connection:
    #         return connection[ConnectionPool.CONNECTION]
    #     else:
    #         print("Cannot find identifier %s (pool: %s)" % (identifier, self))

    # def get_state(self, identifier):
    #     """Get the state from pool by identifier

    #     Args:
    #         identifier (String): unique identifier to find the connection

    #     Returns:
    #         int: state
    #     """
    #     self._pool_lock.acquire()
    #     connection = self._connections.get(identifier, None)
    #     self._pool_lock.release()

    #     if connection:
    #         return connection[ConnectionPool.SERVER_STATE]
    #     else:
    #         print("Cannot find identifier %s (pool: %s)" % (identifier, self))

    # def get_timestamp(self, identifier):
    #     """Get the timestamp from pool by identifier

    #     Args:
    #         identifier (String): unique identifier to find the connection

    #     Returns:
    #         int: timestamp
    #     """
    #     self._pool_lock.acquire()
    #     connection = self._connections.get(identifier, None)
    #     self._pool_lock.release()

    #     if connection:
    #         return connection[ConnectionPool.TIMESTAMP]
    #     else:
    #         print("Cannot find identifier %s (pool: %s)" % (identifier, self))

    # def update_state(self, identifier, state, update_time):
    #     """Update exisiting identifier with new state

    #     Args:
    #         identifier (String): unique identifier to find the conneciton
    #         state (int): state to update
    #     """
    #     self._pool_lock.acquire()
    #     if identifier in self._connections:
    #         self._connections[identifier] = {
    #             ConnectionPool.SERVER_STATE: state,
    #             ConnectionPool.TIMESTAMP: update_time,
    #         }
    #         print("Updated connection %s state (pool: %s)" % (identifier, self))
    #     else:
    #         print(
    #             "Failed to update connection %s state because no connection found " % identifier)
    #     self._pool_lock.release()
