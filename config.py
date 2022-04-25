import socket
import os

token="1334027775:AAHnuoDQWUBlmhAKYy7_Ch9goCq-YfCGp40"
user_id = 737422517
login = 'vito'
pswd = 'Har23ley!'
local_ip = socket.gethostbyname(socket.gethostname())
gw = os.popen("ip -4 route show default").read().split()
# print("telebot module is at: " + telebot.__file__)
