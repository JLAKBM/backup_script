import os
import platform
import tarfile
import zipfile
from datetime import datetime
from tqdm import tqdm  # Ajout de tqdm pour la progression

def get_backup_filename():
    """Génère un nom de fichier basé sur la date et l'OS."""
    os_name = platform.system().lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"backup_{os_name}_{timestamp}"

def get_home_directory():
    """Retourne le répertoire personnel de l'utilisateur."""
    return os.path.expanduser("~")

def create_tar_backup(output_dir="."):
    """Crée une archive .tar.gz du répertoire personnel avec affichage de la progression."""
    home_dir = get_home_directory()
    backup_name = get_backup_filename() + ".tar.gz"
    backup_path = os.path.join(output_dir, backup_name)

    with tarfile.open(backup_path, "w:gz") as tar:
        file_list = [os.path.join(root, f) for root, _, files in os.walk(home_dir) for f in files]

        for file in tqdm(file_list, desc="Compression en cours", unit="fichier"):
            try:
                tar.add(file, arcname=os.path.relpath(file, home_dir))
            except PermissionError:
                print(f"Permission refusée : {file}, ignoré.")
            except Exception as e:
                print(f"Erreur sur {file} : {e}, ignoré.")

    return backup_path

def create_zip_backup(output_dir="."):
    """Crée une archive .zip du répertoire personnel avec affichage de la progression."""
    home_dir = get_home_directory()
    backup_name = get_backup_filename() + ".zip"
    backup_path = os.path.join(output_dir, backup_name)

    file_list = [os.path.join(root, f) for root, _, files in os.walk(home_dir) for f in files]

    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in tqdm(file_list, desc="Compression en cours", unit="fichier"):
            try:
                zipf.write(file, os.path.relpath(file, home_dir))
            except PermissionError:
                print(f"Permission refusée : {file}, ignoré.")
            except Exception as e:
                print(f"Erreur sur {file} : {e}, ignoré.")

    return backup_path

def create_backup():
    """Détecte l'OS et crée la sauvegarde appropriée avec barre de progression."""
    os_name = platform.system().lower()
    if os_name == "windows":
        return create_zip_backup()
    else:
        return create_tar_backup()

if __name__ == "__main__":
    backup_file = create_backup()
    print(f"\n✅ Sauvegarde terminée : {backup_file}")
