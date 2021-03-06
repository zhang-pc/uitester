from socketserver import ThreadingTCPServer, StreamRequestHandler
import json
from threading import Thread
import logging
import queue


logger = logging.getLogger('Tester')

Timeout = 120
Port = 11800


class RPCServer(ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self._agents = {}

    def add_agent(self, agent):
        self._agents[agent.device_id] = agent

    def rm_agent(self, device_id):
        self._agents.pop(device_id)

    def get_agent(self, device_id):
        return self._agents.get(device_id)


class RPCHandler(StreamRequestHandler):

    def __init__(self, request, client_address, server):
        self.has_register = False
        self.agent_proxy = None
        super().__init__(request, client_address, server)

    def handle(self):
        while True:
            line = self.rfile.readline().decode().strip()
            if len(line) == 0:
                break
            try:
                msg = RPCMessage.from_json(line)
                if not self.has_register:
                    self.handle_register(msg)
                elif msg.msg_type == RPCMessage.RPC_KILL_SIGNAL:
                    self.handle_unregister()
                else:
                    self.handle_message(msg)
            except Exception as e:
                print(e.args)
                continue
        if self.has_register:
            self.server.rm_agent(self.agent_proxy.device_id)

    def handle_register(self, msg):
        if msg.msg_type == RPCMessage.RPC_CALL and msg.name == 'register':
            if len(msg.args) < 1:
                res = self._make_error_msg()
                self.wfile.write(res.to_bytes())
            self.agent_proxy = RPCAgent()
            self.agent_proxy.device_id = msg.args[0]
            self.agent_proxy.wfile = self.wfile
            self.agent_proxy.connection = self.connection
            self.server.add_agent(self.agent_proxy)
            self.has_register = True
            self.wfile.write(self._make_ok_msg().to_bytes())
        else:
            self.wfile.write(self._make_error_msg().to_bytes())

    def _make_ok_msg(self):
        ok_msg = RPCMessage()
        ok_msg.msg_type = RPCMessage.RPC_RESULT
        ok_msg.args = [True]
        ok_msg.name = 'ok'
        return ok_msg

    def _make_error_msg(self):
        err_msg = RPCMessage()
        err_msg.msg_type = RPCMessage.RPC_RESULT
        err_msg.args = [False]
        err_msg.name = 'error'
        return err_msg

    def handle_unregister(self):
        self.server.rm_agent(self.agent_proxy.device_id)
        self.connection.close()
        self.agent_proxy.is_closed = True

    def handle_message(self, msg):
        self.agent_proxy.responses.put(msg)


class RPCAgent:

    def __init__(self):
        self.device_id = ''
        self.is_closed = False
        self.msg_id = 0
        self.wfile = None
        self.connection = None
        self.responses = queue.Queue()

    def call(self, name, *args, timeout=Timeout, **kwargs):
        """
        kwargs:
        1) version
           version=1 use normal rpc call
           version=2 use reflection rpc call
           default is version=1

        reflection rpc call:
        name('call', 'call_static', 'new', 'delete') : reflection method name
        *args:
            'call' method need at least 2 arguments. 1)instance 2)method name 3)method arguments
            'call_static' need at least 2 arguments. 1)class name 2)method name 3)method arguments
            'new' need at least 1 argument. 1)class name 2)constructor arguments
            'delete' need at least 1 argument. 1)instance

        :return RemoteObject remote object contains 2 attr : hash and class . If remote object is android View,
        it have attr :'res-id' and 'content-des'. If remote object is TextView ,it have attr 'text'.

        Timeout:
            RPC Call has 30 sec timeout by default. You'll get a TimeoutError after 30sec.
        """
        self.msg_id += 1
        msg = RPCMessage()
        msg.msg_id = self.msg_id
        msg.msg_type = RPCMessage.RPC_CALL
        msg.name = name
        msg.args = args
        if 'version' in kwargs:
            msg.version = kwargs['version']
        self.wfile.write(msg.to_bytes())
        try:
            res = self.responses.get(timeout=timeout)
            return res
        except queue.Empty:
            raise TimeoutError("RPC Call timeout")

    def close(self):
        msg = RPCMessage.get_kill_signal()
        self.wfile.write(msg.to_bytes())


class RPCMessage:
    RPC_CALL = 1
    RPC_RESULT = 2
    RPC_KILL_SIGNAL = 99

    def __init__(self):
        self.msg_type = None
        self.msg_id = None
        self.version = 1
        self.name = None
        self.args = []

    @classmethod
    def get_kill_signal(cls):
        msg = cls()
        msg.name = 'kill'
        msg.msg_type = RPCMessage.RPC_KILL_SIGNAL
        return msg

    @classmethod
    def from_json(cls, json_str):
        msg_dict = json.loads(decode(json_str))
        if type(msg_dict) is not dict:
            raise TypeError('Json is not a dict, can\'t create rpc message')
        instance = cls()
        instance.__dict__ = msg_dict
        return instance

    def to_json(self):
        return encode(json.dumps(self.__dict__))

    def to_bytes(self):
        return (self.to_json() + '\n').encode()


def get_server(port):
    return RPCServer(('0.0.0.0', port), RPCHandler)


def start(port):
    server = get_server(port)
    t = Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()
    logger.debug('RPC Server started')
    return server


def encode(msg):
    """转译，规则为：
        % -> %e
        \n -> %n
    """
    msg = msg.replace("%", "%e")
    msg = msg.replace("\n", "%n")
    return msg


def decode(msg):
    """反转译，规则为：
        %n -> \n
        %e -> %
    """
    msg = msg.replace("%n", "\n")
    msg = msg.replace("%e", "%")
    return msg