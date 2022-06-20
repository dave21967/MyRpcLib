#MyRPCLib 

is a free open-source RPC library for Python made by me!

#Server
you can register new rpc functions, every function must start with "rpc_" and must contains *args as arguments

#Client
you can call remote functions on the server, give arguments and get the return of the functions

#Python server example

```python
from rpclib.RpcServer import RpcServer

def rpc_say_hello(*args):
    return "Hello World!"

def rpc_sum(*args):
    data = eval(args[0])
    return data[0]+data[1]

def rpc_print_msg(*args):
    data = eval(args[0])
    print(data[0])
    return "print successfull!"

def main():
    server = RpcServer(("localhost", 3000))
    server.register_method(rpc_say_hello)
    server.register_method(rpc_sum)
    server.register_method(rpc_print_msg)
    server.serve()

if __name__ == '__main__':
    main()
```

#Python client example
```python
from rpclib.RpcClient import RpcClient

def main():
    client = RpcClient(("localhost",3000))
    res=client.call("rpc_print_msg", "Hello from client!")
    print(res)
    client.close()


if __name__ == '__main__':
    main()
```