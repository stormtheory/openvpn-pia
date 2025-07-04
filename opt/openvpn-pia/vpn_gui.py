#!/usr/bin/python3
# Written by StormTheory DEC2024

import PIL
from PIL import Image
from pystray import MenuItem as Item
from pystray import Menu as Menu
import pystray
import argparse
import subprocess
import time
import sys
import os
import re
import threading
import logging
from subprocess import check_output

### Find Username
USERNAME = os.getlogin()
print(USERNAME)
logging.debug(USERNAME)


SERVICE = 'piavpn.service'
APP_NAME = 'VPN'
VPN_DEV = 'tun0'
USER_HOME = '/home/' + USERNAME
HOME_CONFIG = USER_HOME +'/.openvpn-pia.conf'

ICON_IMAGE_GREEN = '/opt/openvpn-pia/icons/vpn_green_mine.png'
ICON_IMAGE_RED = '/opt/openvpn-pia/icons/vpn_red_mine.png'
ICON_IMAGE_BROWN = '/opt/openvpn-pia/icons/vpn_brown_mine.png'
ICON_IMAGE_PURPLE = '/opt/openvpn-pia/icons/vpn_purple_mine.png'

IP_COMPARE = 'Enabled' #Enabled/Disabled

# Python COLORS
class pcolors:
    BGCOLOR = '#2B3856'
    LBGCOLOR = '#2B3856'
    RED = '#FF0000'
    GREEN = '#008000'
    ORANGE = '#FFA500'
    YELLOW = '#fdf623'
    WHITE = '#FFFFFF'
    BLACK = '#000000'

# TEXT COLORS
class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Defaults
EXIT_PYTHON = 'FALSE'
global icon_state
global service_state
icon_state = 'default'
service_state = 'default'

SCRIPT = subprocess.run(["basename {}".format(__file__)], shell=True, stdout=subprocess.PIPE).stdout.decode('ascii').rstrip('\r\n')
print(SCRIPT)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", action='store_true', help='Run program in debug mode')
args = parser.parse_args()

### SET LOGGING LEVEL
if args.debug:
    lLevel = logging.DEBUG     # INFO, DEBUG
else:
    lLevel = logging.INFO     # INFO, DEBUG

### LOGGER CONFIG
logger = logging.getLogger()
logger.setLevel(lLevel)

logging.debug('debug')

def btn_return():
    return

def relocate(FILE):
    subprocess.run(["sed -i '/run/c\\run {}' {}".format(FILE,HOME_CONFIG)], shell=True, stdout=subprocess.PIPE)
    vpn_restart()

def locate_chicago():
    relocate('us_chicago.ovpn')

def locate_MO():
    relocate('us_missouri.ovpn')

def locate_east():
    relocate('us_east.ovpn')

def locate_atlanta():
    relocate('us_atlanta.ovpn')

def locate_DC():
    relocate('us_washington_dc.ovpn')

def locate_switzerland():
    relocate('switzerland.ovpn')

def locate_netherlands():
    relocate('nl_amsterdam.ovpn')
    
def locate_germany():
    relocate('de_berlin.ovpn')

def locate_london():
    relocate('uk_london.ovpn')

def locate_manchester():
    relocate('uk_manchester.ovpn')

def locate_Ireland():
    relocate('ireland.ovpn')

def locate_FL():
    relocate('us_florida.ovpn')

def locate_IN():
    relocate('us_indiana.ovpn')

def locate_MI():
    relocate('us_michigan.ovpn')

def locate_sydney():
    relocate('aus-sydney.ovpn')

def locate_melbourne():
    relocate('aus_melbourne.ovpn')

def locate_brisbane():
    relocate('au_brisbane.ovpn')

def locate_new_zealand():
    relocate('new_zealand.ovpn')

def locate_costa_rica():
    relocate('costa_rica.ovpn')

def locate_HI():
    relocate('us_honolulu.ovpn')

def locate_west():
    relocate('us_west.ovpn')

def locate_CA():
    relocate('us_california.ovpn')
    
def locate_toronto():
    relocate('ca_toronto.ovpn')
    
def locate_vancouver():
    relocate('ca_vancouver.ovpn')

