#!/usr/bin/env python3
# so that script can be run from Brickman

import ev3dev.auto as ev3
from time import sleep
import random


def wait_for_motor(wait_time=.5):
    """Sleep for a specific amount of time. default is .5 second"""
    sleep(wait_time)


class Rover(object):
    def __init__(self):
        self.leftMotor = ev3.LargeMotor('outB')
        self.rightMotor = ev3.LargeMotor('outC')
        self.touchSensor = ev3.TouchSensor()
        self.speed = 600
        self.backward_speed = -600
        self.hold_stop_action = "hold"
        self.is_moving_forward = False
        self.btn = ev3.Button()
        self.lcd = ev3.Screen()
        self.ir = ev3.InfraredSensor()
        self.ir.mode = 'IR-PROX'
        self.distance = 0

    def move_forward(self):
        """Move the rover forward"""

        ev3.Sound.speak('Danger, moving forward!').wait()
        self.is_moving_forward = True
        self.leftMotor.run_forever(speed_sp=750)
        self.rightMotor.run_forever(speed_sp=750)
        wait_for_motor(.5)

    def stop(self):
        """Stop the rover"""
        self.is_moving_forward = False
        self.leftMotor.stop()
        self.rightMotor.stop()

    def move_backward(self):
        """Move the rover backward"""

        ev3.Sound.play('Backing_alert.wav').wait()
        self.leftMotor.run_timed(time_sp=1000, speed_sp=self.backward_speed)
        self.rightMotor.run_timed(time_sp=1000, speed_sp=self.backward_speed)
        self.rightMotor.wait_while('running')
        self.is_moving_forward = False

    def turn_left(self):
        """Turn the Rover Left"""
        ev3.Sound.beep()
        ev3.Sound.speak('Danger, turning left!').wait()
        self.leftMotor.run_to_rel_pos(position_sp=-620, speed_sp=self.speed, stop_action=self.hold_stop_action)
        self.leftMotor.wait_while('running')
        self.is_moving_forward = False

    def turn_right(self):
        """Turn the Rover Right"""
        ev3.Sound.beep()
        ev3.Sound.speak('Danger, turning right!').wait()
        self.rightMotor.run_to_rel_pos(position_sp=-620, speed_sp=self.speed, stop_action=self.hold_stop_action)
        self.rightMotor.wait_while('running')
        self.is_moving_forward = False

    def run(self):
        """Run the Rover until any Button is pressed"""
        while not self.btn.any():
            self.lcd.clear()
            self.distance = self.ir.value()

            # lcd.draw returns a PIL.ImageDraw handle
            self.lcd.draw.ellipse((20, 20, 60, 60))
            self.lcd.draw.ellipse((118, 20, 158, 60))

            if not self.is_moving_forward:
                # Draw a smiley face
                self.draw_smiley_face()
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)

                self.move_forward()
            if self.touchSensor.value() or self.distance < 30:
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
                # Draw a sade face
                self.draw_sade_face()

                self.stop()
                wait_for_motor(0.5)
                self.move_backward()
                wait_for_motor(0.5)

                # Randomly turn left or right
                if random.randint(0, 1) == 1:
                    self.turn_right()
                else:
                    self.turn_left()

        self.stop()

    def draw_sade_face(self):
        self.lcd.draw.arc((20, 80, 158, 100), 180, 360)

    def draw_smiley_face(self):
        self.lcd.draw.arc((20, 80, 158, 100), 0, 180)


def main():
    rover = Rover()
    rover.run()


if __name__ == '__main__':
    main()
