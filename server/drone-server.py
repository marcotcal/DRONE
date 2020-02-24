import socket
import sys
import traceback
from threading import Thread
import logging
from gpiozero import LED
from time import sleep
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

led1 = LED(16)
led2 = LED(20)
led3 = LED(21)
led4 = LED(17)
led5 = LED(27)
led6 = LED(22)
led7 = LED(26)
led8 = LED(19)

led1on = False
led2on = False
led3on = False
led4on = False
led5on = False
led6on = False
led7on = False
led8on = False

kit.servo[0].angle = 90
kit.servo[1].angle = 90

def main():
    start_server()

def gimble_vertical(position):
    kit.servo[1].angle = position

def gimble_horizontal(position):
    kit.servo[0].angle = position

def start_server():
    host = "192.168.0.214"
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
                Thread(target=client_thread, args=(connection, ip, port)).start()
            except Exception as e:
                print("Thread did not start.")
                logging.exception(e)
                traceback.print_exc()
    except KeyboardInterrupt:
        print("stoping")
        
    finally:
        soc.close()


def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True

    while is_active:
        client_input = receive_input(connection, max_buffer_size)

        if "--QUIT--" in client_input:
            print("Client is requesting to quit")
            connection.close()
            print("Connection " + ip + ":" + port + " closed")
            is_active = False
        else:
            print("Command {} {}".format(client_input, led1.value))
            if client_input == "B2":
                if led1.value:
                    led1.off()
                    led2.off()
                    led5.off()
                    led6.off()
                else:
                    led1.on()
                    led2.on()
                    led5.on()
                    led6.on()

            if client_input == "B9":
                if led3.value:
                    led3.off()
                    led4.off()
                    led7.off()
                    led8.off()
                else:
                    led3.on()
                    led4.on()
                    led7.on()
                    led8.on()

            if client_input == "B3":
                gimble_horizontal(90)
                gimble_vertical(90)


            if client_input[0:5] == "CAN_X":
                try:
                    value = int(client_input[5:])
                    gimble_horizontal(value)
                except:
                    pass

            if client_input[0:5] == "CAN_Y":
                try:
                    value = int(client_input[5:])
                    gimble_vertical(value)
                except:
                    pass

            if client_input[0:2] == "AI":
                try:
                    value = int(client_input[2:])
                    gimble_horizontal(value)
                except:
                    pass

            if client_input[0:2] == "EL":
                try:
                    value = int(client_input[2:])
                    gimble_vertical(value)
                except:
                    pass

            connection.sendall("-".encode("utf8"))


def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)

    return result


def process_input(input_str):
    return str(input_str).upper()


if __name__ == "__main__":
    main()
