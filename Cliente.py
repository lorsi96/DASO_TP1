from abc import ABC, abstractmethod
import socket


class Cliente(ABC):
    @abstractmethod
    def send(self, msg) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def close(self) -> bool:
        raise NotImplementedError
        
class ClienteUdp(Cliente):
    def __init__(self, ip='127.0.1', port=8081, buffsize=1024) -> None:
        self._ip = ip 
        self._port = port
        self._buffsize = buffsize
        self._socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    def send(self, msg:str) -> bool:
        self._socket.sendto(msg.encode(), (self._ip, self._port))
        return next(iter(self._socket.recvfrom(self._buffsize))).decode()
    
    def close(self):
        self._socket.close()
