import neopixel
from microbit import display
from microbit import pin0
from microbit import pin1
from microbit import pin2
from microbit import pin3
from microbit import pin4
from microbit import pin5
from microbit import pin6
from microbit import pin7
from microbit import pin8
from microbit import pin9
from microbit import pin10
from microbit import pin11
from microbit import pin12
from microbit import pin16 
from microbit import sleep
from random import randint

# Reuse GPIO pins P3, P4, P6, P7, P9, P10 as Digital by
# uncouple the pins from the LED matrix
display.off()
randomMode = False
np8 = neopixel.NeoPixel(pin8,8)
np12 = neopixel.NeoPixel(pin12,8)
np16 = neopixel.NeoPixel(pin16,8)

# LED's above buttons        
def panelLEDs(pix, col):
    np16[pix] = (col)
    np16.show()

# LED's next to switches on pin8
def signalPoleLEDs1(pix, col):
    np8[pix] = (col)
    np8.show()    

# LED's next to switches on pin12
def signalPoleLEDs2(pix, col):
    np12[pix] = (col)
    np12.show()    

# Power LED ON
panelLEDs(7,(100,0,0))

def setBeginState():
    # Reset LED ON
    panelLEDs(4,(0,200,0))
    global randomMode
    global switch1Pos, switch2Pos, switch3Pos, switch4Pos
    switch1Pos = 2
    switch2Pos = 2
    switch3Pos = 2
    switch4Pos = 2
    randomMode = False
    # Remove power from all switches
    removePowerFromSwitches()
    print('Remove power from all switches and set position to 1')
    sleep(300)
    # Set all switches in start position 1
    flipSwitch(1)
    flipSwitch(2)
    flipSwitch(3)
    flipSwitch(4)
    randomMode = False
    # Reset LED off
    panelLEDs(4,(0,0,0))

# Power off all switch coins
def removePowerFromSwitches():
    pin0.write_digital(0)  # switch 1, coin 1
    pin1.write_digital(0)  # switch 1, coin 2
    pin2.write_digital(0)  # switch 2, coin 1
    pin3.write_digital(0)  # switch 2, coin 2
    pin4.write_digital(0)  # switch 3, coin 1
    pin6.write_digital(0)  # switch 3, coin 2
    pin7.write_digital(0)  # switch 4, coin 1
    pin9.write_digital(0)  # switch 4, coin 2

# Read binary representation of the 10 to 4 line encoder (74HCT147)
# We use it as 8 to 3 encoder
# On the encoder inputs I1..I8 we have 8 buttons
# The encoder outputs Y0, Y1 and Y2 are connected to pin5, pin10 and pin11
def readButtonsStateAsBinaryAndConvertToDecimal():
    decimal = 0
    if pin5.read_digital(): decimal = 1
    if pin10.read_digital(): decimal = decimal + 2
    if pin11.read_digital(): decimal = decimal + 4
    return 7 - decimal # encoder output is inverted
    # encoder has strange way of binary counting
    # but we do not use output 8 so commenting out
    # output = 7 - decimal  
    # if output == 0:
    #    output = 8  
    # return output

def flipSwitch(switch):
    global switch1Pos, switch2Pos, switch3Pos, switch4Pos
    if switch == 1:
        if switch1Pos == 1:
            pin1.write_digital(1)
            sleep(500)
            pin1.write_digital(0)
            switch1Pos = 2
            panelLEDs(0,(0,55,100))
            flipSignalPoleLEDs(0, 2)
        else:
            pin0.write_digital(1)
            sleep(500)
            pin0.write_digital(0)
            switch1Pos = 1
            panelLEDs(0,(55,100,0))
            flipSignalPoleLEDs(0, 1)
    elif switch == 2:
        if switch2Pos == 1:
            pin3.write_digital(1)
            sleep(500)
            pin3.write_digital(0)
            switch2Pos = 2
            panelLEDs(1,(0,55,100))
            flipSignalPoleLEDs(2, 2)
        else:
            pin2.write_digital(1)
            sleep(500)
            pin2.write_digital(0)
            switch2Pos = 1
            panelLEDs(1,(55,100,0))
            flipSignalPoleLEDs(2, 1)
    elif switch == 3:
        if switch3Pos == 1:
            pin6.write_digital(1)
            sleep(500)
            pin6.write_digital(0)
            switch3Pos = 2
            panelLEDs(2,(0,55,100))
            flipSignalPoleLEDs(4, 2)
        else:
            pin4.write_digital(1)
            sleep(500)
            pin4.write_digital(0)
            switch3Pos = 1
            panelLEDs(2,(55,100,0))
            flipSignalPoleLEDs(4, 1)
    elif switch == 4:
        if switch4Pos == 1:
            pin9.write_digital(1)
            sleep(500)
            pin9.write_digital(0)
            switch4Pos = 2
            panelLEDs(3,(0,55,100))
            flipSignalPoleLEDs(6, 2)
        else:
            pin7.write_digital(1)
            sleep(500)
            pin7.write_digital(0)
            switch4Pos = 1
            panelLEDs(3,(55,100,0))
            flipSignalPoleLEDs(6, 1)

def flipSignalPoleLEDs(pix, position):
    if position == 1:
        signalPoleLEDs1(pix,(100,0,0))
        signalPoleLEDs1(pix+1,(0,100,0))
        signalPoleLEDs2(pix,(100,0,0))
        signalPoleLEDs2(pix+1,(0,100,0))
    else:
        signalPoleLEDs1(pix,(0,100,0))
        signalPoleLEDs1(pix+1,(100,0,0))
        signalPoleLEDs2(pix,(0,100,0))
        signalPoleLEDs2(pix+1,(100,0,0))

setBeginState()
while True:
    buttonPressed = readButtonsStateAsBinaryAndConvertToDecimal()
    # Button 1 pressed, flip switch 1
    if buttonPressed == 1: flipSwitch(1)
    # Button 2 pressed, flip switch 2
    if buttonPressed == 2: flipSwitch(2)
    # Button 3 pressed, flip switch 3
    if buttonPressed == 3: flipSwitch(3)
    # Button 4 pressed, flip switch 4
    if buttonPressed == 4: flipSwitch(4)
    if buttonPressed == 5:
        if randomMode:
            # Button 5 pressed, random mode OFF
            randomMode = False
            panelLEDs(6,(0,0,0))
            #print('Button 5 pressed, random mode OFF')
        else:
            # Button 5 pressed, random mode ON
            g = randint(0,100)
            r = randint(0,100)
            b = randint(0,100)
            randomMode = True
            panelLEDs(6,(g,r,b))
            #print('Button 5 pressed, random mode ON')
    if buttonPressed == 6:
        # Button 6 pressed, nothing happens except for LED fun
        panelLEDs(7,(0,0,0))
        for i in range(0, 8):
            panelLEDs(i,(200,200,200))
            sleep(50)
            panelLEDs(i,(0,0,0))
        sleep(1000)
        panelLEDs(7,(100,0,0))
    if buttonPressed == 7:
        # Button 7 pressed, reset
        setBeginState()
    if randomMode:
        random = randint(0, 100)
        if random == 0:
            randomSwitch = randint(1,4)
            # Random mode is flipping over switch 'randomSwitch'
            flipSwitch(randomSwitch)
    sleep(300)