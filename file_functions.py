import os 
import sys 
import shutil
import hashlib
import json 
import datetime 
import base64
from hash import HashCalculator
from file_handler import FileHandler
from utility import Utility

class Filefunctions:
    def __init__(self):
        self.hash = HashCalculator()
        self.file_handler = FileHandler()
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
            del data[key]
        self.utility.dump_json(data, file_path)

    
    
    def get_unadded_files(self,added):
        unadded_files=set()
        try:
            for root, dirs, files in os.walk(os.getcwd()):
                dirs[:] = [d for d in dirs if d not in [
                    '.bhavu', '_pycache_', '.git']]
                files[:] = [f for f in files if f not in ['vcs.py', '.gitignore']]
                for file in files:
                    file_path = os.path.join(root, file)
                    hash = self.hash.hash_file(file_path)
                    rel_path = os.path.relpath(file_path, os.getcwd())
                    if rel_path not in added or added[rel_path]!=hash:
                        unadded_files.add(rel_path)
        except Exception as e:
            print(f"An error occurred: {e}")
        return unadded_files


    def get_commited_files(self, commit_file, type):
        try:
            data = self.utility.decrypt_data_file_path(commit_file)
            data = self.utility.read_data(data)
            added_files = data[type]
            return added_files
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def save_object(self, commit_path, commit_data):
        try:
            object_hash = self.utility.get_object_hash(commit_data)
            object_path = self.utility.get_object_path(commit_path, object_hash)

            if not self.check_file_exists(object_path):
                commit_data = self.utility.encrypt_data(commit_data)
                self.file_handler.write_file(object_path, commit_data)
            return object_hash
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def clear_directory(self,dir_path):
        try:
            for root, dirs, files in os.walk(dir_path):
                dirs[:] = [d for d in dirs if d not in [
                    '.bhavu', '_pycache_', '.git']]
                files[:] = [f for f in files if f not in ['vcs.py', '.gitignore']]
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for dir in dirs:
                    dir_path = os.path.join(root,dir)
                    shutil.rmtree(dir_path)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def clear_directory(self,dir_path):
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d not in [
                '.bhavu', '_pycache_', '.git']]
            files[:] = [f for f in files if f not in ['vcs.py', '.gitignore']]
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root,dir)
                shutil.rmtree(dir_path)


    