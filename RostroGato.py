import cv2
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play

def detectar_rostro(imagen):
    # Cargar el clasificador preentrenado para la detección de rostros de gatos
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface_extended.xml')

    # Convertir la imagen a escala de grises (requerido para la detección de rostros)
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Detectar rostros de gatos en la imagen utilizando el clasificador cargado
    rostros = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Verificar si se detectaron rostros de gatos en la imagen
    if len(rostros) > 0:
        print("Se ha detectado un rostro de gato.")
        return True, rostros
    else:
        print("No se ha detectado ningún rostro de gato.")
        return False, []

def texto_a_voz(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save("output.mp3")
    audio = AudioSegment.from_mp3("output.mp3")
    audio.export("output.wav", format="wav")

def reproducir_audio():
    play(AudioSegment.from_wav("output.wav"))

def main():
    ruta_ffmpeg_ffprobe = "FFmpeg/bin"
    os.environ["PATH"] += os.pathsep + ruta_ffmpeg_ffprobe

    camara = cv2.VideoCapture(0)

    while True:
        ret, frame = camara.read()

        if not ret:
            print("No se puede obtener el cuadro de la cámara.")
            break

        rostro_detectado, rostros = detectar_rostro(frame)

        if rostro_detectado:
            for (x, y, w, h) in rostros:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.putText(frame, "Se ha detectado un rostro de gato", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            texto_a_voz("Se ha detectado un rostro de gato.")
            reproducir_audio()
        else:
            equis=1
            #cv2.imshow("Deteccion de Rostro de Gato", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camara.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
