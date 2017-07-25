import os, sys, inspect, thread, time
import numpy as np
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

# Detectar gestos

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    min_largo = 100.0
    min_velocidad = 10

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        controller.config.set("Gesture.Swipe.MinLength",self.min_largo);
        controller.config.set("Gesture.Swipe.MinVelocity",self.min_velocidad);
        controller.config.save();

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        previous = controller.frame(1)

        # Girar Imagen
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                pos_swipe = swipe.position
                if(pos_swipe.x > 0 and self.state_names[gesture.state] == "STATE_START" ):
                	print "Derecha a izquierda => Giro a la izquierda"
                elif(pos_swipe.x < 0 and self.state_names[gesture.state] == "STATE_START"):
                	print "Izquierda a derecha => Giro a la derecha"
                print " Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f"% (gesture.id, self.state_names[gesture.state],swipe.position, swipe.direction, swipe.speed)
                """
                if(previous):
                	for prev_gesture in previous.gestures():
                		if prev_gesture.type == Leap.Gesture.TYPE_SWIPE:
                			prev_swipe = SwipeGesture(prev_gesture)
                			prev_pos_swipe = prev_swipe.position

                diferencia = (prev_pos_swipe - pos_swipe).magnitude
                print"diferencia: %f"% diferencia
                """
                print"velocidad: %f"% swipe.speed

        
        # Redimensionar Imagen => Con las 2 imagenes

        #Zoom in y Zoom out
        #Ver si afecta delay
        if(len(frame.hands)==2 and len(previous.hands)==2):
        	for hand in frame.hands:
        		#Ver diferencias de posicion en tiempos t y t+1, si (t+1 - t).x > 0 la mano va hacia la derecha, por lo tanto estoy agrandando
        		if hand.is_left:
        			print "Mano Izquierda:",hand.palm_position
 
        		elif hand.is_right:
        			print "Mano Derecha:",hand.palm_position
        			
        		## Diferenciar con rotar imagen, velocidad
        	
        	print "Hay 2 manos!"

        
        """   
        for hand in frame.hands:
	        if(hand.is_left and hand.is_right):
	        	print "Ambas manos sobre el sensor"
	        elif(hand.is_left and not hand.is_right):
	        	print "mano izquierda sobre el sensor"
	        elif(hand.is_right and not hand.is_left):
	        	print "mano derecha sobre el sensor"
		"""


        """
	        handType = "Left hand" if hand.is_left else "Right hand"
	        posicion_palma = hand.palm_position
	        print "x:",posicion_palma.x
	        print "y:",posicion_palma.y
	        print "z:",posicion_palma.z
	        direction = hand.direction
	        
	        normal = hand.palm_normal
	        
	        
	        print "  angulo y-z: %f degrees, angulo y-x: %f degrees, angulo z-x: %f degrees" % (
	            direction.pitch * Leap.RAD_TO_DEG,
	            normal.roll * Leap.RAD_TO_DEG,
	            direction.yaw * Leap.RAD_TO_DEG)
			 
	        #print "  %s, id %d, position: %s" % (
	            #handType, hand.id, hand.palm_position)
	        
	        # Get the hand's normal vector and direction
	        normal = hand.palm_normal
	        direction = hand.direction

	        # Calculate the hand's pitch, roll, and yaw angles
	        

	        # Get arm bone
	        arm = hand.arm
	        print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
	            arm.direction,
	            arm.wrist_position,
	            arm.elbow_position)        
	    """

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()