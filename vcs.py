import os 
import sys 
import shutil
import hashlib
import json 
import datetime 



class VersionControlSystem:

    def init(self,repo_path=".bhavu"):
        # self.username = input("Enter your username: ")
        # self.email = input("Enter your email: ")
        self.repo_path = repo_path
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

        self.object_path = os.path.join('.bhavu','objects')
        self.branch_path = os.path.join('.bhavu','branches')
        
        if not os.path.exists(self.branch_path):
            os.makedirs(self.branch_path)

        if not os.path.exists(self.object_path):
            os.makedirs(self.object_path)    
    
        #creating the main branch

        self.main_branch = os.path.join(self.branch_path,'main')

        if not os.path.exists(self.main_branch):
            os.makedirs(self.main_branch)

        self.index_file = os.path.join(repo_path,'index.json')
        self.add_file = os.path.join(repo_path,'added.json')
        files_to_be_created = [self.index_file,self.add_file]
        

        for file in files_to_be_created:
            if not os.path.exists(file):
                with open(file, "w") as index:
                    json.dump({}, index)   

        self.user_file = os.path.join(repo_path,'user.txt')

        if not os.path.exists(self.user_file):
                
            user_name = input("Enter your username: ")
            if user_name == "":
                user_name = "Unknown"
            date_time = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S") 
            with open(self.user_file, "w") as user_data:
                user_data.write(f"{date_time} {user_name}")



        


        

if __name__ == "__main__": 
    vcs = VersionControlSystem()
    command = sys.argv[1]
    if(command == 'init'):
        vcs.init()

    
    
