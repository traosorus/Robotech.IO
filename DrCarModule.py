import tkinter as tk
import pyaudio
import wave
import threading
import time
import openai



class AudioRecorder:
    def __init__(self):
        self.frames = []
        self.is_recording = False

    def start_recording(self):
        self.frames = []
        self.is_recording = True
        threading.Thread(target=self._record_audio).start()

    def stop_recording(self):
        self.is_recording = False

    def _record_audio(self):
        CHUNK = 1024  # Taille de chaque chunk audio
        FORMAT = pyaudio.paInt16  # Format des échantillons
        CHANNELS = 1  # Nombre de canaux audio (mono)
        RATE = 44100  # Taux d'échantillonnage en Hz

        p = pyaudio.PyAudio()  # Crée une instance de PyAudio
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)  # Ouvre un stream audio pour l'entrée

        while self.is_recording:
            data = stream.read(CHUNK)  # Lit un chunk audio depuis le stream
            self.frames.append(data)  # Ajoute le chunk à la liste des frames enregistrées

        stream.stop_stream()  # Arrête le stream audio
        stream.close()  # Ferme le stream audio
        p.terminate()  # Termine l'instance PyAudio

    def save_recording(self, filename):
        wf = wave.open(filename, 'wb')  # Crée un fichier WAV en mode écriture
        wf.setnchannels(1)  # Définit le nombre de canaux audio (mono)
        wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))  # Définit la taille d'échantillon en bytes
        wf.setframerate(44100)  # Définit le taux d'échantillonnage en Hz
        wf.writeframes(b''.join(self.frames))  # Écrit les frames enregistrées dans le fichier WAV
        wf.close()  # Ferme le fichier WAV

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assistant vocal")

        self.recorder = AudioRecorder()
        self.is_recording = False
        self.start_time = None

        self.record_button = tk.Button(self, text="Enregistrer", command=self.toggle_recording)
        self.record_button.pack(pady=10)

        self.duration_label = tk.Label(self, text="Durée d'enregistrement: 0.0s")
        self.duration_label.pack(pady=5)

    def toggle_recording(self):
        if not self.is_recording:
            self.recorder.start_recording()  # Démarre l'enregistrement audio
            self.is_recording = True
            self.start_time = time.time()
            self.record_button.config(text="Arrêter l'enregistrement")
            self.update_duration()  # Démarre la mise à jour de la durée d'enregistrement
        else:
            self.recorder.stop_recording()  # Arrête l'enregistrement audio
            self.recorder.save_recording("enregistrement.wav")  # Sauvegarde l'enregistrement dans un fichier WAV
            self.is_recording = False
            Ts = Transcriber("enregistrement.wav")
            self.record_button.config(text="Enregistrer")

    def update_duration(self):
        if self.is_recording:
            duration = time.time() - self.start_time
            self.duration_label.config(text=f"Durée d'enregistrement: {duration:.1f}s")
            self.after(100, self.update_duration)  # Planifie la prochaine mise à jour après 100 ms

class Transcriber:
    def __init__(self,request):
                # transcribe the audio using OpenAI
        with open("API_key.txt","r") as key:
            API_key = key.read() 
        openai.api_key = API_key
        audio_file = open(request, "rb")
        self.transcript = openai.Audio.transcribe("whisper-1", audio_file)
        self.transcript = self.transcript.text
        print(self.transcript)

app = Application()
app.mainloop()
