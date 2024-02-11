import os 
import sys 
import shutil
import hashlib
import json 
import datetime 
import base64
from file_handler import FileHandler

class Utility:
    def __init__(self):
        self.file_handler = FileHandler()

    def not_init(self, dir_path):
        try:
            files_and_dirs = os.listdir(dir_path)
            if '.bhavu' not in files_and_dirs:
                return True
        except OSError as e:
            print(f"Error: {e}")
        return False
    
    def get_date_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def dump_json(self, data, filename):
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)             
        except Exception as e:  
            print(f"An error occurred: {e}")
            return None
            
    def read_json(self, filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def dump_data(self,commit_data):
        json_data = json.dumps(commit_data)
        return json_data
    
    def get_object_hash(self,commit_data):
        return hashlib.sha1(commit_data.encode('utf-8')).hexdigest()
    
    def get_object_path(self,commit_path,object_hash):
        return os.path.join(commit_path,object_hash)
    
    def encrypt_data(self,commit_data):
        return base64.b64encode(commit_data.encode()).decode('utf-8')
    
    def decrypt_data(self,commit_data):
        return base64.b64decode(commit_data).decode('utf-8')
    
    def encrypt_data_file_path(self,file_path):
        try:
            data = self.file_handler.read_file(file_path)
            encrpted_data = self.encrypt_data(data)
               
            return encrpted_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    
    def decrypt_data_file_path(self,file_path):
        try:
            data = self.file_handler.read_file(file_path)
            decrypted_data = self.decrypt_data(data)
            return decrypted_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_head_commit(self,current_branch = "main",branch_path=".bhavu/branches",):
         
        current_head = os.path.join(branch_path,current_branch,'HEAD')
        head_commit = self.file_handler.read_file(current_head)
        head_commit = head_commit.strip().split("\n")[-1]
        return head_commit
    

    def printLine(self):
        print("'.bhavu' folder is not initialized...")
        print("Run 'bhavu init' command to initialize")