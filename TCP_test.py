# 客户端编程
# 导入socket库:
import socket

# 创建一个socket:AF_INET指定使用IPv4协议，如果要用更先进的IPv6，就指定为AF_INET6
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#SOCK_STREAM指定使用面向流的TCP协议
# 建立连接:
s.connect(('www.sina.com.cn', 80))  #一个tuple，包含地址和端口号
# 发送数据:b' 指的就是bytes类型。
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
# 接收数据:
buffer = []
while True:
    # 每次最多接收1k字节:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)  #b''是一个空字节，join是连接列表的函数，buffer是一个字节串的列表
#使用空字节把buffer这个字节列表连接在一起，成为一个新的字节串
#接收数据时，调用recv(max)方法，一次最多接收指定的字节数，
#功能就是把[b'ab',b'cd',b'ef']变成 b'abcdef'
# 因此，在一个while循环中反复接收，直到recv()返回空数据，表示接收完毕，退出循环。
# 关闭连接:
s.close()
header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))
# 把接收的数据写入文件:
with open('sina.html', 'wb') as f:
    f.write(html)
