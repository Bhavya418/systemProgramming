import os 
import sys 
import shutil
import hashlib
import json 
import datetime 



class VersionControlSystem:

    def init(self,repo_path=".tico"):
        self.username = input("Enter your username: ")
        self.email = input("Enter your email: ")
        self.repo_path = repo_path
        os.mkdir(repo_path)
        

if __name__ == "__main__": 
    vcs = VersionControlSystem()
    command = sys.argv[1]
    if(command == 'init'):
        vcs.init()

    
    
