"""
discovery.py向外暴露一个Discovery类

Discovery类实现两个核心功能：
1. 主动搜索用户：新建socket，向局域网广播探测请求，收集其他在线节点的单播回复，返回在线用户列表快照
2. 被动监听响应：在后台监听UDP发现端口，收到探测请求后，以单播方式回复自身信息（昵称、聊天端口、node_id）

Discovery类向外提供的方法：
1. start()：启动后台UDP监听线程，绑定发现端口，开始被动等待别人的搜索请求，调用后立即返回，不阻塞
2. search()：发起一次局域网广播搜索，在超时窗口内收集在线节点响应，返回在线用户列表
3. stop()：停止监听循环，关闭UDP socket，释放端口资源
"""

import socket
import threading
import uuid
import time
from protocol import make_discover, make_discover_reply, parse_message

class Discovery:
    def __init__(self, nickname, node_id, disc_port, chat_port): 
        # 保存信息
        self.nickname=nickname
        self.node_id=node_id
        self.disc_port=disc_port
        self.chat_port=chat_port
        # 创建UDP套接字
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(0.5)
        # 初始化运行状态标记，初始化线程变量，创建在线成员peers列表
        self.running=False
        self.listen_thread=None
        self.peers=[]

    def _listen_loop(self):
        while self.running:
            try:
                data, addr=self.sock.recvfrom(4096)
            except socket.timeout:
                continue
            msg=parse_message(data)
            if msg is None :
                continue
            elif msg["type"] == "discover":
                msg_reply=make_discover_reply(msg['reqId'], self.node_id, self.nickname, self.chat_port)
                self.sock.sendto(msg_reply, addr)

    def start(self):
        # 绑定端口
        self.sock.bind(("",self.disc_port))
        # 更新运行状态标志
        self.running=True
        # 创建线程
        self.listen_thread=threading.Thread(target=self._listen_loop, daemon=True)
        # 运行线程
        self.listen_thread.start()

    def _get_reqId(self):
        reqId=str(uuid.uuid4())
        return reqId
    
    def search(self, timeout=1.5)->list:
        self.peers=[]
        reqId=self._get_reqId()
        msg_search=make_discover(reqId, self.disc_port)
        sock_search=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock_search.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock_search.settimeout(0.5)
        sock_search.sendto(msg_search,("255.255.255.255", self.disc_port))
        start_time=time.time()
        while time.time() - start_time < timeout:
            try:
                data, addr=sock_search.recvfrom(4096)
            except socket.timeout:
                continue
            msg=parse_message(data)
            if msg is None:
                continue
            if msg["type"] != "discover_reply" or msg["reqId"] != reqId:
                continue
            found=False
            for p in self.peers:
                if p["nodeId"] == msg["nodeId"]:
                    found=True
                    break
            if found:
                continue
            self.peers.append({
                "nodeId":msg["nodeId"],
                "nickname":msg["name"],
                "chatPort":msg["chatPort"],
            })
        sock_search.close()
        return self.peers
    
    def stop(self):
        self.running = False
        if self.listen_thread is not None:
            self.listen_thread.join()
        self.sock.close()



    