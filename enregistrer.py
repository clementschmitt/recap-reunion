import pyaudiowpatch as pyaudio
import wave
from datetime import datetime
from pathlib import Path

dossier = Path("enregistrements") / datetime.now().strftime("%Y-%m-%d_%Hh%M")
dossier.mkdir(parents=True, exist_ok=True)

# initialiser PyAudio
p = pyaudio.PyAudio()

def ouvrir_piste(appareil, nom_fichier):
    # ouvrir le fichier WAV pour l'écriture
    wav = wave.open(str(dossier / nom_fichier), "wb")

    wav.setnchannels(appareil["maxInputChannels"])
    wav.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wav.setframerate(int(appareil["defaultSampleRate"]))

    # définir la fonction de rappel pour l'enregistrement audio
    def ecrire_piste(in_data, frame_count, time_info, status):
        wav.writeframes(in_data)
        return (None, pyaudio.paContinue)

    # ouvrir le flux audio pour l'enregistrement
    flux = p.open(
        format=pyaudio.paInt16,
        channels=appareil["maxInputChannels"],
        rate=int(appareil["defaultSampleRate"]),
        input=True,
        input_device_index=appareil["index"],
        frames_per_buffer=1024,
        stream_callback=ecrire_piste
    )

    return flux, wav

# trouver le micro et le son du pc par défaut
micro = p.get_default_input_device_info()
print(f"Enregistrement depuis le micro : {micro['name']}")

pc = p.get_default_wasapi_loopback()
print(f"Enregistrement depuis le périphérique de sortie : {pc['name']}")

micro_flux, micro_wav = ouvrir_piste(micro, "micro.wav")
pc_flux, pc_wav = ouvrir_piste(pc, "pc.wav")

# démarrer l'enregistrement
input("Enregistrement en cours... Appuyez sur Entrée pour arrêter l'enregistrement...")
micro_flux.stop_stream()
micro_flux.close()
pc_flux.stop_stream()
pc_flux.close()
micro_wav.close()
pc_wav.close()
p.terminate()