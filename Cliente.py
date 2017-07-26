import socket
import sys
import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, lib_dir)
import Leap
import thread
import time
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
 
# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
#Conecta el socket al puerto 
server_address = ('localhost', 10000)

print >> sys.stderr, 'conectando a %s puerto %s' % server_address
sock.connect(server_address)

clock_inicial = "lala"

class SampleListener(Leap.Listener):
    clockwiseness = "lala"
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        
    
        image_list = frame.images
        left_image = image_list[0]
        right_image = image_list[1]        
        
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            #print "  %s, id %d, posicion palma: %s" % (
            #    handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            #print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
            #    direction.pitch * Leap.RAD_TO_DEG,
            #    normal.roll * Leap.RAD_TO_DEG,
            #    direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            arm = hand.arm
        #    print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
               # arm.direction,
               # arm.wrist_position,
               # arm.elbow_position)

            # Get fingers
            for finger in hand.fingers:
                #print "FINGER"
                #determina la caja de interaccion de la mano...hay ue darle un poco mas pues el campo
                #de vision es un poco mayor que  400 X 600 
                interaction_box = frame.interaction_box
                app_width = 700
                app_height = 500
                i_box = frame.interaction_box
                normalized_tip = i_box.normalize_point(finger.tip_position)
                app_x = app_width  * normalized_tip.x
                app_y = app_height * (1 - normalized_tip.y)
               # print " %f app_x, %f app_y ... " % (app_x, app_y)
               # print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                #    self.finger_names[finger.type],
                 #   finger.id,
                  #  finger.length,
                   # finger.width)

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
          #          print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                    #    self.bone_names[bone.type],
                     #   bone.prev_joint,
                      #  bone.next_joint,
                      #  bone.direction)

        # Get tools
        #for tool in frame.tools:

            #print "  Tool id: %d, position: %s, direction: %s" % (
            #    tool.id, tool.tip_position, tool.direction)

        for gesture in frame.gestures():
            #clockwiseness = "lala"
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                print "HAGO UN CIRCULO"
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"
                
                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                #print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                #        gesture.id, self.state_names[gesture.state],
                #        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                #print "HAGO SWIPE!"
                swipe = SwipeGesture(gesture)
                #print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                #        gesture.id, self.state_names[gesture.state],
                #        swipe.position, swipe.direction, swipe.speed)

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                #print "HICE KEYTAP"
                keytap = KeyTapGesture(gesture)
                #print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                #        gesture.id, self.state_names[gesture.state],
                #        keytap.position, keytap.direction )

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                #print "SCREENT}AP!!!!!!"
                screentap = ScreenTapGesture(gesture)
                #print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
                #        gesture.id, self.state_names[gesture.state],
                #        screentap.position, screentap.direction )

        
            cosa = "clock clock "
            global clock_inicial
            clock_inicial = clockwiseness
            print clock_inicial
        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""
        
            
    def nuevo_clock(self):
        print "NO SOY LALA o si?"
        print clock_inicial
        print "pase "

        algo()
        
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
def algo():
    clock_inicial="hola"
    
def main():
    # Create a sample listener and controller
    #clockwiseness = "lala"
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    #print "Press Enter to quit..."
    
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

    try:

        #print listener.nuevo_clock()
        # Enviando datos
        print clock_inicial 
        #message = clockwiseness
        print >>sys.stderr, 'enviando "%s"' % clock_inicial
        sock.sendall(clock_inicial)
     
        # Buscando respuesta
        amount_received = 0
        amount_expected = len(clock_inicial)
         
        while amount_received < amount_expected:
            data = sock.recv(1024)
            amount_received += len(data)
            print >>sys.stderr, 'recibiendo "%s"' % data

    finally:
        print >>sys.stderr, 'cerrando socket'
        sock.close()




if __name__ == "__main__":
    #clockwiseness= "lala"
    main()

