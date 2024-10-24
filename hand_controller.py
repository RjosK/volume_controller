import cv2
import mediapipe as mp
import math
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


source = 0 # webcam| rtsp_url | video file as input
cap = cv2.VideoCapture(source) # Then start the webcam

mpmanos = mp.solutions.hands

manos = mpmanos.Hands(static_image_mode = False, 
                      max_num_hands =2, 
                      min_detection_confidence = 0.9, 
                      min_tracking_confidence = 0.8)

mpDibujar = mp.solutions.drawing_utils
cambiar = 0


#----------------------------------------------------------------- 
# Obtener los dispositivos de audio
dispositivos = AudioUtilities.GetSpeakers()
# Activar la interfaz de control de volumen
interfaz = dispositivos.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# Obtener la interfaz de control de volumen
volumen = interfaz.QueryInterface(IAudioEndpointVolume)
# Obtener el rango de volumen
RangoVol = volumen.GetVolumeRange()
VolMin = RangoVol[0]
VolMax = RangoVol[1]
# Variables para controlar si el volumen está fijo
volumen_fijo = False

#------------------------------------------------------------------


while True:
    success,img = cap.read()

    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    resultado = manos.process(imgRGB)

    if resultado.multi_hand_landmarks:
        for handsLms in resultado.multi_hand_landmarks:
           # mpDibujar.draw_landmarks(img,handsLms,mpmanos.HAND_CONNECTIONS)
           for id, lm in enumerate(handsLms.landmark):
               alto,ancho,color =img.shape
               cx,cy = int(lm.x*ancho), int(lm.y*alto)
               if id == 4:
                   cv2.circle(img,(cx,cy),10,(255,255,0),cv2.FILLED)
                   x4,y4 =cx,cy
               elif id == 8:
                    cv2.circle(img,(cx,cy),10,(255,255,0),cv2.FILLED)
                    x8,y8 =cx,cy
               elif id == 12:  # Dedo anular
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    x12, y12 = cx, cy   
                            
       # mediaX = (x4+x8)//2
       # mediaY = (y4+y8)//2

#--------------------------------------------------------------------------               
        distanciaEntreDedos = math.hypot(x8-x4,y8-y4)
        cv2.line(img,(x4,y4),(x8,y8),(0,255,0),3)

        # Cálculo para bajar el volumen con anular
        distanciaEntreDedosAnular = math.hypot(x12 - x4, y12 - y4)
        cv2.line(img, (x4, y4), (x12, y12), (255, 0, 255), 3)
#--------------------------------------------------------------------------
     # Obtener el volumen actual del sistema en dB
        volumen_actual_sistema = volumen.GetMasterVolumeLevel()
       # Convertir el volumen actual de dB a potencia
        potencia_actual = 10 ** (volumen_actual_sistema / 20) 
        print(potencia_actual)
#--------------------------------------------------------------------------
        # Disminuir volumen con el indice
        if distanciaEntreDedos < 35 and cambiar == 0:
            print("Realizo acción")
            cambiar = 1
            volumen_fijo = False  # Permitir ajustar el volumen
#--------------------------------------------------------------------------


            if potencia_actual >= 0.0005 and potencia_actual < 0.006:
                # Incrementar la potencia en un 10%
                nueva_potencia = 0.00791
                # Convertir la nueva potencia de vuelta a dB
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                # Asegurarse de que el nuevo volumen no exceda el máximo permitido
                #nuevo_volumen = min(nuevo_volumen, VolMax)
                # Ajustar el volumen del sistema
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.007 and potencia_actual < 0.02:
                nueva_potencia = 0.0216
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)

            #10/20
            elif potencia_actual >= 0.0201 and potencia_actual < 0.039:
                nueva_potencia = 0.0410
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.04 and potencia_actual < 0.063:
                nueva_potencia = 0.0656
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)

            #20/30
            elif potencia_actual >= 0.064 and potencia_actual < 0.09:
                nueva_potencia = 0.0948
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.091 and potencia_actual < 0.12:
                nueva_potencia = 0.128
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)

            #30/40
            elif potencia_actual >= 0.121 and potencia_actual < 0.16:
                nueva_potencia = 0.166
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.161 and potencia_actual < 0.200:
                nueva_potencia = 0.208
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)

            #40/50
            elif potencia_actual >= 0.201 and potencia_actual < 0.25:
                nueva_potencia = 0.254
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.251 and potencia_actual < 0.290:
                nueva_potencia = 0.304
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)

            #50/60
            elif potencia_actual >= 0.291 and potencia_actual < 0.35:
                nueva_potencia = 0.358
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.351 and potencia_actual < 0.41:
                nueva_potencia = 0.415
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)

            #60/70
            elif potencia_actual >= 0.411 and potencia_actual < 0.47:
                nueva_potencia = 0.476
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.471 and potencia_actual < 0.53:
                nueva_potencia = 0.541
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            
            #70/80
            elif potencia_actual >= 0.531 and potencia_actual < 0.59:
                nueva_potencia = 0.609
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.591 and potencia_actual < 0.670:
                nueva_potencia = 0.680
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)

            #80/90
            elif potencia_actual >= 0.671 and potencia_actual < 0.745:
                nueva_potencia = 0.755
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.741 and potencia_actual < 0.82:
                nueva_potencia = 0.833
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            

            #90/100
            elif potencia_actual >= 0.821 and potencia_actual < 0.9:
                nueva_potencia = 0.915
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.91 and potencia_actual < 1:
                nueva_potencia = 1
                nuevo_volumen = 20 * np.log10(nueva_potencia) 
                volumen.SetMasterVolumeLevel(nuevo_volumen, None)                
