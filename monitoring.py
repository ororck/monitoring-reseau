import subprocess
import platform
from datetime import datetime
import sqlite3

DB = "historique.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS pings (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nom       TEXT,
            ip        TEXT,
            statut    INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def sauvegarder_ping(nom, ip, statut):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO pings (nom, ip, statut) VALUES (?, ?, ?)",
        (nom, ip, 1 if statut else 0)
    )
    conn.commit()
    conn.close()

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
        sauvegarder_ping(nom, ip, statut)
        resultats.append({
            "nom": nom,
            "ip": ip,
            "statut": statut
        })
    return resultats

init_db()