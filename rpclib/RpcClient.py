import socket
import json

class RpcClient:
    def __init__(self, addr: tuple[str, int]) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(addr)
    
    def call(self, method, *args):
        self.socket.send(str("method="+method+",args="+str(args)).encode())
        res = self.socket.recv(1024)
        return res.decode().split("=")[1]
    
    def close(self):
        self.socket.close()