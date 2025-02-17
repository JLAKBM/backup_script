import os
import platform
import tarfile
import zipfile
import logging
from datetime import datetime
from tqdm import tqdm  # Pour afficher une barre de progression

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_backup_filename():
    """Génère un nom de fichier basé sur la date et l'OS."""
    os_name = platform.system().lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{os_name}_{timestamp}"
    logging.info(f"Nom du fichier de sauvegarde généré : {backup_filename}")
    return backup_filename

def get_home_directory():
    """Retourne le répertoire personnel de l'utilisateur."""
    home_dir = os.path.expanduser("~")
    logging.info(f"Répertoire personnel détecté : {home_dir}")
    return home_dir

def create_tar_backup(output_dir="."):
    """Crée une archive .tar.gz du répertoire personnel avec logs et barre de progression."""
    home_dir = get_home_directory()
    backup_name = get_backup_filename() + ".tar.gz"
    backup_path = os.path.join(output_dir, backup_name)

    logging.info(f"Début de la création de l'archive TAR : {backup_path}")

    with tarfile.open(backup_path, "w:gz") as tar:
        file_list = [os.path.join(root, f) for root, _, files in os.walk(home_dir) for f in files]
        logging.info(f"Nombre de fichiers à archiver : {len(file_list)}")

        for file in tqdm(file_list, desc="Compression en cours", unit="fichier"):
            try:
                tar.add(file, arcname=os.path.relpath(file, home_dir))
                logging.debug(f"Ajouté : {file}")
            except PermissionError:
                logging.warning(f"Permission refusée : {file}, ignoré.")
            except Exception as e:
                logging.error(f"Erreur sur {file} : {e}, ignoré.")

    logging.info(f"Sauvegarde TAR terminée : {backup_path}")
    return backup_path

def create_zip_backup(output_dir="."):
    """Crée une archive .zip du répertoire personnel avec logs et barre de progression."""
    home_dir = get_home_directory()
    backup_name = get_backup_filename() + ".zip"
    backup_path = os.path.join(output_dir, backup_name)

    logging.info(f"Début de la création de l'archive ZIP : {backup_path}")

    file_list = [os.path.join(root, f) for root, _, files in os.walk(home_dir) for f in files]
    logging.info(f"Nombre de fichiers à archiver : {len(file_list)}")

    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in tqdm(file_list, desc="Compression en cours", unit="fichier"):
            try:
                zipf.write(file, os.path.relpath(file, home_dir))
                logging.debug(f"Ajouté : {file}")
            except PermissionError:
                logging.warning(f"Permission refusée : {file}, ignoré.")
            except Exception as e:
                logging.error(f"Erreur sur {file} : {e}, ignoré.")

    logging.info(f"Sauvegarde ZIP terminée : {backup_path}")
    return backup_path

def create_backup():
    """Détecte l'OS et crée la sauvegarde appropriée avec logs."""
    os_name = platform.system().lower()
    logging.info(f"Système d'exploitation détecté : {os_name}")

    if os_name == "windows":
        return create_zip_backup()
    else:
        return create_tar_backup()

if __name__ == "__main__":
    logging.info("Démarrage du script de sauvegarde.")
    backup_file = create_backup()
    logging.info(f"✅ Sauvegarde terminée : {backup_file}")
