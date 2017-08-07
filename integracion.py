import os, sys, inspect, thread, time
import numpy as np

# Path para importar libreria Leap //Windows and Linux
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

# Librerias/Modulos relacionadas a Imagenes
from PIL import Image, ImageFile, ImageChops,ImageOps

# Librerias/Modulos relacionados a LP
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

# Transformaciones a imagenes de archivo imports_imagenes.py
from imports_imagenes import *

##------------------DATOS NECESARIOS-----------------------------
##esto vendria definido de antemano (variables globales)

#4 imagenes en 4 angulos
angulos = [0.0, 90.0, 180.0, 270.0]

name_image = raw_input("Nombre de imagen GIF: ")

#Asumiendo que estan en la misma carpeta
im = Image.open("./imagenes/"+name_image+".gif")
print(im.format, im.size, im.mode)

frames = cantidad_frames(im)+1 #asumiendo que los frames da vuelta 360
print "La imagen tiene %d frames"%(frames)
##------------------DATOS NECESARIOS-----------------------------

#Movimiento de la imagen a traves de actual
#current = 0
#zoom = 1.0

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    min_largo = 200.0
    min_velocidad = 50
    current = 0
    zoom = 1.0

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Habilitar movimientos
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

    def on_frame(self, controller,current=0,zoom=1.0):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        previous = controller.frame(1)
        previous2 = controller.frame(2)
        previous3 = controller.frame(3)
        #print "Frame id1: %d, Frame id2: %d, Frameid3: %d, Frameid4: %d" % (
              #frame.id, previous.id, previous2.id, previous3.id)

        for hand in frame.hands:
            normal = hand.palm_normal
            direction = hand.direction
            posicion_palma = hand.palm_position
            print "posicion palma:",hand.palm_position
            print" palma: %f,%f , direccion: %f,%f"%(normal.x,normal.y,direction.x,direction.y)
            #print(previous.hands[0].normal,previous.hands[0].direction)
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
                
               
        # Girar Imagen entorno a eje y -- Si detecta un swipe hace el giro en la imagen
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                print "SWIP DETECTADO!"
                swipe = SwipeGesture(gesture)
                pos_swipe = swipe.position
                speed_swipe = swipe.speed/10
                # Cantidad de frames a girar, es proporcional a la velocidad de swipe
                if(swipe.direction.x < 0 and self.state_names[gesture.state] == "STATE_START"):
                    print "Direccion Swip : Derecha a izquierda!"
                    print "Pos_swipe:",pos_swipe
                    self.current += int(speed_swipe %frames)
                    #hacer(im, frames, angulos,current,zoom) <- Si se utiliza zoom
                    hacer(im,frames,self.current)
                elif(swipe.direction.x > 0 and self.state_names[gesture.state] == "STATE_START"):
                    print "Direccion Swip : Izquierda a Derecha!"
                    print "Pos_swipe:",pos_swipe
                    self.current -= int(speed_swipe %frames)
                    #hacer(im, frames, angulos,current,zoom) <- Si se utiliza zoom
                    hacer(im,frames,self.current)
                #print " Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f"% (gesture.id, self.state_names[gesture.state],swipe.position, swipe.direction, swipe.speed)
                print "Swipe direction:",swipe.direction.x
                break
        
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
            	print "Hice un KEY TAP!!"
                keytap = KeyTapGesture(gesture)
                #hacer(im, frames, angulos,current,zoom)
                hacer(im,frames,self.current)
                break

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)
                print "Hice un SCREEN TAP!!"
                print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        screentap.position, screentap.direction )
                break

            # Futuro => Rotar entorno eje z     
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                print "HICE UN CIRCULO!"
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

                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                        gesture.id, self.state_names[gesture.state],
                        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)
                hacer(im,frames,self.current)
                break
        
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