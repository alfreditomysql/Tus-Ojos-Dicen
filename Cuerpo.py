import cv2
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play

# Función para detectar cuerpos en una imagen
def detectar_cuerpo(imagen):
    # Cargar el clasificador preentrenado para la detección de cuerpos
    body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

    # Convertir la imagen a escala de grises (requerido para la detección de cuerpos)
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Detectar cuerpos en la imagen utilizando el clasificador cargado
    cuerpos = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Verificar si se detectaron cuerpos en la imagen
    if len(cuerpos) > 0:
        print("Se ha detectado un cuerpo humano.")
        return True, cuerpos
    else:
        print("No se ha detectado ningún cuerpo humano.")
        return False, []

# Función para convertir texto a voz y reproducirlo
def texto_a_voz(texto):
    # Crear un objeto gTTS (Google Text-to-Speech) para convertir el texto en un archivo de audio MP3
    tts = gTTS(text=texto, lang='es')
    tts.save("output.mp3")

    # Convertir el archivo MP3 a WAV (requerido para reproducir el audio)
    audio = AudioSegment.from_mp3("output.mp3")
    audio.export("output.wav", format="wav")

# Función para reproducir el archivo de audio WAV
def reproducir_audio():
    # Reproducir el archivo WAV utilizando la biblioteca pydub y pyaudio
    play(AudioSegment.from_wav("output.wav"))

# Función principal del programa
def main():
    ruta_ffmpeg_ffprobe = "FFmpeg/bin"
    os.environ["PATH"] += os.pathsep + ruta_ffmpeg_ffprobe

    # Inicializar la cámara capturando video de la cámara del dispositivo (valor 0 indica la cámara predeterminada)
    camara = cv2.VideoCapture(0)

    while True:
        # Leer un cuadro (imagen) de la cámara
        ret, frame = camara.read()

        # Verificar si se pudo leer el cuadro de la cámara
        if not ret:
            print("No se puede obtener el cuadro de la cámara.")
            break

        # Detectar cuerpo en el cuadro utilizando la función detectar_cuerpo
        cuerpo_detectado, cuerpos = detectar_cuerpo(frame)

        # Si se detectó un cuerpo en el cuadro
        if cuerpo_detectado:
            # Dibujar un rectángulo alrededor del cuerpo detectado en la imagen
            for (x, y, w, h) in cuerpos:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Mostrar el texto "Se ha detectado un cuerpo" en la imagen
            cv2.putText(frame, "Se ha detectado un cuerpo", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Convertir el texto a voz y reproducirlo
            texto_a_voz("Se ha detectado un cuerpo humano.")
            reproducir_audio()
        else:
            equis=1
            # Si no se detectó un cuerpo, mostrar el cuadro sin modificaciones
            #cv2.imshow("Deteccion de Cuerpo", frame)

        # Esperar 1 milisegundo para que se actualice la ventana de la cámara
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar todas las ventanas
    camara.release()
    cv2.destroyAllWindows()

# Verificar si este archivo es el programa principal que se está ejecutando
if __name__ == "__main__":
    # Ejecutar la función main
    main()
