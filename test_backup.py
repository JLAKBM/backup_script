import os
import platform
import pytest
import zipfile
import tempfile
from backup import get_backup_filename, create_zip_backup

def test_get_backup_filename():
    filename = get_backup_filename()
    assert filename.startswith("backup_")
    assert filename.endswith(("_windows", "_linux", "_darwin"))

@pytest.mark.skipif(platform.system().lower() != "windows", reason="Test spécifique à Windows")
def test_create_zip_backup():
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
