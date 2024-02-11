import os 
import sys 
import shutil
import hashlib
import json 
import datetime 
import base64
from pathlib import Path


        
class HashCalculator:
    def md5_hash_from_dir(self, directory):
        try:
            assert Path(directory).is_dir()
            for path in sorted(Path(directory).iterdir(), key=lambda p: str(p).lower()):
                self.hash.hash(path.name.encode())
                if path.is_file():
                    with open(path, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            self.hash.hash(chunk)
                elif path.is_dir():
                    self.md5_hash_from_dir(path)
            return hash
        except Exception as e:
            print(f"An error occurred: {e}")
            return Non
    def md5_dir(self,directory):
        try:
            return md5_update_from_dir(directory, hashlib.md5()).hexdigest()
        except Exception as e:
            print(f"An error occurred: {e}")
            return Non
    def hash_file(self,filename):
        try:
            h = hashlib.md5()
            with open(filename, 'rb') as file:
                # loop till the end of the file
                chunk = 0
                while chunk != b'':
                    # read only 1024 bytes at a time
                    chunk = file.read(1024)
                    h.update(chunk)
            return h.hexdigest()
        except Exception as e:
            print(f"An error occurred: {e}")
            return Non