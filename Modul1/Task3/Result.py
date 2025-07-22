class Router():

    def __init__(self):
        self.buffer = []
        self._list_connected_server = []

    def link(self, server):
        self._list_connected_server.append(server)
        server.connected_to_router = self

    def unlink(self, server):
        self._list_connected_server.remove(server)
        server.connected_to_router = None

    def send_data(self):
        for packet in self.buffer:
            for sv in self._list_connected_server:
                if sv.get_ip() == packet.ip:
                    sv.buffer.append(packet)
                    break
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
        
    def __repr__(self):
        return f"{self.data}"

router = Router()
sv_from = Server() 
sv_from2 = Server() 
router.link(sv_from) 
router.link(sv_from2) 
router.link(Server()) 
router.link(Server()) 
sv_to = Server()
router.link(sv_to)
sv_from.send_data(Data("Hello", sv_to.get_ip())) 
sv_from2.send_data(Data("Hello", sv_to.get_ip())) 
sv_to.send_data(Data("Hi", sv_from.get_ip())) 
router.send_data()
print(sv_from.get_data())
print(sv_to.get_data())