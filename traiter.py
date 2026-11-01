import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()
cle = os.environ["DEEPGRAM_API_KEY"]

dossier = Path(sys.argv[1])

def horodatage(temps):
    minutes, secondes = divmod(temps, 60)
    heures, minutes = divmod(minutes, 60)
    return f"{int(heures):02d}:{int(minutes):02d}:{int(secondes):02d}"

def transcrire_fichier(fichier, qui):
    url = "https://api.deepgram.com/v1/listen"
    parameters = {
        "model": "nova-3",
        "smart_format": "true",
        "language": "fr",
        "utterances": "true"
    }
    headers = {
        "Authorization": f"Token {cle}",
        "Content-Type": "audio/wav"
    }

    with open(fichier, "rb") as f:
        response = requests.post(url, headers=headers, params=parameters, data=f, timeout=300)

    response.raise_for_status()
    phrases = response.json()["results"]["utterances"]

    resultat = []
    for phrase in phrases:
        resultat.append({"debut": phrase["start"], "fin": phrase["end"], "texte": phrase["transcript"], "qui": qui})
    
    return resultat

moi = transcrire_fichier(dossier / "micro.wav", "Moi")
interlocuteur = transcrire_fichier(dossier / "pc.wav", "Interlocuteur")

conversation = sorted(moi + interlocuteur, key=lambda x: x["debut"])

lignes = []

for phrase in conversation:
    lignes.append(f"[{horodatage(phrase['debut'])}] {phrase['qui']} : {phrase['texte']}")

texte_final = "\n".join(lignes)
(dossier / "transcription.txt").write_text(texte_final, encoding="utf-8")
print(f"Transcription terminée. Le fichier est enregistré dans : {dossier / 'transcription.txt'}")