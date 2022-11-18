import busio        # to access the bus on the trinket board
import board        # to access the tricket board's pads/pins
import time         # for time delays

# Set up SPI bus to access the DotStar RGB LED
dotstar = busio.SPI(board.APA102_SCK, board.APA102_MOSI)

# Set up I2C bus to access the pressure sensor
i2c = busio.I2C(board.SCL, board.SDA)

# Create an instance of the I2CDevice class for the pressure sensor, with I2C bus oject and its address
from adafruit_bus_device.i2c_device import I2CDevice
p_sensor = I2CDevice(i2c, 0x28)

p_min = 0                   # sensor is positive pressure so the range of pressure starts at 0 kpa
p_max = 6000                #   and maxes out at 6 kpa
out_min = 1677722           # sensor output min: 10% of of the pressure sensor count that should be around atmospheric pressure
out_max = 15099494          # sensor output max: 90% of the pressure sensor count

# This will take the result pulled from the sensor and turn it into a number and use it to calculate the pressure
def pressure(result1):
    output = (result1[1]<<16 |result1[2]<<8 | result1[3])               # takes the 3 bytes of data and combines to one number
    output = float(output)                                              # fixes an overflow problem
    p = ((output - out_min)*(p_max - p_min))/(out_max-out_min)+p_min    # conversion from data to pressure
    return p                                                            # return the pressure

# This will set the onboard RGB LED to any colour by passing in a combination of red, green and blue colour
def setRGB(red, green, blue):
    if not dotstar.try_lock():                                          # check to see if the bus is being used
        return
    data = bytearray([0x00, 0x00, 0x00, 0x00, 0xff, blue, green, red, 0xff, 0xff, 0xff, 0xff])
    dotstar.write(data)                                                 # write the above data to the dotstar to change the colour
    dotstar.unlock()                                                    # function to give back control of the I2C bus to other code

# This loop will repeat when ENTER is pressed, providing a new average pressure with each loop.
while True:
    input("Press ENTER to continue with pressure reading.")
    i = 0
    total_pressure = 0
    while i < 200:
        setRGB(0,0,0)                              # turn on blue on the RBG LED
        with p_sensor:
            p_sensor.write(bytes([0xaa,0x00,0x00]), end=1)    # write data to the pressure data address
            time.sleep(.005)
            result = bytearray(4)                   # create a byte array for the data to be put into.
            p_sensor.readinto(result)               # put the pressure data into the array
            time.sleep(.005)
        bytearray(b'\xc1s')                         # not sure what this does
        total_pressure = total_pressure + pressure(result)
        i = i+1
    ave_pressure = total_pressure/200
    print ("Average Pressure: ", ave_pressure)



