import curses
import traceback


class DroneInterface:

    def __init__(self):

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)

    def __del__(self):

        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def menu_main(self):

        self.stdscr.addstr(7, 5, '1 - Calibrate Gyroscopes', curses.A_BOLD)
        self.stdscr.addstr(8, 5, '2 - Show Gyroscope Values', curses.A_BOLD)
        self.stdscr.addstr(9, 5, '3 - Show Remote Control Throttle, Pitch, Yaw, Roll', curses.A_BOLD)

    def init_screen(self):

        self.stdscr.border(0)
        self.stdscr.addstr(0, 4, ' Drone Server Interface ', curses.A_BOLD)
        self.menu_main()
        self.stdscr.addstr(22, 5, 'Press q to close this screen', curses.A_NORMAL)
        self.stdscr.addstr(20, 5, 'Option: ', curses.A_BOLD)

    def main_loop(self):
    
        self.init_screen()
        while True:
            ch = self.stdscr.getch()
            if ch == ord('q'):
                break

if __name__ == "__main__":

    try:
        drone = DroneInterface()
        drone.main_loop()

    except:
        traceback.print_exc()
    

