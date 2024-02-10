import os 
import sys 
import shutil
import hashlib
import json 
import datetime 
import base64

class FileHandler:
    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def write_file(self, filename,data):
        try:
            with open(filename, 'w') as file:
                file.write(data)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def append_file(self, filename,data):
        try:
            with open(filename, 'a') as file:
                file.write(data)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
