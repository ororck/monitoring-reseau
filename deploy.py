import subprocess
import sys
import os
from datetime import datetime

LOG_FILE = f"deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log(message, statut="INFO"):
    horodatage = datetime.now().strftime("%H:%M:%S")
    ligne = f"[{horodatage}] [{statut}] {message}"
    print(ligne)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(ligne + "\n")

def verifier_prerequis():
    log("Vérification des prérequis...")
    
    outils = ["python", "git"]
    
    for outil in outils:
        try:
            subprocess.run(
                [outil, "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            log(f"{outil} trouvé ✓", "OK")
        except FileNotFoundError:
            log(f"{outil} non trouvé — installation requise", "ERREUR")
            sys.exit(1)

def installer_projet(repo_url, dossier):
    log(f"Clonage du projet depuis {repo_url}...")
    
    if os.path.exists(dossier):
        log(f"Le dossier {dossier} existe déjà — mise à jour du code", "INFO")
        subprocess.run(["git", "-C", dossier, "pull"], check=True)
    else:
        subprocess.run(["git", "clone", repo_url, dossier], check=True)
        log("Clonage terminé ✓", "OK")

    log("Création de l'environnement virtuel...")
    venv_path = os.path.join(dossier, ".venv")
    subprocess.run(["python", "-m", "venv", venv_path], check=True)
    log("Environnement virtuel créé ✓", "OK")

    log("Installation des dépendances...")
    pip = os.path.join(venv_path, "Scripts", "pip")
    subprocess.run([pip, "install", "-r", 
                   os.path.join(dossier, "requirements.txt")], check=True)
    log("Dépendances installées ✓", "OK")

def lancer_tests(dossier):
    log("Lancement des tests...")
    
    python = os.path.join(dossier, ".venv", "Scripts", "python")
    test_file = os.path.join(dossier, "test_monitoring.py")
    
    if not os.path.exists(test_file):
        log("Aucun fichier de tests trouvé — étape ignorée", "WARNING")
        return True
    
    resultat = subprocess.run([python, "-m", "pytest", test_file])
    
    if resultat.returncode == 0:
        log("Tests réussis ✓", "OK")
        return True
    else:
        log("Tests échoués — déploiement annulé", "ERREUR")
        return False
    
def main():
    REPO_URL = "https://github.com/ororck/monitoring-reseau.git"
    DOSSIER  = "monitoring-reseau"

    log("=" * 50)
    log("  DÉPLOIEMENT — Dashboard Monitoring Réseau")
    log("=" * 50)

    verifier_prerequis()
    installer_projet(REPO_URL, DOSSIER)
    
    tests_ok = lancer_tests(DOSSIER)
    if not tests_ok:
        sys.exit(1)

    log("=" * 50)
    log("Déploiement terminé avec succès ✓", "OK")
    log("Lancer l'application avec :", "INFO")
    log(f"  cd {DOSSIER}", "INFO")
    log(f"  .venv\\Scripts\\python app.py", "INFO")
    log("=" * 50)

if __name__ == "__main__":
    main()