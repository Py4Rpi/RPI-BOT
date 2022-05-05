# INTERNAL MODULES
import socket
import os
from subprocess import check_output
import logging
import time

# EXTERNAL MODULES
import telebot
import lib8relay
from gpiozero import LED, Button
import paramiko
from paramiko import BadHostKeyException, SSHException

# BOT CREDENTIALS
import config

bot = telebot.TeleBot(config.token)
user_id = config.user_id
local_ip = config.local_ip
default_conn = config.gw[2]

# LOGGER CONFIG
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

# KEYBOARDS
main_keyboard = telebot.types.ReplyKeyboardMarkup()
main_keyboard.row('/terminal', '/ssh', '/relay')
terminal_keyboard = telebot.types.ReplyKeyboardMarkup()
terminal_keyboard.row('/exit')
ssh_keyboard0 = telebot.types.ReplyKeyboardMarkup()
ssh_keyboard0.row('INIT CHECK IPs')
ssh_keyboard = telebot.types.ReplyKeyboardMarkup()
ssh_keyboard.row('LOCAL HOST IP', 'DEFAULT CONN. IP')
relay_keyboard = telebot.types.ReplyKeyboardMarkup()
relay_keyboard.row('RELAY 1 on', 'RELAY 1 off', 'RELAY 2 on', 'RELAY 2 off')
relay_keyboard.row('RELAY 3 on', 'RELAY 3 off', 'RELAY 4 on', 'RELAY 4 off')


# INITIAL MSG AFTER START
def init_msg():
    bot.send_message(user_id, 'RPI BOT ONLINE \n' + "local ip is: " +
                     local_ip + '\n' + "default conn. ip is: " + default_conn + '\n' + "SELECT MODE:",
                     reply_markup=main_keyboard)


init_msg()

# OPTIONAL RASPBERRY PI GPIO FUNCS###
# green = LED(17)
# button = Button(27)
# def led_on():
#    green.on()
#    logging.info('led on')
# def led_off():
#    green.off()
#    logging.info('led off')
# button.when_released = led_on
# button.when_pressed = led_off
####################################

# GLOBAL VARIABLE
switch = 0

#MODE SELECTION
@bot.message_handler(commands=['start', 'terminal', 'ssh', 'relay', 'exit'])
def init_cmd(cmd):
    global switch

    if cmd.text == "/start":
        bot.send_message(cmd.chat.id, "SELECT MODE:",
                         reply_markup=main_keyboard)
        logging.info('SWITCHED TO START')
        switch = "/start"
        print(switch)

    elif cmd.text == "/terminal":
        bot.send_message(cmd.chat.id, 'SWITCHED TO TERMINAL.' + '\n' +' ENTER COMMAND:',
                         reply_markup=terminal_keyboard)
        logging.info('SWITCHED TO TERMINAL')
        switch = "/terminal"
        print(switch)

    elif cmd.text == "/ssh":
        bot.send_message(cmd.chat.id, 'SWITCHED TO SSH',
                         reply_markup=ssh_keyboard0)
        logging.info('SWITCHED TO SSH')
        switch = "/ssh"
        print(switch)

    elif cmd.text == "/relay":
        bot.send_message(cmd.chat.id, 'SWITCHED TO RELAY CONTROL',
                         reply_markup=relay_keyboard)
        logging.info('SWITCHED TO RELAY CONTROL')
        switch = "/relay"
        print(switch)

    elif cmd.text == "/exit":
        bot.send_message(cmd.chat.id, "SELECT MODE:",
                         reply_markup=main_keyboard)
        logging.info('EXIT MODE')
        switch = "/start"
        print(switch)

#MAIN OPERATIONS
@bot.message_handler(content_types=["text"])
def funcs(message):
    # ACCESS TERMINAL WITH "SUBPROCESS" LIB
    if switch == "/terminal":   
        comand = message.text  # MSG TEXT
        try:  # if wrong cmd - check_output gives exception
            bot.send_message(message.chat.id, check_output(comand, shell=True))

        except:
            bot.send_message(message.chat.id, "Invalid input")
            
     # ACCESS TERMINAL WITH "PARAMIKO" LIB
    elif switch == "/ssh":  
        bot.send_message(message.chat.id, "local ip is: " + local_ip + '\n' +
                         "default conn. ip is: "  + default_conn + '\n' + "SELECT MODE:", reply_markup=ssh_keyboard)
        if message.text == 'LOCAL HOST IP':
            var_ip = local_ip
        elif message.text == 'DEFAULT CONN. IP':
            var_ip = default_conn

        print("SSH client assembly...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("SSH client assembled.")

        try:
            bot.send_message(message.chat.id, "trying " + var_ip + ' ...')
            client.connect(hostname=var_ip, username=config.login, password=config.pswd, look_for_keys=False,
                           allow_agent=False)
            bot.send_message(message.chat.id, "connected to " + var_ip)
            print("invoke shell...")
            ssh = client.invoke_shell()
            time.sleep(1)
            print("Invoke shell done.")
            time.sleep(1)
            ssh.send('ls\n')
            time.sleep(1)
            ssh.recv(20000)
            time.sleep(1)
            ssh.send('python3\n')
            time.sleep(1)
            bot.send_message(message.chat.id, ssh.recv(20000))
            ssh.send('print("HELLO BEETROOT!")\n')
            time.sleep(1)
            bot.send_message(message.chat.id, ssh.recv(20000))
            time.sleep(1)
            bot.send_message(message.chat.id, 'completed')
            return init_msg()
      
                
        except (BadHostKeyException, SSHException):
            logging.error(msg='Cannot establish connection', exc_info=True)
            print("Cannot establish connection")
            time.sleep(1)
            return None
    # RELAY CONTROL MODE
    elif switch == "/relay":

        if message.text == 'RELAY 1 on':
            bot.send_message(message.chat.id, 'relay 1 on')
            lib8relay.set(1, 1, 1)
            logging.info('RELAY 1 on')
        elif message.text == 'RELAY 1 off':
            bot.send_message(message.chat.id, 'relay 1 off')
            lib8relay.set(1, 1, 0)
            logging.info('RELAY 1 off')
        elif message.text == 'RELAY 2 on':
            bot.send_message(message.chat.id, 'relay 2 on')
            lib8relay.set(1, 2, 1)
            logging.info('RELAY 2 on')
        elif message.text == 'RELAY 2 off':
            bot.send_message(message.chat.id, 'relay 2 off')
            lib8relay.set(1, 2, 0)
            logging.info('RELAY 2 off')
        elif message.text == 'RELAY 3 on':
            bot.send_message(message.chat.id, 'relay 3 on')
            lib8relay.set(1, 3, 1)
            logging.info('RELAY 3 on')
        elif message.text == 'RELAY 3 off':
            bot.send_message(message.chat.id, 'relay 3 off')
            lib8relay.set(1, 3, 0)
            logging.info('RELAY 3 off')
        elif message.text == 'RELAY 4 on':
            bot.send_message(message.chat.id, 'relay 4 on')
            lib8relay.set(1, 4, 1)
            logging.info('RELAY 4 on')
        elif message.text == 'RELAY 4 off':
            bot.send_message(message.chat.id, 'relay 4 off')
            lib8relay.set(1, 4, 0)
            logging.info('RELAY 4 off')

bot.polling(none_stop=True) 


