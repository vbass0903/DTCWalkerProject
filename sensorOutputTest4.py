import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711
from Adafruit_LED_Backpack import SevenSegment

def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()

hx1 = HX711(5, 6)
hx2 = HX711(20, 21)
hx3 = HX711(19, 26)
hx4 = HX711(23, 24)


# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx1.set_reading_format("LSB", "MSB")
hx2.set_reading_format("LSB", "MSB")
hx3.set_reading_format("LSB", "MSB")
hx4.set_reading_format("LSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
hx1.set_reference_unit(40000)
hx2.set_reference_unit(19000)
hx3.set_reference_unit(44000)
hx4.set_reference_unit(22000)

hx1.reset()
hx1.tare()
hx2.reset()
hx2.tare()
hx3.reset()
hx3.tare()
hx4.reset()
hx4.tare()

#
# Start of Output Display
#
 
# Create display instance on default I2C address (0x70) and bus number.
display = SevenSegment.SevenSegment()

# Alternatively, create a display with a specific I2C address and/or bus.
# display = SevenSegment.SevenSegment(address=0x74, busnum=1)

# Initialize the display. Must be called once before using the display.
display.begin()
colon = False

# Clear the display buffer.
display.clear()
display.set_colon(colon)

i = 0
while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment the three lines to see what it prints.
        #np_arr8_string = hx.get_np_arr8_string()
        #binary_string = hx.get_binary_string()
        #print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val1 = hx1.get_weight(1)
        val2 = hx2.get_weight(1)
        val3 = hx3.get_weight(1)
        val4 = hx4.get_weight(1)

        sumVal = (val1 + val2 + val3 + val4)

        # No decimal digits and left justified
        display.print_float(sumVal, decimal_digits=0, justify_right=False)
        # Actually updates the LEDs
        display.write_display()
        
        #
        # End of Output Display
        #

        i = i + 1
        if i = 50:
            hx1.power_down()
            hx1.power_up()
            hx2.power_down()
            hx2.power_up()
            hx3.power_down()
            hx3.power_up()
            hx4.power_down()
            hx4.power_up()
            i = 0
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
