#Importando librerias y paquetes
import cv2
import os
import time
#from gtts import gTTS

#hacer referencia a la haarcasdade de cada uno de los casos

cuerpo = cv2.CascadeClassifier('haarcascades_haarcascade_fullbody.xml')
carro = cv2.CascadeClassifier('vehicle_detection_haarcascades_master_cars.xml')
rostro = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
gato = cv2.CascadeClassifier('haarcascade_frontalcatface_extended.xml')

#referencia a la camara del cumputador para poder utilizarla

#cap = cv2.VideoCapture("dataset_video1.avi") #Video carros 1
#cap = cv2.VideoCapture("dataset_video2.avi") #Video carros 2
#cap = cv2.VideoCapture("londres2.mp4") #Video personas
cap = cv2.VideoCapture(0)

#referencia a camara ip para poder utilizarla
'''address = "https://192.168.1.13:8080/video"
cap.open(address)'''

#ciclo infinito que permite ciclar fotogramas del video

while True:
    texto="Nada"
    _,img = cap.read() #Lee los fotogramas del video
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Convertir a escala de grises el video

    # Guardar todas las imagenes detectadas con metodo establecido
    body = cuerpo.detectMultiScale(gray, 1.1, 4)
    car = carro.detectMultiScale(gray, 1.1, 4)
    face = rostro.detectMultiScale(gray, 1.1, 4)
    cat = gato.detectMultiScale(gray, 1.1, 4)

    # ciclo que nos dibuja los rectangulos utilizando vertices del mismo
    for(x,y,w,h) in body:
        cv2.rectangle(img,(x,y), (x+w, y+h), (255,0,0), 2) #azul
        # Mostrar el texto en la imagen
        cv2.putText(img, "Cuerpo", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    for (x, y, w, h) in car:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) #Verde
        # Mostrar el texto en la imagen
        cv2.putText(img, "Carro", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2) #rojo
        # Mostrar el texto en la imagen
        cv2.putText(img, "Rostro", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    for (x, y, w, h) in cat:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2) #Blanco
        # Mostrar el texto en la imagen
        cv2.putText(img, "Gato", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    #impresion de la ima gen ya procesada sin escala de grises
    cv2.imshow('img', img)



    #Audio descriptivo
    '''for an in range(2):
        os.system("tecsify.mp3")
        time.sleep(5)
        texto = "Nada"'''

    #condicional para detectar la tecla ESC y cerrar el bucle
    k = cv2.waitKey(30)
    if k == 27:
        break




#cierre total de la camara
cap.retenre()