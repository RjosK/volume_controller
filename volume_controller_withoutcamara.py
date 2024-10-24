import cv2 
import mediapipe as mp
import math
from comtypes import CLSCTX_ALL
import pyautogui

source = 0 # webcam| rtsp_url | video file as input
cap = cv2.VideoCapture(source) # Then start the webcam

mpmanos = mp.solutions.hands

manos = mpmanos.Hands(static_image_mode=False, 
                      max_num_hands=1,  # número de manos a detectar
                      min_detection_confidence=0.9, 
                      min_tracking_confidence=0.8)

mpDibujar = mp.solutions.drawing_utils
cambiar = 0
#----------------------------------------------------------------- 
while True:
    success, img = cap.read()
    
    if not success:
        break  # Sale si no hay éxito en la captura de la cámara

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resultado = manos.process(imgRGB)
#--------------------------------------------------------------------------               
    # Marcar los dedos a usar
    if resultado.multi_hand_landmarks:
        for handsLms in resultado.multi_hand_landmarks:
            for id, lm in enumerate(handsLms.landmark):
                alto, ancho, color = img.shape
                cx, cy = int(lm.x * ancho), int(lm.y * alto)
                
                if id == 4:
                    x4, y4 = cx, cy
                elif id == 8:
                    x8, y8 = cx, cy
                elif id == 12:  # Dedo anular
                    x12, y12 = cx, cy   
#--------------------------------------------------------------------------               
        # Cálculo para bajar el volumen con anular
        distanciaEntreDedos_indice = math.hypot(x8 - x4, y8 - y4)
        distanciaEntreDedos_Anular = math.hypot(x12 - x4, y12 - y4)
#--------------------------------------------------------------------------               
        if distanciaEntreDedos_indice < 35 and cambiar == 0:
            pyautogui.keyDown('volumeup')
#--------------------------------------------------------------------------               
        if distanciaEntreDedos_Anular < 35 and cambiar == 0:
            pyautogui.keyDown('volumedown')
#--------------------------------------------------------------------------               
    # Omitir el uso de cv2.imshow() para evitar abrir una ventana de visualización
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara cuando se termine
cap.release()
cv2.destroyAllWindows()
