import os 
import sys 
import shutil
import hashlib
import json 
import datetime 
import base64
from utility import Utility

class File_functions:
    def __init__(self):
        self.utility = Utility()
        
    def check_file_exists(self, filename):
        try:
            return os.path.exists(filename)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def check_dir(self, filename):
        try:
            return os.path.isdir(filename)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def file_update(self,file_path):
        data = self.utility.read_json(file_path)
        
        delKeys  = []
        for key in data:
            if not self.check_file_exists(data[key]):
                delKeys.append(key)
        for key in delKeys:
            del data1[key]
        self.utility.dump_json(data, file_path)
