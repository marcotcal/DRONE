import curses
import traceback
import subprocess
import threading
import time
from oleddisplay import OledDisplay
from gyroscopes import Gyroscopes

class DroneInterface:

    def __init__(self):

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        self.oled = OledDisplay()
        self.clear_oled()
        self.gyro = Gyroscopes()
        self.gyro.init_mpu() 

    def __del__(self):

        pass

    def clear_oled(self):

        self.oled.clear()

    def menu_main(self):

        self.stdscr.addstr(7,  5,  '1 - Calibrate Gyroscopes', curses.A_BOLD)
        self.stdscr.addstr(8,  5,  '2 - Show Gyroscope Values', curses.A_BOLD)
        self.stdscr.addstr(9,  5,  '3 - Show Remote Control Throttle, Pitch, Yaw, Roll', curses.A_BOLD)
        self.stdscr.addstr(10, 5,  '4 - Display Statistics', curses.A_BOLD)
        self.stdscr.addstr(11, 5,  '5 - Clear Display', curses.A_BOLD)

    def init_screen(self):

        self.stdscr.border(0)
        self.stdscr.addstr(0, 4, ' Drone Server Interface ', curses.A_BOLD)
        self.menu_main()
        self.stdscr.addstr(22, 5, 'Press q to close this screen', curses.A_NORMAL)
        self.stdscr.addstr(20, 5, 'Option: ', curses.A_BOLD)

    def shutdown_screen(self):

        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def system_info(self):

        self.clear_oled()

        cmd = "hostname -I | cut -d\' \' -f1"
        ip = subprocess.check_output(cmd, shell = True ).decode('utf-8')
        cmd = "top -bn1 | grep load | awk '{print $11 \" \" $12 \" \" $13}'"
        cpu = subprocess.check_output(cmd, shell = True ).decode('utf-8')
        cmd = "free -m | awk 'NR==2{printf \"%s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        mem_usage = subprocess.check_output(cmd, shell = True ).decode('utf-8')
        cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB %s\", $3,$2,$5}'"
        disk = subprocess.check_output(cmd, shell = True ).decode('utf-8')

        self.oled.write_line(0, "IP : " + ip)
        self.oled.write_line(1, "CPU: " + cpu)
        self.oled.write_line(2, "Mem: " + mem_usage)
        self.oled.write_line(3, "Dsk: " + disk)


    def display_gyroscope(self, stop):

        pass

    def command_read(self, stop):
        while True:
            # implement read control loop

            if stop():
                print("Terminating command thread")
                break;

    def main_loop(self):
    
        stop_thread = False
        thr_cmd = threading.Thread(target=self.command_read, args=(lambda: stop_thread,))
        thr_cmd.daemon = True
        thr_cmd.start()
        
        try:

            self.init_screen()
            while True:
                ch = self.stdscr.getch()
                if ch == ord('q'):
                    stop_threads = True
                    break

                elif ch == ord('4'):
                    self.system_info()

                elif ch == ord('5'):
                    self.clear_oled()

        except Exception as e: 

            pass    

        self.shutdown_screen()
        stop_thread = True
        thr_cmd.join()


if __name__ == "__main__":

    try:
        drone = DroneInterface()
        drone.main_loop()

    except:
        traceback.print_exc()
    

