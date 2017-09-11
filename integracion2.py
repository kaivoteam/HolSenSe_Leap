import os, sys, inspect, thread, time
import numpy as np
import time


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
name_image = raw_input("Nombre de imagen GIF: ")
inicializar(name_image)

##------------------DATOS NECESARIOS-----------------------------
class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    min_largo = 200.0
    min_velocidad = 50
    #x_prev = 0.0
    #y_prev= 0.0
    #app_x = 0.0
    #app_y = 0.0

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

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        cont = 1
        frame = controller.frame()
        #previous = controller.frame(1)
        #previous2 = controller.frame(2)
        #previous3 = controller.frame(3)
        print "CUANTAS MANOS HAY antes del for:",len(frame.hands)
        #print "Frame id1: %d, Frame id2: %d, Frameid3: %d, Frameid4: %d" % (
              #frame.id, previous.id, previous2.id, previous3.id)
        
        """
        ZOOM ANTERIOR :

        
        for hand in previous.hands:
            manos = len(frame.hands)
            if(manos == 1):
                continue
            gesto = "zoom"
            ## 
            handType = "Left hand" if hand.is_left else "Right hand"
            # CAJA 
            interaction_box = frame.interaction_box
            #Reducir tamanno de caja de interaccion!
            app_width = 700
            app_height = 500
            i_box = frame.interaction_box
            normalized_tip = i_box.normalize_point(hand.palm_position)
            x_prev = app_width  * normalized_tip.x
            y_prev = app_height * (1 - normalized_tip.y)
            break

            
        for hand in frame.hands:
            #print "posicion palma:",hand.palm_position
            manos = len(frame.hands)
            if(manos == 1):
                continue
                #else? break?
            gesto = "zoom"
            ## 
            handType = "Left hand" if hand.is_left else "Right hand"
            # CAJA 
            interaction_box = frame.interaction_box
            #Reducir tamanno de caja de interaccion!
            app_width = 700
            app_height = 500
            i_box = frame.interaction_box
            normalized_tip = i_box.normalize_point(hand.palm_position)
            app_x = app_width  * normalized_tip.x
            app_y = app_height * (1 - normalized_tip.y)
            print "Segun el frame anterior => X es :%f, Y es: %f" % (x_prev,y_prev)
            print "Segun la caja => X es: %f , Y es: %f " % (app_x,app_y)
            
            delta_x = app_x - x_prev
            delta_y = app_y - y_prev
            print "El delta en X es: %f, en Y es: %f" % (delta_x, delta_y)
            if delta_x > 10 : #in / out
                    hacer("3",0.3)
                    print "HICISTE ZOOM IN!!"
            elif(delta_x < -20): ## CORREGIR
                    hacer("4",0.3)
                    print "HICISTE ZOOM OUT!!"
            break
            
            #Metodo anterior...
            
            #print hand.palm_velocity.x
            #print hand.palm_velocity.y           
            
            if cont==1: 
                delta_x = self.app_x - self.x_prev
                delta_y = self.app_y - self.y_prev
                print "El delta en X es: %f, en Y es: %f" % (delta_x, delta_y)
                self.x_prev=self.app_x
                self.y_prev=self.app_y
                if delta_x > 40 : #in / out
                    hacer("3",0.5,"Esta cantidad de zoom no esta permitida!")
                    print "ZOOM IN"
                elif(delta_x < -10): ## CORREGIR
                    hacer("4",0.5,"Imagen muy pequenna")
                    print "HICISTE ZOOM OUT!!"
                cont += 1
            break
            """

        for gesture in frame.gestures():
        # SWIPES!      
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                # ZOOM IN Y ZOOM OUT
                # Girar Imagen entorno a eje y -- Si detecta un swipe hace el giro en la imagen    
                print "GIRO SWIP DETECTADO!"
                swipe = SwipeGesture(gesture)
                
                #---> si swipe es en eje Y hacia abajo centrar
                if(swipe.direction.y < -0.9 and self.state_names[gesture.state] == "STATE_START"): #algo
                    hacer('-') #eso resetea
                    print "ESTOY HACIENDO RESET!"
                    print " Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f"% (gesture.id, self.state_names[gesture.state],swipe.position, swipe.direction, swipe.speed)
                    break

                if(swipe.direction.z < -0.9 and self.state_names[gesture.state] == "STATE_START"): #algo
                    hacer('3',0.3,"Mucho zoom!!") #eso resetea
                    print "ESTOY HACIENDO ZOOM IN!"
                    print " Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f"% (gesture.id, self.state_names[gesture.state],swipe.position, swipe.direction, swipe.speed)
                    break
                 
                elif(swipe.direction.z > 0.9 and self.state_names[gesture.state] == "STATE_START"): #algo
                    hacer('4',0.3,"No se ve nada!!") #eso resetea
                    print "ESTOY HACIENDO ZOOM OUT!"
                    print " Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f"% (gesture.id, self.state_names[gesture.state],swipe.position, swipe.direction, swipe.speed)
                    break

                pos_swipe = swipe.position
                v_max = 400
                #Antes era / frames
                factor_mov = swipe.speed/v_max 
                print "velocidad swipe:", swipe.speed
                print "factor de giro: ", factor_mov
                # Cantidad de frames a girar de escala 0 a 100
                if(swipe.direction.x < 0 and self.state_names[gesture.state] == "STATE_START"):
                    print "Direccion Swip : Derecha a izquierda!"
                    print "Pos_swipe:",pos_swipe
                    print " Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f"% (gesture.id, self.state_names[gesture.state],swipe.position, swipe.direction, swipe.speed)
                    hacer("2",factor_mov) 
                    break
                elif(swipe.direction.x > 0 and self.state_names[gesture.state] == "STATE_START"):
                    print "Direccion Swip : Izquierda a Derecha!"
                    print "Pos_swipe:",pos_swipe
                    print " Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f"% (gesture.id, self.state_names[gesture.state],swipe.position, swipe.direction, swipe.speed)
                    hacer("1",factor_mov) 
                    break

            # Futuro => Rotar entorno eje z
            
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                print "CIIIIIRCULOOOOOOOOO"

                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                        gesture.id, self.state_names[gesture.state],
                        circle.progress, circle.radius, 1, "hola")

                # Determine clock direction using the angle between the pointable and the circle normal
                if (self.state_names[gesture.state] == "STATE_START" and circle.radius > 50):
                    clockwiseness = "clockwise"
                    hacer("5") #rota 180 grados
                    time.sleep(0.5) 
                break
                """
                
                previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                swept_angle = 0
                clockwiseness = "hola"
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                
                """    
                
            

            """
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