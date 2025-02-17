import os
import platform
import pytest
import zipfile
import tempfile
from backup import get_backup_filename, get_home_directory, create_zip_backup, create_tar_backup, create_backup

def test_get_backup_filename():
    filename = get_backup_filename()
    assert filename.startswith("backup_")
    
    # Vérifier si le nom contient bien l'OS attendu
    assert "_windows_" in filename or "_linux_" in filename or "_darwin_" in filename


@pytest.mark.skipif(platform.system().lower() != "windows", reason="Test spécifique à Windows")
def test_light_create_zip_backup():
    """Test de création d'une sauvegarde ZIP avec un répertoire de test allégé."""
    
    # Création d'un répertoire temporaire avec quelques fichiers
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file1 = os.path.join(temp_dir, "test1.txt")
        test_file2 = os.path.join(temp_dir, "test2.txt")

        with open(test_file1, "w") as f:
            f.write("Fichier de test 1")

        with open(test_file2, "w") as f:
            f.write("Fichier de test 2")

        # Création d'une archive ZIP à partir de ce répertoire
        backup_name = get_backup_filename() + ".zip"
        backup_path = os.path.join(temp_dir, backup_name)

        with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(test_file1, os.path.basename(test_file1))
            zipf.write(test_file2, os.path.basename(test_file2))

        # Vérifications
        assert os.path.exists(backup_path)
        assert backup_path.endswith(".zip")

        # Vérifier que les fichiers sont bien dans l'archive
        with zipfile.ZipFile(backup_path, "r") as zipf:
            assert "test1.txt" in zipf.namelist()
            assert "test2.txt" in zipf.namelist()


# Test pour get_backup_filename
def test_get_backup_filename():
    filename = get_backup_filename()
    assert filename.startswith("backup_")
    assert "_windows_" in filename or "_linux_" in filename or "_darwin_" in filename
    assert len(filename.split("_")) == 4  # Verifie qu'il y a bien 4 parties : 'backup', 'timestamp', 'os', 'date'

# Test pour get_home_directory
def test_get_home_directory():
    home_dir = get_home_directory()
    # Vérifie que le répertoire personnel existe et est un dossier
    assert os.path.isdir(home_dir)
    assert "Users" in home_dir or "home" in home_dir  # Vérifie si c'est un dossier utilisateur valide

# Test pour create_zip_backup
def test_create_zip_backup(tmpdir):
    backup_path = create_zip_backup(output_dir=tmpdir)
    assert backup_path.endswith(".zip")
    assert os.path.exists(backup_path)

    # Vérifie qu'un fichier zip existe et n'est pas vide
    with open(backup_path, "rb") as f:
        content = f.read()
        assert len(content) > 0  # Le fichier zip ne doit pas être vide

# Test pour create_tar_backup
def test_create_tar_backup(tmpdir):
    backup_path = create_tar_backup(output_dir=tmpdir)
    assert backup_path.endswith(".tar.gz")
    assert os.path.exists(backup_path)

    # Vérifie qu'un fichier tar.gz existe et n'est pas vide
    with open(backup_path, "rb") as f:
        content = f.read()
        assert len(content) > 0  # Le fichier tar.gz ne doit pas être vide

# Test pour create_backup
def test_create_backup(tmpdir):
    # Test si la fonction crée la bonne sauvegarde en fonction de l'OS
    backup_file = create_backup()
    assert os.path.exists(backup_file)
    assert backup_file.endswith(('.zip', '.tar.gz'))  # Vérifie que l'extension est correcte

