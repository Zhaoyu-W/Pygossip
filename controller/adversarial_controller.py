from multiprocessing import Lock
from multiprocessing import Manager
from util.constants import ADVERSARIAL_DATA
from util.constants import IS_ADVERSARIAL


class AdversarialController:
    def __init__(self, connection_pool, adversarial=False):
        self.connection_pool = connection_pool
        self._adversarial = Manager().Value(IS_ADVERSARIAL, adversarial)
        self._adversarial_lock = Lock()

    def toggle_adversarial(self, command):
        self._adversarial_lock.acquire()
        if command == 'Y':
            self._adversarial.value = True
            print("[ADVERSARIAL]: Turn on adversarial gossip...")
        else:
            self._adversarial.value = False
            print("[ADVERSARIAL]: Turn off adversarial gossip...")
        self._adversarial_lock.release()

    def response(self, client_socket, client_identfier):
        self._adversarial_lock.acquire()
        if self._adversarial.value:
            client_socket.send(ADVERSARIAL_DATA.encode())
            print("[SERVER]: Responsed to %s adversarially!" % client_identfier)
        else:
            data = ""
            entries = self.connection_pool.get_all_entries()
            for idx in range(0, len(entries)):
                entry = entries[idx] if idx == len(entries)-1 \
                        else entries[idx]+"\n"
                data += entry
                client_socket.send(entry.encode())

            print("[SERVER]: Responsed %s to %s successfully!" % (data, client_identfier))
        self._adversarial_lock.release()
