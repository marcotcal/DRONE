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

        self.AccErrorX = 0
        self.AccErrorY = 0

        self.GyrErrorX = 0
        self.GyrErrorY = 0
        self.GyrErrorZ = 0

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
        Ax = x/16384.0 
        Ay = y/16384.0
        Az = z/16384.0
        
        return Ax,Ay,Az

    def gyro(self):
        x = self.read_mpu(GYRO_X)
        y = self.read_mpu(GYRO_Y)
        z = self.read_mpu(GYRO_Z)
        Gx = x/131.0
        Gy = y/131.0
        Gz = z/131.0
        
        return Gx, Gy, Gz

    def temp(self):
        temp_raw = self.read_mpu(TEMP)
        temp_c = (temp_raw / 340.0) + 36.53
        
        return temp_c

    def calibrate(self, cycles=200):
        x = 0.0
        y = 0.0
        z = 0.0
        AccErrorX = 0
        AccErrorY = 0

        # accelerometers

        for i in range(cycles):
            x,y,z = self.accel() 
            AccErrorX = AccErrorX + ((math.atan((y) / math.sqrt(math.pow((x), 2) + math.pow((z), 2))) * 180 / math.pi)) 
            AccErrorY = AccErrorY + ((math.atan(-1 * (x) / math.sqrt(math.pow((y), 2) + math.pow((z), 2))) * 180 / math.pi))

        AccErrorX = AccErrorX / cycles
        AccErrorY = AccErrorY / cycles

        # gyroscopes 

        x = 0.0
        y = 0.0
        z = 0.0
        GyrErrorX = 0
        GyrErrorY = 0
        GyrErrorZ = 0

        for i in range(cycles):
            x,y,z = self.gyro() 
            GyrErrorX = GyrErrorX + x 
            GyrErrorY = GyrErrorY + y 
            GyrErrorZ = GyrErrorZ + z 

        GyrErrorX = GyrErrorX / cycles 
        GyrErrorY = GyrErrorY / cycles 
        GyrErrorZ = GyrErrorZ / cycles 

        self.AccErrorX = AccErrorX
        self.AccErrorY = AccErrorY

        self.GyrErrorX = GyrErrorX 
        self.GyrErrorY = GyrErrorY 
        self.GyrErrorZ = GyrErrorZ 

        return AccErrorX, AccErrorY, GyrErrorX, GyrErrorY, GyrErrorZ 

    def get_y_rotation(self):
        x,y,z = self.accel()
        return (math.atan(-1 * x / math.sqrt(math.pow(y, 2) + math.pow(z, 2))) * 180 / math.pi) - self.AccErrorY;
 
    def get_x_rotation(self):
        x,y,z = self.accel()
        return (math.atan(y / math.sqrt(math.pow(x, 2) + math.pow(z, 2))) * 180 / math.pi) - self.AccErrorX;
 
