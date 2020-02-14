import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, Pango, GObject
import threading
import time
import serial
import math

class MainWindow:

    def on_destroy(self, *args):
        Gtk.main_quit()

    def set_ui(self):
        ed_pre_procedure = self.builder.get_object("ed_source_pre_procedure")

    def on_exit_app(self, button):
        Gtk.main_quit()

    def __init__(self):

        GObject.threads_init()

        objects = ["MainWindow", "AdjustYAW", "AdjustROLL", ]

        self.ard = serial.Serial('/dev/ttyUSB0',9600)

        self.throttle = 0;

        self.builder = Gtk.Builder()
        self.builder.add_objects_from_file("/home/pi/DRONE/interface/drone.glade", objects)

        self.builder.connect_signals(self)
        self.window = self.builder.get_object("MainWindow")

        # Buttons
        self.ctrl1 = self.builder.get_object("CTRL01")
        self.ctrl2 = self.builder.get_object("CTRL02")
        self.ctrl3 = self.builder.get_object("CTRL03")
        self.ctrl4 = self.builder.get_object("CTRL04")
        self.ctrl5 = self.builder.get_object("CTRL05")
        self.ctrl6 = self.builder.get_object("CTRL06")
        self.ctrl7 = self.builder.get_object("CTRL07")

        self.ping_counter = self.builder.get_object("PingCounter")

        # Joysticks

        # Bar controls

        self.bar_throttle = self.builder.get_object("BarThrottle")
        self.bar_pitch = self.builder.get_object("BarPitch")

        # Scale Controls

        self.bar_yaw = self.builder.get_object("BarYaw")
        self.bar_roll = self.builder.get_object("BarRoll")

        # Axis Indicators

        self.axis_throttle = self.builder.get_object("AxisThrottle")
        self.axis_pitch = self.builder.get_object("AxisPitch")
        self.axis_yaw = self.builder.get_object("AxisYaw") 
        self.axis_roll = self.builder.get_object("AxisRoll")

        def read_ping():
            count = 0
            while True:
                count += 1
                print("{}".format(count))
                time.sleep(1)

        def update_params(value):

            add_throttle = (511 - int(value[0])) / 20 

            # Joystick error correction
            if abs(add_throttle) < 3:
                add_throttle = 0

            if add_throttle > 0: 
                self.throttle += math.floor(add_throttle)
            else:
                self.throttle += math.ceil(add_throttle)

            if self.throttle < 0:
                self.throttle = 0;

            if self.throttle > 1023:
                self.throttle = 1023

            # self.axis_throttle.set_text("{}".format(self.throttle))
            self.axis_throttle.set_text("{}".format(self.throttle))
            self.bar_throttle.set_value(self.throttle)
            self.axis_pitch.set_text(value[2])
            self.bar_pitch.set_value(1023-int(value[2]))
            self.axis_yaw.set_text(value[1])
            self.bar_yaw.set_value(int(value[1]))
            self.axis_roll.set_text(value[3])
            self.bar_roll.set_value(int(value[3]))

            self.ctrl1.set_value(int(value[4]))
            self.ctrl2.set_value(int(value[5]))
            self.ctrl3.set_value(int(value[6]))
            self.ctrl4.set_value(int(value[7]))
            self.ctrl5.set_value(int(value[8]))
            self.ctrl6.set_value(int(value[9]))
            self.ctrl7.set_value(int(value[10]))

        def read_serial():
            while True:
                try:
                    data = self.ard.readline()
                    line = data.decode("utf-8")
                    line = line.replace("\n", "")
                    line = line.replace("\r", "")
                    params = line.split(",")
                    # print(params)
                    GLib.idle_add(update_params, params)
                    # time.sleep(0.2)
                except Exception as e:
                    print('Error', e)

        print('init thread')
        thread = threading.Thread(target=read_serial)
        thread.daemon = True
        thread.start()

