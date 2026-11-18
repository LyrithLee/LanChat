import uuid
from discovery import Discovery

def node1():
    d = Discovery("Alice", "AAA", 8888, 9001)
    d.start()
    print("Alice 启动，等待搜索...")
    while True:
        cmd = input("输入 s 搜索，q 退出：")
        if cmd == "s":
            res = d.search()
            print("搜索结果：", res)
        elif cmd == "q":
            d.stop()
            break

if __name__ == "__main__":
    node1()
