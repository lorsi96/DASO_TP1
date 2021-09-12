import socket
from abc import ABC, abstractmethod

# ******************************************************************************************************************** #
#                                                      Exceptions                                                      #
# ******************************************************************************************************************** #
class ServerUnavailableError(Exception):
    pass

# ******************************************************************************************************************** #
#                                                      Interfaces                                                      #
# ******************************************************************************************************************** #
class Cliente(ABC):
    @abstractmethod
    def send(self, msg) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def close(self) -> bool:
        raise NotImplementedError

# ******************************************************************************************************************** #
#                                               Concrete Implementations                                               #
# ******************************************************************************************************************** #
class ClienteUdp(Cliente):
    def __init__(self, ip='localhost', port=8081, buffsize=1024, timeout=0.5) -> None:
        self._ip = ip 
        self._port = port
        self._buffsize = buffsize
        self._socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self._socket.settimeout(timeout)
    
    def send(self, msg:str):
        self._socket.sendto(msg.encode(), (self._ip, self._port))
        try:
            return bool(next(iter(self._socket.recvfrom(self._buffsize))).decode())
        except (socket.timeout, OSError):
            raise ServerUnavailableError('No response received from server.')
    
    def close(self):
        self._socket.close()
