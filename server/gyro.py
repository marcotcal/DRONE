#!/usr/bin/python3
#
# MPU 6050 TEST
#
import smbus
import math
from curses import wrapper
import time;

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
def main(stdscr):
    stdscr.clear()

    
    stdscr.addstr(10,10,"Gyro Test")
    stdscr.addstr(11,10,"=========")
    
    try:
        while True:
            gyro_x = read_word_2c(0x43)
            gyro_y = read_word_2c(0x45)
            gyro_z = read_word_2c(0x47)
    
            acel_x = read_word_2c(0x3b)
            acel_y = read_word_2c(0x3d)
            acel_z = read_word_2c(0x3f)
    
            stdscr.addstr(15,10,"Gyro X {}".format(gyro_x/131))
            stdscr.addstr(16,10,"Gyro Y {}".format(gyro_y/131))
            stdscr.addstr(17,10,"Gyro Z {}".format(gyro_z/131))
    
            stdscr.addstr(18,10,"Acel X {}".format(acel_x/16384))
            stdscr.addstr(19,10,"Acel Y {}".format(acel_y/16384))
            stdscr.addstr(20,10,"Acel Z {}".format(acel_z/16384))
            
            rot_x = get_x_rotation(acel_x/16384, acel_y/16384, acel_z/16384) 
            rot_y = get_y_rotation(acel_x/16384, acel_y/16384, acel_z/16384) 

            stdscr.addstr(22,10,"X Rot {}".format(rot_x))
            stdscr.addstr(24,10,"Y Rot {}".format(rot_y))

            stdscr.refresh()
            time.sleep(1)

    except:
        pass

    stdscr.getkey()


bus = smbus.SMBus(1) 
address = 0x68       
bus.write_byte_data(address, power_mgmt_1, 0)
wrapper(main)

