import touchio
import busio
import board
import time
import digitalio
import random

dotstar = busio.SPI(board.APA102_SCK, board.APA102_MOSI)
r = 0
g = 0
b = 0
u = 0

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def setPixel(red, green, blue):
    if not dotstar.try_lock():
        return
    print("setting pixel to: %d %d %d" % (red, green, blue))
    data = bytearray([0x00, 0x00, 0x00, 0x00, 0xff, blue, green, red, 0xff, 0xff, 0xff, 0xff])
    dotstar.write(data)
    dotstar.unlock()

while u < 20:
    setPixel(r,b,g)
    led.value = True
    time.sleep(0.1)
    led.value = False
    time.sleep(0.1)
    r = random.randrange(20)
    g = random.randrange(20)
    b = random.randrange(20)
    u = u+1


#while not i2c.try_lock():
#    pass
#try:
   # [hex(x) for x in i2c.scan()]

    #i2c.writeto(0x28, bytes([0xaa]), stop=False)
    #result = bytearray(4)
    #i2c.readfrom_into(0x28, result)
    #time.delay(.5)
#finally:
 #   i2c.unlock()

#result
#bytearray(b'\xc1s')

