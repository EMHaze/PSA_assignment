import board
import digitalio
import time
import time, board, pwmio

notes = [n * 2 for n in [330, 330]]
tone = pwmio.PWMOut(board.GP15, variable_frequency=True)
tone_duration = 0.2
rest_duration = 0.2

# Configure which GPIO pin the leds are connected to
r_led = digitalio.DigitalInOut(board.GP16)
b_led = digitalio.DigitalInOut(board.GP15)
g_led = digitalio.DigitalInOut(board.GP14)
# Configure the leds as outputs
r_led.direction = digitalio.Direction.OUTPUT
b_led.direction = digitalio.Direction.OUTPUT
g_led.direction = digitalio.Direction.OUTPUT

# PEOPLE BUTTON
people_button = digitalio.DigitalInOut(board.GP26)
people_button.direction = digitalio.Direction.INPUT
people_button.pull = digitalio.Pull.UP # Set internal pull-up resistor -> this makes it an active low, so it has to be reversed when used
# How pullUP works:
    # hold at 3.3V until pressed -> 3.3 = TRUE
    # drop to 0V when pressed -> 0 = FALSE
    # THIS is active low logic

#PLANT BUTTON
plant_button = digitalio.DigitalInOut(board.GP22)
plant_button.direction = digitalio.Direction.INPUT
plant_button.pull = digitalio.Pull.UP 

# On startup, mode is set to None so that none of the lights are on
mode = None

# Buzzer functions 
def play(freq, dur): #controls what sound the buzzer makes 
    tone.frequency = freq
    time.sleep(dur)
    return


def beep(notes): # when called allows the buzzer to sound 
    for n in notes:
            tone.duty_cycle = 32768
            play(n, tone_duration)
        
            tone.duty_cycle = 0
            time.sleep(rest_duration)
    return 
        
# Flags for previous state of the BUTTON 
prev_plant = True # Why are these true and not false? -> because we're using pull UP!!
prev_people = True #True = 0V -> LEDs off

while True:
    cur_people = people_button.value
    cur_plant = plant_button.value

    if prev_people and not cur_people: # if state was people and people WAS pressed, <- tis is where the pull-up thing comes in
        if mode == "people":
            mode = None
            beep(notes)
        else:
            mode = "people"
            beep(notes)
# HERE, WHY CARE IF PREV_PLANT? -> to track BUTTON state: mode tracks led state but not button state. 
# this code cycles through 20 times a second, and we want the button to remember its state until we change it
    if prev_plant and not cur_plant: # if state was plant, and plant is pressed again
        if mode == "plant": # if the current mode is plant, make it None
            mode = None
            beep(notes)
        else: # if the current mode in None, make it plant
            mode = "plant"
            beep(notes)
    if cur_people and cur_plant: 
        continue 


    '''
    if plant button pressed:
        if mode = plant already (if last_pressed_button = plant # if plant is already on)
            mode = None
        else:
            mode = plant # was not plant last pressed, so make it plant
    '''

# start from all of them being false. either mode makes something turn ON
    r_led.value = False
    b_led.value = False
    g_led.value = False


    if mode == "plant":
        r_led.value = True
        b_led.value = True
        # g_led.value REMAINS false
    elif mode == "people":
        r_led.value = True
        b_led.value = True
        g_led.value = True
    # update previous states
    prev_people = cur_people 
    prev_plant = cur_plant 
    
    time.sleep(0.05) 
    # ^ whats the point of a sleep if the led keeps glowing until toggled? -> the code HAS to repeat several times a second. 
    # sleep allows me to control how many times it repeats, and 0.05 accounts to 20 times a second, a decent amount considering debugging and power consumption. 
