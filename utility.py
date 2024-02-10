import os 
import sys 
import shutil
import hashlib
import json 
import datetime 
import base64

class Utility:
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
    
    def printLine(self):
        print("'.bhavu' folder is not initialized...")
        print("Run 'bhavu init' command to initialize")