def locate_ontario():
    relocate('ca_ontario.ovpn')
    
def locate_south_korea():
    relocate('south_korea.ovpn')

def locate_singapore():
    relocate('singapore.ovpn')

def locate_japan():
    relocate('japan.ovpn')

global CHOICE_LOCATIONS
ASIA_LOCATIONS = pystray.Menu(Item("Japan", locate_japan), Item("Singapore", locate_singapore), Item("South Korea", locate_south_korea))
CANADA_LOCATIONS = pystray.Menu(Item("Ontario", locate_ontario), Item("Toronto", locate_toronto), Item("Vancouver", locate_vancouver))
EAST_LOCATIONS = pystray.Menu(Item("East", locate_east), Item("Atlanta", locate_atlanta), Item("Wash DC", locate_DC), Item("Florida", locate_FL))
CENTRAL_LOCATIONS = pystray.Menu(Item("Missouri", locate_MO), Item("Indiana", locate_IN), Item("Michigan", locate_MI), Item("Chicago", locate_chicago))
WEST_LOCATIONS = pystray.Menu(Item("West", locate_west), Item("California", locate_CA), Item("Hawaii", locate_HI))
US_LOCATIONS = pystray.Menu(Item("CENTRAL", CENTRAL_LOCATIONS), Item("EAST", EAST_LOCATIONS), Item("WEST", WEST_LOCATIONS))
OCEANIA_LOCATIONS = pystray.Menu(Item("Sydney", locate_sydney), Item("Melbourne", locate_melbourne), Item("Brisbane", locate_brisbane), Item("New Zealand", locate_new_zealand))
EUROPE_LOCATIONS = pystray.Menu(Item("Switzerland", locate_switzerland), Item("Netherlands", locate_netherlands), Item("UK London", locate_london), Item("UK Manchester", locate_manchester), Item("Ireland", locate_Ireland), Item("Germany", locate_germany))
CHOICE_LOCATIONS = pystray.Menu(Item("US", US_LOCATIONS), Item("CANADA", CANADA_LOCATIONS), Item("EUROPE", EUROPE_LOCATIONS), Item("OCEANIA", OCEANIA_LOCATIONS), Item("ASIA", ASIA_LOCATIONS), Item("Costa Rica", locate_costa_rica))

def THERE_ONLY_CAN_BE_ONE():
  global EXIT_PYTHON
  RUNNING_TEST = subprocess.run(["ps -ef|grep python3|grep './{}'|grep -v grep|wc -l".format(SCRIPT)], shell=True, stdout=subprocess.PIPE).stdout
  COUNT = str(RUNNING_TEST.decode('ascii').rstrip('\r\n'))
  logging.debug('App PID Run Count: ' + COUNT)
  if COUNT > str('1'):
    print(bcolors.YELLOW + 'App is already running. Exiting...' + bcolors.NC)
    EXIT_PYTHON = 'True'
    sys.exit()
  else:
    EXIT_PYTHON = 'False'
THERE_ONLY_CAN_BE_ONE()

#### ERROR CHECK FOR IF FILES ARE PRESENT
def check_file_exists_exit(FILE):
  try:
    with open(FILE) as f:
      pass
  except FileNotFoundError:
    print('ERROR: ' + FILE + ' was not found!... exiting')
    sys.exit(1)
def check_dir_exists_exit(DIR):
  if not os.path.exists(DIR):
    print('ERROR: ' + DIR + ' was not found!... exiting')
    sys.exit(1)
check_file_exists_exit(HOME_CONFIG)
check_dir_exists_exit(USER_HOME)


def find_config_distination():
    LOCATION = subprocess.run(["ls -al /opt/openvpn-pia/pia.conf|awk '{print $11}'"], shell=True, stdout=subprocess.PIPE).stdout.decode('ascii').rstrip('\r\n')
    LOCATION = subprocess.run(["basename {}".format(LOCATION)], shell=True, stdout=subprocess.PIPE).stdout.decode('ascii').rstrip('\r\n')
    return LOCATION

