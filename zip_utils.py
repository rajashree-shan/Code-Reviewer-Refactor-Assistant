import zipfile
import os
import tempfile

def extract_python_files(zip_file) -> dict:
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        py_files = {}
        for root, _, files in os.walk(tmpdir):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        py_files[file] = f.read()
        return py_files
