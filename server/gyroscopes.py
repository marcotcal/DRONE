import time
import smbus
import math

PWR_M = 0x6B
DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_EN = 0x38
ACCEL_X = 0x3B
ACCEL_Y = 0x3D
ACCEL_Z = 0x3F
GYRO_X = 0x43
GYRO_Y = 0x45
GYRO_Z = 0x47

TEMP = 0x41
bus= smbus.SMBus(1)

Device_Address = 0x68

class Gyroscopes:

    def __init__(self):

        self.AxCal=0
        self.AyCal=0
        self.AzCal=0
        self.GxCal=0
        self.GyCal=0
        self.GzCal=0

    def __del__(self):

        pass 

    def init_mpu(self):

        bus.write_byte_data(Device_Address, DIV, 7)
        bus.write_byte_data(Device_Address, PWR_M, 1)
        bus.write_byte_data(Device_Address, CONFIG, 0)
        bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
        bus.write_byte_data(Device_Address, INT_EN, 1)

    def read_mpu(self, addr):
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
        value = ((high << 8) | low)
        if(value > 32768):
            value = value - 65536
        return value

    def accel(self):
        x = self.read_mpu(ACCEL_X)
        y = self.read_mpu(ACCEL_Y)
        z = self.read_mpu(ACCEL_Z)
        Ax = x/16384.0 - self.AxCal
        Ay = y/16384.0 - self.AyCal
        Az = z/16384.0 - self.AzCal
        
        return Ax,Ay,Az

    def gyro(self):
        x = self.read_mpu(GYRO_X)
        y = self.read_mpu(GYRO_Y)
        z = self.read_mpu(GYRO_Z)
        Gx = x/131.0 - self.GxCal
        Gy = y/131.0 - self.GyCal
        Gz = z/131.0 - self.GzCal
        
        return Gx, Gy, Gz

    def temp(self):
        temp_raw = self.read_mpu(TEMP)
        temp_c = (temp_raw / 340.0) + 36.53
        
        return temp_c

    def calibrate(self, cycles=50):
        x = 0.0
        y = 0.0
        z = 0.0

        # accelerometers

        for i in range(cycles):
            x = x + self.read_mpu(ACCEL_X)
            y = y + self.read_mpu(ACCEL_Y)
            z = z + self.read_mpu(ACCEL_Z)
            
        self.AxCal = x / cycles / 16384.0
        self.AyCal = y / cycles / 16384.0
        self.AzCal = z / cycles / 16384.0

        # gyroscopes 

        x = 0.0
        y = 0.0
        z = 0.0

        for i in range(cycles):
            x = x + self.read_mpu(GYRO_X)
            y = y + self.read_mpu(GYRO_Y)
            z = z + self.read_mpu(GYRO_Z)

        self.GxCal = x / cycles / 131.0
        self.GyCal = x / cycles / 131.0
        self.GzCal = x / cycles / 131.0

        return self.AxCal, self.AyCal, self.AzCal, self.GxCal, self.GyCal, self.GzCal

        def get_y_rotation(self):
            x,y,z = self.accel()
            radians = math.atan2(x, dist(y,z))
            return -math.degrees(radians)
 
        def get_x_rotation(self):
            x,y,z = self.accel()
            radians = math.atan2(y, dist(x,z))
            return math.degrees(radians)
 
