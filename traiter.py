import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()
cle = os.environ["DEEPGRAM_API_KEY"]

dossier = Path(sys.argv[1])

def transcrire_fichier(fichier):
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
        resultat.append({"debut": phrase["start"], "fin": phrase["end"], "texte": phrase["transcript"]})
    
    return resultat

for phrase in transcrire_fichier(dossier / "micro.wav"):
    print(f"[{phrase['debut']:.1f} s]: {phrase['texte']}")