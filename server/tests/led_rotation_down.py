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
    led3.on()
    sleep(DELAY)
    led3.off()
    sleep(DELAY)
    led4.on()
    sleep(DELAY)
    led4.off()
    sleep(DELAY)

    led8.on()
    sleep(DELAY)
    led8.off()
    sleep(DELAY)
    led7.on()
    sleep(DELAY)
    led7.off()
    sleep(DELAY)
