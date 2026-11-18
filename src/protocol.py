'''
在局域网中，客户端需要进行广播来发现其他用户，其他用户需要通过单播来回应自身存在

两类信息：
① discover信息：
注释：客户端用来发现其他用户时，用来广播的信息
字段：
type：str，固定为discover
reqId:str，非空
replyPort:int，1~65535

② discover_reply信息：
注释：其他用户用来回应自身存在的信息
字段：
type：str，固定为discover_reply
reqId:str，非空
nodeId:str，非空
name:str，非空
chatPort:int，1~65535
'''

import json

# ---------------------------
#          信息构造函数
# ---------------------------

# 构造discover信息
def make_discover(reqId:str, replyPort:int)->bytes:
    dict_discover=dict(type='discover', reqId=reqId, replyPort=replyPort)
    json_discover=json.dumps(dict_discover)
    bytes_discover=json_discover.encode("utf-8")
    return bytes_discover
# 构造discover_reply信息
def make_discover_reply(reqId:str, nodeId:str, name:str, chatPort:int)->bytes:
    dict_discover_reply=dict(type='discover_reply', reqId=reqId, nodeId=nodeId, name=name, chatPort=chatPort)
    json_discover_reply=json.dumps(dict_discover_reply)
    bytes_discover_reply=json_discover_reply.encode("utf-8")
    return bytes_discover_reply 

# ---------------------------
#          信息解析函数
# ---------------------------

def _is_valid_reqId(reqId):
    if not isinstance(reqId,str):
        return False
    if 0 < len(reqId) <= 128:
        return True

def _is_valid_Port(msg_replyPort):
    if not isinstance(msg_replyPort,int):
        return False
    if 1 <= msg_replyPort <= 65535:
        return True

def _is_valid_nodeId(msg_nodeId):
    if not isinstance(msg_nodeId,str):
        return False
    if 0 < len(msg_nodeId) <= 128:
        return True

def _is_valid_name(msg_name):
    if not isinstance(msg_name,str):
        return False
    if 0 < len(msg_name) <= 128:
        return True
    
def parse_message(data:bytes):
    try:
        text=data.decode("utf-8")
        msg=json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(msg,dict):
        return None
    
    msg_type=msg.get('type')
    if msg_type not in ('discover','discover_reply'):
        return None
    
    if msg_type == 'discover':
        msg_reqId=msg.get('reqId')
        if not _is_valid_reqId(msg_reqId):
            return None
        msg_replyPort=msg.get('replyPort')
        if not _is_valid_Port(msg_replyPort):
            return None
        return {
            "type": msg_type,
            "reqId": msg_reqId,
            "replyPort": msg_replyPort,
        }
    
    elif msg_type == 'discover_reply':
        msg_reqId=msg.get('reqId')
        if not _is_valid_reqId(msg_reqId):
            return None
        msg_nodeId=msg.get('nodeId')
        if not _is_valid_nodeId(msg_nodeId):
            return None
        msg_name=msg.get('name')
        if not _is_valid_name(msg_name):
            return None
        msg_chatPort=msg.get('chatPort')
        if not _is_valid_Port(msg_chatPort):
            return None
        return {
            "type": msg_type,
            "reqId": msg_reqId,
            "nodeId": msg_nodeId,
            "name": msg_name,
            "chatPort": msg_chatPort,
        }

if __name__ == '__main__':
    print(make_discover('req-1','12345'))