def service_status(qservice):
    global CHOICE_LOCATIONS
    global service_state
    SLEEP = 2
    while True:
        if 'EXIT_PYTHON' in globals():
            if EXIT_PYTHON == 'TRUE':
                print('ERROR: Exit SERVICE Thread')
                sys.exit()
        time.sleep(SLEEP)
        #service = subprocess.run(["systemctl is-active --quiet {}".format(qservice)], shell=True, stdout=subprocess.PIPE)
        service = subprocess.run(["ip link show {}".format(VPN_DEV)], shell=True, stdout=subprocess.PIPE)
        ReturnCode = service.returncode

        try:
            if str(ReturnCode) == '0':
                if service_state != 'online':
                    logging.debug(SERVICE + ' is online')
                    icon_change('green')
                    service_state = 'online'
                    
                    LOCATION = find_config_distination()
                    tray_notifation(APP_NAME, 'Online ' + LOCATION)
                    systray.menu = pystray.Menu(Item("Turn Off", vpn_off), Item('Change Location', CHOICE_LOCATIONS), Item(LOCATION, btn_return), Item("Exit", exit_app))
                    SLEEP = 2
                        
                    logging.debug(VPN_DEV)
                    CONN = subprocess.run(["cat /sys/class/net/{}/carrier".format(VPN_DEV)], shell=True, stdout=subprocess.PIPE).stdout.decode('ascii').rstrip('\r\n')
                    logging.debug(CONN)
                    if IP_COMPARE == 'Enabled':
                        if os.geteuid() != 0:
                            time.sleep(6)
                            if CONN == '1':
                                EXT_IP = subprocess.run(["curl ipinfo.io/ip"], shell=True, stdout=subprocess.PIPE).stdout.decode('ascii').rstrip('\r\n')
                                logging.debug(EXT_IP)

                                ### Check IP Address of the Network to the Public Address
                                CONFIG_IP = subprocess.run(["grep remote /opt/openvpn-pia/pia.conf|grep -v server|awk '{print $2}'|sed 's/[0-9]\\+/ /5'"], shell=True, stdout=subprocess.PIPE).stdout.decode('ascii').rstrip('\r\n')
                                
                                ### Come and clean this up
                                qEXT_IP = EXT_IP.split(".")
                                logging.debug('qEXT_IP ' + str(qEXT_IP))
                                IP1 = qEXT_IP[0]
                                IP2 = qEXT_IP[1]
                                IP3 = qEXT_IP[2]
                                qEXT_IP_final = str(IP1 + '.' + IP2 + '.' + IP3 + '.')
                                
                                ### Come and clean this up
                                qCONFIG_IP = CONFIG_IP.split(".")
                                logging.debug('qCONFIG_IP ' + str(qCONFIG_IP))
                                IP1 = qCONFIG_IP[0]
                                IP2 = qCONFIG_IP[1]
                                IP3 = qCONFIG_IP[2]
                                qCONFIG_IP_final = str(IP1 + '.' + IP2 + '.' + IP3 + '.')

                                logging.debug('NET ' + str(qCONFIG_IP_final))
                                logging.debug('NET ' + str(qEXT_IP_final))
                                if qEXT_IP_final == qCONFIG_IP_final:
                                    logging.debug('green')
                                    icon_change('green')
                                else:
                                    logging.debug('red')
                                    icon_change('red')
                    else:
                        ### IP_COMPARE is Disabled
                        time.sleep(6)
                        EXT_IP = 'Disabled'
                        logging.debug('EXT_IP Disabled: green')
                        icon_change('green')

                    if CONN == '1':
                        #### Pull more data for Display
                        ETH_IP = subprocess.run(["ifconfig tun0 |grep 'inet'|grep -v inet6|awk '{print $2}'"], shell=True, stdout=subprocess.PIPE).stdout.decode('ascii').rstrip('\r\n')
                        logging.debug(ETH_IP)
                        LOCATION = find_config_distination()
                        systray.menu = pystray.Menu(Item("Turn Off", vpn_off), Item('Change Location', CHOICE_LOCATIONS), Item(LOCATION, btn_return), Item('Public IP: ' + EXT_IP, btn_return), Item('LAN: ' + ETH_IP, btn_return), Item("Exit", exit_app))
                        ### Look up Cipher level
                        CIPHER_LEVEL = subprocess.run(["grep cipher /opt/openvpn-proton/proton.conf|awk '{print $2}'"], shell=True, stdout=subprocess.PIPE).stdout.decode('ascii').rstrip('\r\n')
                        systray.menu = pystray.Menu(Item("Turn Off", vpn_off), Item('Change Location', CHOICE_LOCATIONS), Item(LOCATION, btn_return), Item('Public IP: ' + EXT_IP, btn_return), Item('LAN: ' + ETH_IP, btn_return), Item(CIPHER_LEVEL, btn_return), Item("Exit", exit_app))

            else:
                if service_state != 'offline':
                    logging.debug(SERVICE + ' is offline')
                    icon_change('brown')
                    service_state = 'offline'
                    LOCATION = find_config_distination()
                    systray.menu = pystray.Menu(Item("Turn On", vpn_restart), Item('Change Location', CHOICE_LOCATIONS), Item(LOCATION, btn_return), Item("Exit", exit_app))
                    time.sleep(2)
                    tray_notifation(APP_NAME, 'Offline')
                    SLEEP = 5
        except:
            continue
            
