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

movimiento = "lalainicio"
gesto= "vacio"

x_prev = 0.0

y_prev= 0.0

conta=1
# global test
test=0
sentido = "none"
velocidad = 0.0
washu = 0
mov = 0.0
angulo = 0.0


class SampleListener(Leap.Listener):
    mov = 0.0
    
    movimiento = "lala"
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
        cont=1
                
        # Get the most recent frame and report some basic information
        frame = controller.frame()   
        image_list = frame.images
        left_image = image_list[0]
        right_image = image_list[1]
        
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                gesto= "circle"
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise" 
                sentido = clockwiseness
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI
                    var = swept_angle * Leap.RAD_TO_DEG
                #print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                #        gesture.id, self.state_names[gesture.state],
                #        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)
                angulo = swept_angle * Leap.RAD_TO_DEG
                velocidad = circle.radius
                

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                print "se que x_prev es %f y que y_prev original macro es %f" %(x_prev, y_prev) 
                x_antes= x_prev
                y_antes = y_prev
                global x_prev, y_prev
                gesto = "zoom"
                swipe = SwipeGesture(gesture)
                velocidad = swipe.speed
                print velocidad
                #sentido = swipe.direction
                
                for hand in frame.hands:
                    if len(frame.hands)==2:                    
                        handType = "Left hand" if hand.is_left else "Right hand"
                        # CAJA 
                        interaction_box = frame.interaction_box
                        app_width = 700
                        app_height = 500
                        i_box = frame.interaction_box
                        normalized_tip = i_box.normalize_point(hand.palm_position)
                        app_x = app_width  * normalized_tip.x
                        app_y = app_height * (1 - normalized_tip.y)
                        print "X es: %f , Y es: %f " % (app_x, app_y )
                        print hand.palm_velocity.x
                        print hand.palm_velocity.y
                                               
                        if cont==1:
                           
                            delta_x = app_x - x_antes
                            delta_y = app_y - y_antes
                            print "el cambio en X es: %f, en Y es: %f" % (delta_x, delta_y)
                            
                            x_prev=app_x
                            y_prev=app_y
                            if delta_x >0: #in / out
                                sentido = "out"
                            else:
                                sentido = "in"
                            
                        else:
                            mov_x=app_x
                            mov_y=app_y
                        cont+=1
           
            global movimiento, gesto, velocidad, sentido, testt
             
            #aqui el +sentido
            movimiento = gesto+"---"+sentido+"---"+str(velocidad)
            
            print movimiento
        if not (frame.hands.is_empty and frame.gestures().is_empty):
            y=0
        
            
    def nuevo_clock(self):
        print "NO SOY LALA o si?"
        print movimiento
        print "pase nuevo_clock"

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
    movimiento="hola de algo"
    
def main():
    
    listener = SampleListener()
    controller = Leap.Controller()
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

        print movimiento 
        print >>sys.stderr, 'el mensaje a enviar es: "%s"' % movimiento
        sock.sendall(movimiento)
     
        # Buscando respuesta
        amount_received = 0
        amount_expected = len(movimiento)
         
        while amount_received < amount_expected:
            data = sock.recv(1024)
            amount_received += len(data)
            print >>sys.stderr, 'recibiendo el mensaje: "%s"' % data

    finally:
        print >>sys.stderr, 'cerrando socket'
        sock.close()

if __name__ == "__main__":
    main()

