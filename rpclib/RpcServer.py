import socket
from threading import Thread
from rpclib.NonRemoteMethodError import NonRemoteMethodError

class RpcServer:
    def __init__(self, addr: tuple[str, int], backlog=10) -> None:
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.listener.bind(addr)
        self.listener.listen(backlog)
        self.remote_methods = {}
    
    def serve(self):
        print("server running...")
        while True:
            conn, addr = self.listener.accept()
            self.clients.append(conn)
            thr = Thread(target=self._handle_client, args=(conn, ))
            thr.start()
            print("new client connected")
        self.listener.close()
    
    def register_method(self, method):
        if not self.has_method(method.__name__) and method.__name__.startswith("rpc_"):
            self.remote_methods[method.__name__] = method
        else:
            raise NonRemoteMethodError("la funzione che si tenta di registrare non è una funzione remota!")

    def has_method(self, method) -> bool:
        return method in self.remote_methods
    
    def _handle_client(self, conn: socket.socket):
        while True:
            data = conn.recv(1024).decode()
            if data:
                method = data.split("=")[1]
                method = method.split(",")[0]
                args = data.split("=")[2]
                if self.has_method(method):
                    res = {"data": str(self.remote_methods[method](args))}
                    print(self.remote_methods[method])
                    if 'data' in res:
                        conn.send(str("Result="+res['data']).encode())
                if method == 'close':
                    self.clients.remove(conn)
                    conn.close()
                    break