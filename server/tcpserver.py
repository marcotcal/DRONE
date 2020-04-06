import socket
import sys
import traceback
from threading import Thread
import logging
from gpiozero import LED
from time import sleep
from adafruit_servokit import ServoKit
import constants


class TCPServer:

    def __init__(self):

        self.kit = ServoKit(channels=16)

        self.led1 = LED(constants.LED_01)
        self.led2 = LED(constants.LED_02)
        self.led3 = LED(constants.LED_03)
        self.led4 = LED(constants.LED_04)
        self.led5 = LED(constants.LED_05)
        self.led6 = LED(constants.LED_06)
        self.led7 = LED(constants.LED_07)
        self.led8 = LED(constants.LED_08)

        self.led1on = False
        self.led2on = False
        self.led3on = False
        self.led4on = False
        self.led5on = False
        self.led6on = False
        self.led7on = False
        self.led8on = False

        self.kit.servo[0].angle = 90
        self.kit.servo[1].angle = 90
        self.kit.servo[2].angle = 0
        self.kit.servo[3].angle = 0
        self.kit.servo[4].angle = 0
        self.kit.servo[5].angle = 0
        self.kit.servo[6].angle = 0

    def gimble_vertical(self, position):
        self.kit.servo[1].angle = position

    def gimble_horizontal(self, position):
        self.kit.servo[0].angle = position

    def start_server(self):
        host = "192.168.1.1"
        port = 8888

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print("Socket created")

        try:
            soc.bind((host, port))
        except socket.error:
            print("Bind failed. Error : " + str(sys.exc_info()))
            sys.exit()

        soc.listen(5)
        print("Socket now listening")

        try:
            while True:
                connection, address = soc.accept()
                ip, port = str(address[0]), str(address[1])
                print("Connected with " + ip + ":" + port)

                try:
                    Thread(target=self.client_thread, args=(connection, ip, port)).start()
                except Exception as e:
                    print("Thread did not start.")
                    logging.exception(e)
                    traceback.print_exc()
        except KeyboardInterrupt:
            print("stoping")
            
        finally:
            soc.close()

    def client_thread(self, connection, ip, port, max_buffer_size = 5120):
        is_active = True
        camera_horizontal = 90
        camera_vertical = 90
        elevator = 0
        throttle = 0
        aileron = 0
        rudder = 0
        auxiliary = 0
    
        while is_active:
            client_input = self.receive_input(connection, max_buffer_size)
    
            if "--QUIT--" in client_input:
                print("Client is requesting to quit")
                connection.close()
                print("Connection " + ip + ":" + port + " closed")
                is_active = False
            else:
    
                param = client_input.split(",")  
                #print("Command {}".format(client_input))
    
                if param[4] == "1":
                    self.led1.on()
                    self.led2.on()
                    self.led5.on()
                    self.led6.on()
                else:
                    self.led1.off()
                    self.led2.off()
                    self.led5.off()
                    self.led6.off()
    
                # camera gimbal
    
                if param[8] == "1":
                    self.kit.servo[0].angle = 90
                    self.kit.servo[1].angle = 90
    
                new_cam_h_pos = int(float(param[11]))
                new_cam_v_pos = int(float(param[12]))
    
                new_throttle = int(float(param[0]))
    
                if new_throttle > 10:
                    if new_throttle < 60:
                        new_throttle = 60
                    else:
                        pass
                else:
                        pass
    
                new_rudder =   int(float(param[1]))
                new_elevator = int(float(param[2]))
                new_aileron =  int(float(param[3]))
                new_auxiliary = 0
    
                if aileron != new_aileron:
                    aileron = new_aileron
                    #self.kit.servo[2].angle = aileron
    
                if elevator != new_elevator:
                    elevator = new_elevator
                    #self.kit.servo[3].angle = elevator
    
                if throttle != new_throttle:
                    throttle = new_throttle
                    print ('Throttle ',throttle)
                    self.kit.servo[12].angle = throttle
                    self.kit.servo[13].angle = throttle
                    self.kit.servo[14].angle = throttle
                    self.kit.servo[15].angle = throttle
    
                if rudder != new_rudder:
                    rudder = new_rudder
                    #self.kit.servo[5].angle = rudder
    
                if auxiliary != new_auxiliary:
                    auxiliary = new_auxiliary
                    #self.kit.servo[6].angle = auxiliary
    
                if new_cam_h_pos != camera_horizontal:
                    camera_horizontal = new_cam_h_pos
                    self.kit.servo[0].angle = camera_horizontal
    
                if new_cam_v_pos != camera_vertical:
                    camera_vertical = new_cam_v_pos
                    self.kit.servo[1].angle = camera_vertical
    
                if client_input == "B2":
                    if self.led1.value:
                        self.led1.off()
                        self.led2.off()
                        self.led5.off()
                        self.led6.off()
                    else:
                        self.led1.on()
                        self.led2.on()
                        self.led5.on()
                        self.led6.on()
    
                if client_input == "B9":
                    if self.led3.value:
                        self.led3.off()
                        self.led4.off()
                        self.led7.off()
                        self.led8.off()
                    else:
                        self.led3.on()
                        self.led4.on()
                        self.led7.on()
                        self.led8.on()
    
                if client_input == "B3":
                    self.gimble_horizontal(90)
                    self.gimble_vertical(90)
    
    
                if client_input[0:5] == "CAN_X":
                    try:
                        value = int(client_input[5:])
                        self.gimble_horizontal(value)
                    except:
                        pass
    
                if client_input[0:5] == "CAN_Y":
                    try:
                        value = int(client_input[5:])
                        self.gimble_vertical(value)
                    except:
                        pass
    
                if client_input[0:2] == "AI":
                    try:
                        value = int(client_input[2:])
                        self.gimble_horizontal(value)
                    except:
                        pass
    
                if client_input[0:2] == "EL":
                    try:
                        value = int(client_input[2:])
                        self.gimble_vertical(value)
                    except:
                        pass
    
                connection.sendall("-".encode("utf8"))
    
    def receive_input(self, connection, max_buffer_size):
        client_input = connection.recv(max_buffer_size)
        client_input_size = sys.getsizeof(client_input)
    
        if client_input_size > max_buffer_size:
            print("The input size is greater than expected {}".format(client_input_size))
    
        decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
        result = self.process_input(decoded_input)
    
        return result
    
    def process_input(self, input_str):
        return str(input_str).upper()


if __name__ == "__main__":

    srv = TCPServer()
    srv.start_server()