def exit_app(icon, item):
    print('Exit called')
    global EXIT_PYTHON
    EXIT_PYTHON = 'TRUE'
    sys.exit(0)

def vpn_off():
    subprocess.run(["timeout 5 sudo systemctl stop {}".format(SERVICE)], shell=True, stdout=subprocess.PIPE)

def vpn_restart():
    subprocess.run(["timeout 5 sudo systemctl restart {}".format(SERVICE)], shell=True, stdout=subprocess.PIPE)
    global service_state
    time.sleep(2)
    service_state = 'offline'

def tray_notifation(Title, Message):
  systray.notify(Message, Title)

def icon_change(category):
    global icon_state
    if category == icon_state:
        return
    else:
        if category == 'green':
            logger.debug('Icon change: ' + category)
            systray.icon = PIL.Image.open(ICON_IMAGE_GREEN)
            icon_state = category
        elif category == 'red':
            logger.debug('Icon change: ' + category)
            systray.icon = PIL.Image.open(ICON_IMAGE_RED)
            icon_state = category
        elif category == 'brown':
            logger.debug('Icon change: ' + category)
            systray.icon = PIL.Image.open(ICON_IMAGE_BROWN)
            icon_state = category
        else:
            logger.debug('Icon change: Default')
            systray.icon = PIL.Image.open(ICON_IMAGE_PURPLE)
            icon_state = category

def SystemTrayIcon():
  global CHOICE_LOCATIONS
  global APP_NAME
  while True:
    if 'EXIT_PYTHON' in globals():
        if EXIT_PYTHON == 'TRUE':
            print('ERROR: Exit SystemTray Thread')
            sys.exit()

    print('system tray')
    print(CHOICE_LOCATIONS)
    icon = PIL.Image.open(ICON_IMAGE_PURPLE)
    smenu = pystray.Menu(Item("Off", vpn_off), Item('Change Location', CHOICE_LOCATIONS), Item("Restart", vpn_restart), Item("Exit", exit_app))
    global systray
    systray = pystray.Icon(name=APP_NAME, icon=icon, title='VPN', menu=smenu)
    try:
        systray.run()
    except:
        logging.debug('systray will not start')
    logger.debug('systray rerun')


t1 = threading.Thread(target=SystemTrayIcon, daemon=False)
t2 = threading.Thread(target=service_status, args=(SERVICE,), daemon=False)

t1.start()
t2.start()

while True:
    time.sleep(5)
    if EXIT_PYTHON == 'TRUE':
        print('Need to Exit GUI')
        PID = subprocess.run(["ps -ef|grep python3|grep './{}'|grep -v grep|awk '{print $2}'".format(SCRIPT)], shell=True, stdout=subprocess.PIPE).stdout.decode('ascii').rstrip('\r\n')
        print('PID')
        EXIT_OUTPUT = subprocess.run(["kill -9 {}".format(PID)], shell=True)
        print(EXIT_OUTPUT)
        sys.exit(0)
