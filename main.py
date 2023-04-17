# main.py -- put your code here!
# EPITA / Majeure Sante / IoT

import machine
import ssd1306
import time
from pyb import Pin, ADC, Timer
import framebuf
import sys
import random
# I2C
# PB8 I2C1_SCL
# PB9 I2C1_SDA
i2c = machine.SoftI2C(scl=machine.Pin('B8'), sda=machine.Pin('B9'))

# Display
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# RTC
rtc = machine.RTC()
rtc.datetime((2023, 2, 2, 2, 21, 18, 00, 0))
print(rtc.datetime())

p = Pin('A7') # A7 has TIM1, CH1
tim = Timer(1, freq=1)
ch = tim.channel(1, Timer.PWM, pin=p)
ch.pulse_width_percent(0)

def led_off_on():
    while(1):
        pyb.LED(1).on()
        time.sleep(1)
        pyb.LED(1).off()
        time.sleep(1)


# ADC 
Pin(Pin.cpu.A1, mode=Pin.IN)
def lecture():
    #gotta set this up
    time.sleep(3)

    #Values start at 3000 / for some 3700 or 4000
    maxi = 0
    mini = 3000

    bpm = 0
    value = 0
    #best to compare to previous, so that we never stray too far
    previous = 0
    up = 0
    iteration = 0
    counter = 0
    while(counter < 6):
        #need to reset matrix
        oled.fill(0)

        #if it ran once, update
        if(iteration!=0):
            oled.text(str((bpm*40)//(9*iteration)), 100, 50)

        #hour() code reused
        now = rtc.datetime()
        oled.text("%02i/%02i" % (now[2], now[1]), 0, 50)
        oled.text("%02i:%02i" % (now[4], now[5]), 50, 50)


        
        for i in range(128):
            partition = ((maxi-mini)//40) + 1
            now = rtc.datetime()

	        # get the previous value for the bpm
            if(value!=0):
                previous = value
                    
            value = 0 # Take the average value of 20 values
            for j in range(20):
                value += ADC("A1").read()
            value = value//20

	        # Detect if there is 
            if(previous < value):
                up+=1
            else:
                up = 0
            if(up==2):
                bpm+=1
                up = 0

            # Update the value of mini and maxi if necessary
            mini = min(mini, value)
            maxi = max(maxi, value)

            # Display the value
            pix = (value - mini)//partition
            oled.pixel(i, pix, 1)
            oled.show()

        #we measured one cycle
        iteration+=1

        print(str((bpm*40)//(9*iteration)))
        counter += 1


def hour():
    counter = 0
    while(counter < 100):
        now = rtc.datetime()
        oled.fill(0)
        oled.text("%02i/%02i/%04i" % (now[2], now[1], now[0]), 0, 0)
        oled.text("%02i:%02i:%02i" % (now[4], now[5], now[6]), 0, 10)
        oled.text(str(ADC("A1").read()), 0, 20)
        oled.show()
        print(now, ':', ADC("A1").read())
        time.sleep(0.01)
        counter+= 1

def intro(lvl, timer, beginning):
    if (beginning):
        oled.fill(0)
        oled.text("Poggers Reaction", 0, 0)
        oled.text("The Game", 10, 10)

        oled.show()
        oled.fill(0)

        time.sleep(2.5)
        oled.text("GO = hit ENTER", 0, 0)
        oled.show()
        oled.fill(0)
        time.sleep(2.5)

    oled.text(lvl, 0, 0)
    oled.show()
    oled.fill(0)

    time.sleep(1.7)
    oled.text("Ready? Set...", 20, 20)
    oled.show()
    time.sleep(timer)

    oled.fill(0)

def level(lvl, lose_msg, min_score):
    completed = False
    while (not completed):
        if (lvl <= 4):
            rand_pos_1 = 0
        else :
            rand_pos_1 = random.randrange(0, 60)

        rand_pos_2 = random.randrange(10, 15)
        rand_pos_3 = random.randrange(7, 25)
        rand_trap = random.randrange(0, 10)

        seconds = time.time_ns()
        oled.fill(0)

        if (lvl == 4) :
            while (rand_trap != 1):
                rand_trap = random.randrange(0, 3)
                oled.text("TRAP", rand_pos_1, rand_pos_1)
                oled.show()
                oled.fill(0)
                time.sleep(0.3)
                oled.fill(0)
                
        seconds = time.time_ns()


        oled.text("GO", rand_pos_1, rand_pos_1)
        if (lvl <= 1):
            oled.text("GO", rand_pos_2, rand_pos_2)
        if (lvl <= 2):
            oled.text("GO", rand_pos_3, rand_pos_3)
        
        oled.show()

        answer = sys.stdin.read(1)

        if answer == "\n":
            end = (time.time_ns() - 20 - seconds)/ 1000000000 #time it would take to show GO on screen
            if (end > min_score):
                oled.fill(0)
                oled.text("%02f Seconds" % (end) ,0, 0)
                oled.show()
                time.sleep(1.3)
                oled.fill(0)
                oled.text(lose_msg, 0 , 0)
                oled.text("Try Again", 0 , 20)
                oled.text("kekw slowpoke", 0 , 40)
                oled.show()
                oled.fill(0)
                completed = False
                time.sleep(1.5)
                

            else :
                oled.fill(0)
                oled.text("%02f Seconds" % (end) ,0, 0)
                oled.show()
                time.sleep(1.5)
                oled.fill(0)
                completed = True
    

def pure_reflex():
    intro("slowpoke", 1.5, True)
    level(1, "Bozo", 2)
    intro("meh", 1.5, False)
    level(2, "Damn", 1.5)
    intro("average", 1, False)
    level(2, "close", 1)
    intro("nice", 0.8, False)
    level(3, "too bad", 0.8)
    intro("gucci", 0.6, False)
    level(3, "aight np", 0.6)
    intro("Devil!", 0.45, False)
    level(4, "You Died", 0.5)
    intro("Dante Must Die!", 0.3, False)
    level(4, "aww man!!", 0.4)
    intro("VERGIL /!\\", 0.2, False)
    level(4, "son of sparda", 0.26)

    oled.fill(0)
    oled.text("Input Code" ,0, 0)
    oled.show()
    oled.fill(0)
    time.sleep(1)
    konami_code = sys.stdin.readline()

    if (konami_code == "wwssdadaba\n"):
        oled.fill(0)
        oled.text("UNLOCKED" ,0, 0)
        oled.show()
        oled.fill(0)
        time.sleep(1)
        intro("ULTRAKILL", 0.1, False)
        level(4, "PRIME SYSPHUS", 0.2)
        intro("GOD???", 0.01, False)
        level(4, "cheater still lost", 0.1)
        oled.fill(0)
        oled.text("Cheating" ,0, 0)
        oled.show()
        oled.fill(0)


def rand_string(length, timer):
    direction = ["A", "W", "D" ,"S"]
    res = ""
    for i in range(length):
        res += (direction[random.randrange(0, 4)])
    oled.fill(0)
    oled.text(res ,0, 0)
    oled.show()
    oled.fill(0)
    time.sleep(timer)
    
    oled.text("Got it" ,0, 0)
    oled.text("Memorized ?" ,0, 10)
    oled.show()
    oled.fill(0)
    time.sleep(1)

    return res

def check_correct_input(length, result):
    oled.text("Input Sequence" ,0, 0)
    oled.show()
    oled.fill(0)
    
    correct = True

    seconds = time.time_ns()


    answer = sys.stdin.read(length)
    for i in range(len(answer)):
        if answer[i] != result[i]:
            oled.fill(0)
            oled.text("WRONG!", 0, 0)
            oled.text("It was :",0, 10)
            oled.text(result,0, 20)
            oled.text("Yours was :",0, 40)
            oled.text(answer,0, 50)
            oled.show()
            oled.fill(0)
            time.sleep(1.7)
            correct = False

    if (correct):
        end = (time.time_ns() - 20 - seconds)/ 1000000000
        oled.fill(0)
        oled.text("CORRECT!", 0, 0)
        oled.text("TIME", 0, 10)
        oled.text("%02f s" % (end) ,40, 10)
        oled.show()
        oled.fill(0)
        time.sleep(1.7)



def memory_intro(beginning, lvl):
    if (beginning):
        oled.fill(0)
        oled.text("Memory Test", 0, 0)
        oled.text("The Game", 10, 10)

        oled.show()
        oled.fill(0)

        time.sleep(2.5)
        oled.text("Left=A", 0, 20)
        oled.text("Right=D", 70, 20)
        oled.text("Up=W", 30, 0 )
        oled.text("Down=S", 30, 40)
        oled.text("CAPS LOCK ON", 0, 50)

        oled.show()
        oled.fill(0)
        time.sleep(4)

    oled.text(lvl, 0, 0)
    oled.show()
    oled.fill(0)

    time.sleep(1.7)
    oled.text("Ready? Set...", 20, 20)
    oled.show()
    oled.fill(0)
    time.sleep(1.7)




def memory():
    memory_intro(True, "Lv 1")
    check_correct_input(3,rand_string(3, 2.7))

    memory_intro(False, "Lv 2")
    check_correct_input(4,rand_string(4, 2.7))

    memory_intro(False, "Lv 3")
    check_correct_input(6,rand_string(6, 2.7))

    memory_intro(False, "Lv 4")
    check_correct_input(8,rand_string(8, 2.4))

    memory_intro(False, "Lv Final")
    check_correct_input(10,rand_string(10, 2))

    oled.fill(0)
    oled.text("Input Code" ,0, 0)
    oled.show()
    oled.fill(0)
    time.sleep(0.7)
    konami_code = sys.stdin.readline()

    if (konami_code == "wwssdadaba\n"):
        oled.fill(0)
        oled.text("UNLOCKED" ,0, 0)
        oled.show()
        oled.fill(0)
        time.sleep(1)
        memory_intro(False, "Lv Dark Souls")
        check_correct_input(10,rand_string(10, 1.5))
        memory_intro(False, "Lv Cheater")
        check_correct_input(10,rand_string(10, 1))
        oled.fill(0)
        oled.text("Cheating" ,0, 0)
        oled.show()
        oled.fill(0)

def g():
    oled.fill(0)
    oled.text("Launcher :" ,0, 0)
    oled.text("1 : React Game" ,0, 10)
    oled.text("2 : Memory Game" ,0, 20)
    oled.text("3 : BPM" ,0, 30)
    oled.text("4 : Time" ,0,40)
    oled.show()
    oled.fill(0)
    time.sleep(1)
    code = sys.stdin.readline()
    if (code == "1\n"):
        pure_reflex()
        g()
    elif (code == "2\n"):
        memory()
        g()
    elif (code == "3\n"):
        lecture()
        g()
    elif (code == "4\n"):
        hour()
        g()
    else:
        oled.text("Input Error" ,0,0)
        oled.show()
        oled.fill(0)
        time.sleep(1)
        g()
