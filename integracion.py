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
        previous = controller.frame(1)
        previous2 = controller.frame(2)
        previous3 = controller.frame(3)
        previous4 = controller.frame(4)
        
        if len(frame.hands) == 2:
            left= 0
            right=0
            for hand in previous.hands:
                manos = len(frame.hands)
                if(manos == 1):
                    continue
                gesto = "zoom"
                ## 
                handTypeP = "Left hand" if hand.is_left else "Right hand"
                # CAJA 
                interaction_box = frame.interaction_box
                #Reducir tamanno de caja de interaccion!
                app_width = 700
                app_height = 500
                i_box = frame.interaction_box
                normalized_tip = i_box.normalize_point(hand.palm_position)
                x_prev = app_width  * normalized_tip.x                
                y_prev = app_height * (1 - normalized_tip.y)
                for hand in frame.hands:
                    gesto = "zoom"
                    ## 
                    handType = "Left hand" if hand.is_left else "Right hand"
                    if handType==handTypeP:                        
                        # CAJA 
                        interaction_box = frame.interaction_box
                        i_box = frame.interaction_box
                        normalized_tip = i_box.normalize_point(hand.palm_position)
                        app_x = app_width  * normalized_tip.x
                        delta_x = app_x - x_prev   
                        if handType== "Left hand":
                            left=delta_x
                        else:
                            right=delta_x                         
                    

            print "ESTOY VIENDO %d MANOS FRENTE AL LEAP " % len(frame.hands)
            if (left < -10 and right > 10) : 
                hacer("3",0.2)
                print "HICISTE ZOOM IN!!"
            elif(left > 10 and right < -10): 
                hacer("4",0.2)
                print "HICISTE ZOOM OUT!!"                     
        else:
        
            lista_gesturetypes = [gesture.type for gesture in frame.gestures()]

            #for gesture in frame.gestures():
            if Leap.Gesture.TYPE_CIRCLE in lista_gesturetypes:#gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                print "Circulo CON %d manos" % len(frame.hands)
                # Determine clock direction using the angle between the pointable and the circle normal
                if (self.state_names[gesture.state] == "STATE_START"):# and circle.radius < 50):
                    #clockwiseness = "clockwise"
                    hacer("5") #rota 180 grados
            
            # SWIPES!      
            elif Leap.Gesture.TYPE_SWIPE in lista_gesturetypes:  #gesture.type == Leap.Gesture.TYPE_SWIPE:
                # Girar Imagen entorno a eje y -- Si detecta un swipe hace el giro en la imagen    
                print "SWIP DETECTADO! CON %d MANOS " %  len(frame.hands)
                swipe = SwipeGesture(gesture)
                for hand in previous.hands:                
                    # CAJA 
                    interaction_box = frame.interaction_box
                    app_width = 700
                    app_height = 500
                    app_depth = 500
                    i_box = frame.interaction_box
                    normalized_tip = i_box.normalize_point(hand.palm_position)
                    x_prev = app_width  * normalized_tip.x                
                    y_prev = app_height * (1 - normalized_tip.y)
                    z_prev = app_depth * normalized_tip.z
                    for hand in frame.hands:
                            interaction_box = frame.interaction_box
                            i_box = frame.interaction_box
                            normalized_tip = i_box.normalize_point(hand.palm_position)                           
                            app_x = app_width  * normalized_tip.x
                            app_y = app_height * (1 - normalized_tip.y)
                            app_z = app_depth * normalized_tip.z
                            delta_x = app_x - x_prev
                            delta_y = app_y - y_prev
                            delta_z = app_z - z_prev   
                print "delta z: ",delta_z
                print "delta_y es ", delta_y
                print "delta x ee ", delta_x
                #---> si swipe es en eje Y hacia abajo centrar
                if(delta_y  > 12 and np.abs(delta_x) < 7 and np.abs(delta_z) <7 and self.state_names[gesture.state] == "STATE_START"): #algo
                    hacer('7') #eso resetea
                    print "ESTOY CENTRANDO!"
                    return

                elif(swipe.direction.z < 0.9 and np.abs(delta_x)<7 and np.abs(delta_y)<7 and self.state_names[gesture.state] == "STATE_START"): #algo
                    hacer('3',0.2) #eso resetea
                    print "ESTOY HACIENDO ZOOM IN!"
                    return
                 
                elif(swipe.direction.z > -0.9 and np.abs(delta_x)<7 and np.abs(delta_y)<7 and self.state_names[gesture.state] == "STATE_START"): #algo
                    hacer('4',0.2) #eso resetea
                    print "ESTOY HACIENDO ZOOM OUT!"
                    return
                

                pos_swipe = swipe.position
                v_max = 400
                #Antes era / frames
                factor_mov = swipe.speed/v_max 

                # Cantidad de frames a girar de escala 0 a 100
                print swipe.direction.x
                if( swipe.direction.x < 0 and np.abs(delta_y) < 10 and np.abs(delta_z) <10 and self.state_names[gesture.state] == "STATE_START"):
           #         print "Direccion Swip : Derecha a izquierda!"
                    hacer("2",factor_mov) #revisar la direccion de esto
                    print "Muevo de derecha a izquierda"
                elif(swipe.direction.x > 0 and np.abs(delta_y) < 10 and np.abs(delta_z) <10  and self.state_names[gesture.state] == "STATE_START"):
            #        print "Direccion Swip : Izquierda a Derecha!"
            #        print "Pos_swipe:",pos_swipe
                    hacer("1",factor_mov)  #revisar la direccion de esto
                    print "Muevo de izquierda a derecha"
                else:
                    print "NO FUE NADA"
                
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
