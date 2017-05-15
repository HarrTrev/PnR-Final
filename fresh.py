from gopigo import *
import time
import logging
class Fresh:

    def __init__(self):
        #LOG_LEVEL = logging.INFO
        LOG_LEVEL = logging.DEBUG
        LOG_FILE = "/home/pi/PnR-Final/log_robot.log"
        LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
        logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)
        logging.debug("Initializing")
        print("Your piggy has been instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 90
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.STOP_DIST = 30
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 140
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 140
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        self.nav()


    def nav(self):
        logging.debug("Nav start.")
        print("\n--------------Start Nav---------------\n")
        while True:
            if self.is_clear():
                print("looks good, onwards")
                fwd()
                while self.dist() > self.STOP_DIST:
                    time.sleep(.2)
            self.stop()
            self.encB(3)
            self.restore_heading()
            answer = self.choose_path()
            if answer == "left":
                self.encL(5)
                time.sleep(.2)
            else:
                self.encR(5)
                time.sleep(.2)

    def restore_heading(self):
        logging.debug("Starting restore heading.")
        if self.turn_track > 10:
            self.encL(self.turn_track)
        elif self.turn_track < 10:
            self.encR(abs(self.turn_track))
        else:
            return "Onward, forward. Dues Vult."

    def set_speed(self, left, right):
        logging.debug("Setting Speed.")
        set_left_speed(left)
        set_right_speed(right)
        print('Left speed set to: ' + str(left) + ' // Right set to: ' + str(right))

    def encF(self, enc):
        logging.debug("Going Forward")
        print('Moving ' + str((enc / 18)) + ' rotation(s) forward')
        enc_tgt(1, 1, enc)
        fwd()
        time.sleep(1 * (enc / 18) + .4)

    def encR(self, enc):
        logging.debug("Right Turn")
        print('Moving ' + str((enc / 18)) + ' rotation(s) right')
        enc_tgt(1, 1, enc)
        right_rot()
        time.sleep(1 * (enc / 18) + .4)
        self.turn_track += enc

    def encL(self, enc):
        logging.debug("Left turn")
        print('Moving ' + str((enc / 18)) + ' rotation(s) left')
        enc_tgt(1, 1, enc)
        left_rot()
        time.sleep(1 * (enc / 18) + .4)
        self.turn_track -= enc

    def encB(self, enc):
        logging.debug("Backing up")
        print('Moving ' + str((enc / 18)) + ' rotations(s) backwards')
        enc_tgt(1, 1, enc)
        bwd()
        time.sleep(1 * (enc / 18) + .4)

    def servo(selfself, val):
        logging.debug("Moving servo")
        print('Moving servo to' + str(val) + 'deg')
        servo(val)
        time.sleep(.1)

    def dist(self):
        logging.debug("Setting distance")
        measurement = us_dist(15)
        time.sleep(.05)
        print('I see something ' + str(measurement) + "cm away")
        return measurement

    # DUMP ALL VALUES IN THE SCAN ARRAY
    def flush_scan(self):
        logging.debug("Get this scan off. Flush scan incoming.")
        self.scan = [None] * 180

    # SEARCH 120 DEGREES COUNTING BY 2's
    def wide_scan(self):
        logging.debug("Running wide scan.")
        # dump all values
        self.flush_scan()
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, +2):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            # double check the distance
            scan2 = us_dist(15)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            time.sleep(.01)
            print(x, scan1)

    def is_clear(self):
        logging.debug("is_clear, anything ahead?")
        print("Running the is_clear method.")
        for x in range((self.MIDPOINT - 15), (self.MIDPOINT + 15), 5):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            # double check the distance
            scan2 = us_dist(15)
            time.sleep(.1)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            if scan1 < self.STOP_DIST:
                print("Doesn't look clear to me")
                return False
        return True

    # DECIDE WHICH WAY TO TURN
    def choose_path(self):
        logging.debug("Choosing path.")
        print('Considering options...')
        if self.is_clear():
            return "fwd"
        else:
            self.wide_scan()
        avgRight = 0
        avgLeft = 0
        for x in range(self.MIDPOINT - 60, self.MIDPOINT):
            if self.scan[x]:
                avgRight += self.scan[x]
        avgRight /= 60
        print('The average dist on the right is ' + str(avgRight) + 'cm')
        for x in range(self.MIDPOINT, self.MIDPOINT + 60):
            if self.scan[x]:
                avgLeft += self.scan[x]
        avgLeft /= 60
        print('The average dist on the left is ' + str(avgLeft) + 'cm')
        if avgRight > avgLeft:
            return "right"
        else:
            return "left"

    def stop(self):
        logging.debug("STOPPING")
        print('All stop.')
        stop()
        servo(self.MIDPOINT)
        time.sleep(0.05)


    def calibrate(self):
        logging.debug("Calibrating.")
        print("Calibrating...")
        servo(self.MIDPOINT)
        response = raw_input("Am I looking straight ahead? (y/n): ")
        if response == 'n':
            while True:
                response = raw_input("Turn right, left, or am I done? (r/l/d): ")
                if response == "r":
                    self.MIDPOINT += 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                elif response == "l":
                    self.MIDPOINT -= 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                else:
                    print("Midpoint now saved to: " + str(self.MIDPOINT))
                    break
        response = raw_input("Do you want to check if I'm driving straight? (y/n)")
        if response == 'y':
            while True:
                set_left_speed(self.LEFT_SPEED)
                set_right_speed(self.RIGHT_SPEED)
                print("Left: " + str(self.LEFT_SPEED) + "//  Right: " + str(self.RIGHT_SPEED))
                self.encF(18)
                response = raw_input("Reduce left, reduce right or drive? (l/r/d): ")
                if response == 'l':
                    self.LEFT_SPEED -= 10
                elif response == 'r':
                    self.RIGHT_SPEED -= 10
                elif response == 'd':
                    self.encF(18)
                else:
                    break

    # PRINTS THE CURRENT STATUS OF THE ROBOT
    def status(self):
        logging.debug("printing status.")
        print("My power is at " + str(volt()) + " volts")
        print('Left speed set to: ' + str(self.LEFT_SPEED) + ' // Right set to: ' + str(self.RIGHT_SPEED))
        print('My MIDPOINT is set to: ' + str(self.MIDPOINT))
        print('I get scared when things are closer than ' + str(self.STOP_DIST) + 'cm')


try:
    f = Fresh()
except (KeyboardInterrupt, SystemExit):
    stop()
except Exception as ee:
    logging.error(ee.__str__())