import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, Pango, GObject
import threading
import time
import serial
import math
import socket

__DRONE_PORT__ = 8888
__DRONE_IP__ = "192.168.1.1"

class MainWindow:

    def on_destroy(self, *args):
        Gtk.main_quit()
        if self.error is not None:
            self.soc.send("--quit--")

    def set_ui(self):
        ed_pre_procedure = self.builder.get_object("ed_source_pre_procedure")

    def on_exit_app(self, button):
        Gtk.main_quit()

    def on_select_parameters(self, button):
        self.main_area.set_visible_child(self.parameters_page)

    def on_select_camera(self, button):
        self.main_area.set_visible_child(self.camera_page)


    def __init__(self):

        GObject.threads_init()

        objects = [
                "MainWindow", 
                "AdjustYAW", 
                "AdjustROLL", 
                "AdjustCameraHorizontal",
                "AdjustCameraVertical"
                ]

        self.ard = serial.Serial('/dev/ttyUSB0',9600)

        self.throttle = 0;

        self.builder = Gtk.Builder()
        self.builder.add_objects_from_file("/home/pi/DRONE/interface/drone.glade", objects)

        self.builder.connect_signals(self)
        self.window = self.builder.get_object("MainWindow")

        self.port = __DRONE_PORT__
        self.host = __DRONE_IP__
        self.error = None 
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Buttons
        self.ctrl1 = self.builder.get_object("CTRL01")
        self.ctrl2 = self.builder.get_object("CTRL02")
        self.ctrl3 = self.builder.get_object("CTRL03")
        self.ctrl4 = self.builder.get_object("CTRL04")
        self.ctrl5 = self.builder.get_object("CTRL05")
        self.ctrl6 = self.builder.get_object("CTRL06")
        self.ctrl7 = self.builder.get_object("CTRL07")

        # Messages
        self.message = self.builder.get_object("message")

        # pages
        self.main_area = self.builder.get_object("MainArea")
        self.parameters_page = self.builder.get_object("ParametersPage")
        self.camera_page = self.builder.get_object("CameraPage")

        # ping counter
        self.ping_counter = self.builder.get_object("PingCounter")

        # Camera

        self.camera_horizontal = self.builder.get_object("CameraHorizontal")
        self.camera_vertical = self.builder.get_object("CameraVertical")

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

            param_send = value;
            param_send[0] = str(int(self.throttle * 180 / 1023))
            param_send[1] = str(int(float(value[1]) * 180 / 1023))
            param_send[2] = str(180-int(float(value[2]) * 180 / 1023))
            param_send[3] = str(int(float(value[3]) * 180 / 1023))
            send_txt = ",".join(param_send)
            print(send_txt)
            if self.error is None:
                self.soc.send(send_txt.encode())

        def read_serial():
            while True:
                try:
                    data = self.ard.readline()
                    line = data.decode("utf-8")
                    line = line.replace("\n", "")
                    line = line.replace("\r", "")

                    line += ",{}".format(self.camera_horizontal.get_value())
                    line += ",{}".format(self.camera_vertical.get_value())

                    params = line.split(",")

                    GLib.idle_add(update_params, params)
                    # time.sleep(0.2)
                except Exception as e:
                    print('Error', e)

        try:
            self.soc.setblocking(False);
            self.soc.settimeout(10);
            self.soc.connect((self.host, self.port))
            
        except Exception as e:
            self.error = "connection error"
            self.message.set_text(str(e))

        thread = threading.Thread(target=read_serial)
        thread.daemon = True
        thread.start()

