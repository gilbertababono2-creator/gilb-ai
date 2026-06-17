import os
import shutil

def cleanup_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)

def cleanup_dir(dirpath: str):
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
