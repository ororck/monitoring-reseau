import subprocess
import platform
from datetime import datetime


equipements = {
    "PC0 - Site A":     "192.168.1.10",
    "PC1 - Site A":     "192.168.1.11",
    "Routeur - Site A": "192.168.1.1",
    "Routeur - Site B": "192.168.2.1",
    "PC2 - Site B":     "192.168.2.10", 
    "PC3 - Site B":     "192.168.2.11",
}

def ping(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    commande = ["ping", param, "1", ip]
    resultat = subprocess.call(commande, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return resultat == 0

def get_resultats():
    resultats = []
    for nom, ip in equipements.items():
        statut = ping(ip)
        resultats.append({
            "nom": nom,
            "ip": ip,
            "statut": statut
        })
    return resultats