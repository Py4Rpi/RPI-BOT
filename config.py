import socket
import os

token="???"
user_id = ???
login = '???'
pswd = '???'
local_ip = socket.gethostbyname(socket.gethostname())
gw = os.popen("ip -4 route show default").read().split()
# print("telebot module is at: " + telebot.__file__)
