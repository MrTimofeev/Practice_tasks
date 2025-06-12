class Router():

    def __init__(self):
        self.buffer = []
        self._list_conected_server = []

    def link(self, server):
        self._list_conected_server.append(server)
        server.conected_to_router = self

    def unlink(self, server):
        self._list_conected_server.remove(server)
        server.conected_to_router = None

    def send_data(self):
        for packet in self.buffer:
            for sv in self._list_conected_server:
                if sv.get_ip() == packet.ip:
                    sv.buffer.append(packet)
        self.buffer = []


class Server():
    __ip_counter = 1

    def __init__(self):
        self.buffer = []
        self.ip = self.__ip_counter
        Server.__ip_counter += 1
        self.connected_to_router = None

    def send_data(self, data):
        if self.connected_to_router:
            self.connected_to_router.buffer.append(data)

    def get_data(self):
        all_messages = self.buffer
        self.buffer = []
        return all_messages

    def get_ip(self):
        return self.ip


class Data():

    def __init__(self, data, ip):
        self.data = data
        self.ip = ip
