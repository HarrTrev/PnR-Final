import pigo
import time
import random

'''
MR. A's Final Project Student Helper
'''

class GoPiggy(pigo.Pigo):

    ########################
    ### CONTSTRUCTOR - this special method auto-runs when we instantiate a class
    #### (your constructor lasted about 9 months)
    ########################

    def __init__(self):
        print("Your piggy has been instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 90
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.STOP_DIST = 30
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 125
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 125
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()


    ########################
    ### CLASS METHODS - these are the actions that your object can run
    #### (they can take parameters can return stuff to you, too)
    #### (they all take self as a param because they're not static methods)
    ########################


    ##### DISPLAY THE MENU, CALL METHODS BASED ON RESPONSE
    def menu(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "w": ("Sweep", self.sweep),
                "o": ("Count obstacles", self.count_obstacles),
                "a": ("Count all objects", self.count_all_obstacles),
                "s": ("Check status", self.status),
                "q": ("Quit", quit),
                "t": ("Test", self.test)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()



    def count_obstacles(self):
        #run a scan
        self.wide_scan()
        #count the objects
        counter = 0
        #starting state assumes no objects
        found_something = False
        #loop through all my scan data
        for x in self.scan:
            # if x is not None and close
            if x and x <= self.STOP_DIST:
                # if I've already found something
                if found_something:
                    print("Object part 7 cont.")
                # if this is a new object
                else:
                    #switch my tracker
                    found_something = True
                    print("Starting Object")
            #if data = safe
            if x and x > self.STOP_DIST:
                #Tracker triggered
                if found_something:
                    print("rip object")
                    #reset tracker
                    found_something = False
                    #increase counter
                    counter += 1
        print('Total number of obstacles in this scan: ' + str(counter))
        return counter

    def count_all_obstacles(self):
        big_counter = 0
        big_counter += self.count_obstacles()
        for x in range(4):
            self.encR(9)
            big_counter += self.count_obstacles()
        print('Total obstacles: ' + str(big_counter))
        return big_counter

    def turn_test(self):
        while True:
            ans = raw_input('Turn right, left or stop? (r/l/s): ')
            if ans == 'r':
                val = int(raw_input('/nBy how much?: '))
                self.encR(val)
            elif ans == 'l':
                val = int(raw_input('/nBy how much?: '))
                self.encL(val)
            else:
                break
            self.restore_heading()

    def safety_dance(self):
        for y in range(3):
            for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, 2):
                self.servo(x)
                if self.dist() < 30:
                    print("m&m's are alright")
                    return
            self.encR(8)
        print("skittles are ok")
        self.dance()

    def sweep(self):
        for x in range(self.MIDPOINT-60, self.MIDPOINT + 60, 2):
            self.servo(x)
            self.scan[x] = self.dist()
        print("Here's what I saw:")
        print(self.scan)



    #YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE
        self.chacha()
        self.sprinkler()
        self.spin()
        self.burn_out()


    def burn_out(self):
        self.set_speed(250,250)
        self.encF(15)
        self.encR(20)

    def spin(self):
        self.encR(100)
        time.sleep(.3)
        self.encL(100)


    def sprinkler(self):
        for x in range(160, 20, -20):
            self.servo(x)
            time.sleep(.4)
        self.servo(160)





    def chacha(self):
        for x in range(2):
            self.set_speed(100, 140)
            self.encB(6)
            time.sleep(.1)
            self.set_speed(150,100)
            self.encB(6)
            time.sleep(.1)
            self.set_speed(100, 150)
            self.encF(6)
            time.sleep(.1)
            self.set_speed(140, 100)
            self.encF(6)
            time.sleep(.1)



    ########################
    ### MAIN LOGIC LOOP - the core algorithm of my navigation
    ### (kind of a big deal)
    ########################
    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("[ Press CTRL + C to stop me, then run stop.py ]\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # this is the loop part of the "main logic loop"
        while True:
            if self.is_clear():
                self.cruise()
            answer = self.choose_path()
            if answer == "left":
                self.encL(6)
            elif answer == "right":
                self.encR(6)

    def cruise(self):
        self.fwd()  # I added this to pigo
        while self.is_clear():
            time.sleep(.1)
        self.stop()
        self.encB(3)

    def test(self):
        answer = raw_input("Run? (y/n)")
        if answer == 'y':
            self.encF(2)
        elif answer == 'yes':
            self.encF(4)
        else:
            return

####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy

g = GoPiggy()
