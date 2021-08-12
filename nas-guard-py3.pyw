# -*- coding: utf-8 -*-
# author:　cheneyjin@outlook.com
# create 20210804

import os
import re
import socket

import random
import argparse

import platform
from time import sleep
import time

BAND = '''
  _   _           _____       _____ _    _         _____  _____  
 | \ | |   /\    / ____|     / ____| |  | |  /\   |  __ \|  __ \ 
 |  \| |  /  \  | (___      | |  __| |  | | /  \  | |__) | |  | |
 | . ` | / /\ \  \___ \     | | |_ | |  | |/ /\ \ |  _  /| |  | |
 | |\  |/ ____ \ ____) |    | |__| | |__| / ____ \| | \ \| |__| |
 |_| \_/_/    \_\_____/      \_____|\____/_/    \_\_|  \_\_____/ 

 [NAS_GUARD]: shutdown your device where your router can not find in times.
'''

CMD_WINDOWS_SHUTDOWN = "shutdown -s -t 00"
CMD_WINDOWS_HIBERNATION1 = "rundll32 powrprof.dll,SetSuspendState"
CMD_WINDOWS_HIBERNATION2 = "shutdown -h"

CMD_LINUX_SHUTDOWN = "shutdown -h 00"
CMD_LINUX_HIBERNATION = "systemctl hybrid-sleep"

SYSTEM_WINDOWS = 1
SYSTEM_LINUX = 2
SYSTEM_OSX = 3


class SystemAction(object):
    def hibernate(self):
        pass

    def shutdown(self):
        pass


class WindowsSystemAction(SystemAction):

    def hibernate(self):
        super().hibernate()
        os.system(CMD_WINDOWS_HIBERNATION2)

    def shutdown(self):
        super().shutdown()
        os.system(CMD_WINDOWS_SHUTDOWN)


class LinuxSystemAction(SystemAction):

    def hibernate(self):
        super().hibernate()
        os.system(CMD_LINUX_HIBERNATION)

    def shutdown(self):
        super().shutdown()
        os.system(CMD_LINUX_SHUTDOWN)


def check_system():
    if str(platform.system()).lower().__contains__('win'):
        return SYSTEM_WINDOWS
    else:
        return SYSTEM_LINUX


def find_router(router):
    skt = socket.socket()
    skt.settimeout(3)
    # noinspection PyBroadException
    try:
        return skt.connect_ex(router) == 0
    except Exception as e:
        return False
    finally:
        skt.close()


# noinspection PyShadowingNames
def patrol(ip, port, tolerate_count, action):
    # print(tolerate_count, ip, port)
    if check_system() == SYSTEM_WINDOWS:
        system_action = WindowsSystemAction()
    else:
        system_action = LinuxSystemAction()
    count = 0
    while count < tolerate_count:
        sleep(30 + random.randint(1, 10))
        router_exist = find_router(router=(ip, port))
        if not router_exist:
            count = count + 1
            print('[{}][T:{}, C:{}]: lost connection, maybe your power was outage'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), tolerate_count, count))
        else:
            count = 0
    if action != 1:
        system_action.shutdown()
    else:
        system_action.hibernate()


def parse_args():
    parser = argparse.ArgumentParser(description=BAND)
    parser.add_argument("-r", "--router", help="your router ip", type=str, required=True)
    parser.add_argument("-p", "--port", help="your router port", type=int, required=True)
    parser.add_argument("-t", "--tolerate", help="times can tolerate that lost router when connect", type=int)
    parser.add_argument("-a", "--action", help="(0/none):shutdown, (1):hibernate", type=int)

    args = parser.parse_args()
    if args.router:
        compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if not compile_ip.match(args.router):
            print("ip is illegal")
            return
    if args.port < 1 or args.port > 65535:
        print("port is illegal")
        return
    if args.tolerate is None:
        args.tolerate = 3
    if not find_router(router=(args.router, args.port)):
        print("router can not connected")
        return
    return args.router, args.port, args.tolerate, 0 if args.action is None or args.action != 1 else 1


if __name__ == '__main__':
    # os.system(CMD_WINDOWS_SHUTDOWN)
    with open(r'NAS.GUARD', 'w', encoding="utf-8") as file:
        file.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    params = parse_args()
    if params is not None:
        BAN_DEAD_LOOP = 20
        print("all is ok, please switch it to the background. process will start in {} minutes.".format(BAN_DEAD_LOOP))
        # !!! give nas 20 minutes to start !!!
        sleep(60 * BAN_DEAD_LOOP)
        # _thread.start_new_thread(patrol, (params[2], params[0], params[1], ))
        patrol(params[0], params[1], params[2], params[3])
