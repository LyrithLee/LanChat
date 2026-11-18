"""
discovery.py向外暴露一个Discovery类

Discovery类实现两个核心功能：
1. 主动搜索用户：向局域网广播探测请求，收集其他在线节点的单播回复，返回在线用户列表快照
2. 被动监听响应：在后台监听UDP发现端口，收到探测请求后，以单播方式回复自身信息（昵称、聊天端口、node_id）

Discovery类向外提供的方法：
1. start()：启动后台UDP监听线程，绑定发现端口，开始被动等待别人的搜索请求，调用后立即返回，不阻塞
2. search()：发起一次局域网广播搜索，在超时窗口内收集在线节点响应，返回在线用户列表
3. stop()：停止监听循环，关闭UDP socket，释放端口资源
"""

import socket
import threading

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
            pass
    def start(self):
        # 绑定端口
        self.sock.bind(("",self.disc_port))
        # 更新运行状态标志
        self.running=True
        # 创建线程
        self.listen_thread=threading.Thread(target=self._listen_loop, daemon=True)
        # 运行线程
        self.listen_thread.start()
        



    