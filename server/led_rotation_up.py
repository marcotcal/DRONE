from gpiozero import LED
from time import sleep

led1 = LED(16) # FTE
led2 = LED(20) # FTD
led3 = LED(21) # FBE
led4 = LED(17) # FBD
led5 = LED(27) # TTE
led6 = LED(22) # TTD
led7 = LED(26) # TBE
led8 = LED(19) # TBD


TURNS = 20
DELAY = .1

for i in range(1, TURNS):
    led1.on()
    sleep(DELAY)
    led1.off()
    sleep(DELAY)
    led2.on()
    sleep(DELAY)
    led2.off()
    sleep(DELAY)

    led6.on()
    sleep(DELAY)
    led6.off()
    sleep(DELAY)
    led5.on()
    sleep(DELAY)
    led5.off()
    sleep(DELAY)