#--------------------------------------------------------------------------

        # Disminuir volumen con el anular
        if distanciaEntreDedosAnular < 35 and cambiar == 0:
            print("Disminuyo volumen")
            cambiar = 1
            volumen_fijo = False  # Permitir ajustar el volumen
#--------------------------------------------------------------------------
            #0/10
            if potencia_actual >= 0.0013 and potencia_actual < 0.009:
                    nueva_potencia = 0.0014
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.01 and potencia_actual <= 0.024:
                    nueva_potencia = 0.0079
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None) 
            #10/20
            elif potencia_actual >= 0.025 and potencia_actual < 0.044:
                    nueva_potencia = 0.0217
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.045 and potencia_actual <= 0.071:
                    nueva_potencia = 0.0411
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None) 
            #20/30
            elif potencia_actual >= 0.07 and potencia_actual < 0.1:
                    nueva_potencia = 0.0656
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.101 and potencia_actual <= 0.131:
                    nueva_potencia = 0.0948
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None) 
            #30/40
            elif potencia_actual >= 0.13 and potencia_actual < 0.171:
                    nueva_potencia = 0.128
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.17 and potencia_actual <= 0.211:
                    nueva_potencia = 0.166
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None) 
            #40/50
            elif potencia_actual >= 0.21 and potencia_actual < 0.261:
                    nueva_potencia = 0.208
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.26 and potencia_actual <= 0.311:
                    nueva_potencia = 0.254
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None) 
            #50/60
            elif potencia_actual >= 0.31 and potencia_actual < 0.361:
                    nueva_potencia = 0.304
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.36 and potencia_actual <= 0.421:
                    nueva_potencia = 0.358
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None) 
            #60/70
            elif potencia_actual >= 0.42 and potencia_actual < 0.481:
                    nueva_potencia = 0.415
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.48 and potencia_actual <= 0.551:
                    nueva_potencia = 0.476
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)              
            #70/80
            elif potencia_actual >= 0.55 and potencia_actual < 0.621:
                    nueva_potencia = 0.541
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.62 and potencia_actual <= 0.691:
                    nueva_potencia = 0.609
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)    
            #80/90
            elif potencia_actual >= 0.69 and potencia_actual < 0.76:
                    nueva_potencia = 0.680
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.77 and potencia_actual <= 0.839:
                    nueva_potencia = 0.755
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)          
            #90/100
            elif potencia_actual >= 0.84 and potencia_actual < 0.92:
                    nueva_potencia = 0.833
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)
            elif potencia_actual >= 0.93 and potencia_actual <= 1.0:
                    nueva_potencia = 0.915
                    nuevo_volumen = 20 * np.log10(nueva_potencia)
                    volumen.SetMasterVolumeLevel(nuevo_volumen, None)
#--------------------------------------------------------------------------

        if distanciaEntreDedos>60 and cambiar == 1 and distanciaEntreDedosAnular>50:
            print("Paro acción")
            cambiar = 0   
        elif distanciaEntreDedosAnular>60 and cambiar == 1 and distanciaEntreDedos>50:
            print("Paro acción")
            cambiar = 0   
    cv2.imshow("Image",img)
    cv2.waitKey(1)
