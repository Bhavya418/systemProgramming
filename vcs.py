import os 
import sys 
import shutil
import hashlib
import json 
import datetime 

def help():
        print("Bhavu - A Version Control System")
        print("---------------------------------")
        print("Usage:")
        print("  bhavu init                - Initialize a new bhavu repository")
        print("  bhavu add <file>          - Add a file to the index")
        print("  bhavu commit -m <message> - Commit changes with a message")
        print("  bhavu rmadd <file>        - remove a file from the index")
        print("  bhavu rmcommit            - remove last commit")
        print("  bhavu log                 - Display commit log")
        print("  bhavu checkout <commit>   - Checkout a specific commit")
        print("  bhavu help                - to see this usage help")
        print("  bhavu status              - to see status")
        print("  bhavu user show           - to see present user")
        print("  bhavu user set <username> - to change user")
        print("  bhavu push <path>         - to push your file to another folder")
        print("---------------------------------")
        print("Created by - Bhavya Shah")
        print("---------------------------------")

def md5_update_from_dir(directory, hash):
    assert Path(directory).is_dir()
    for path in sorted(Path(directory).iterdir(), key=lambda p: str(p).lower()):
        hash.update(path.name.encode())
        if path.is_file():
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash.update(chunk)
        elif path.is_dir():
            hash = md5_update_from_dir(path, hash)
    return hash


def md5_dir(directory):
    return md5_update_from_dir(directory, hashlib.md5()).hexdigest()            


def hash_file(filename):
    h = hashlib.md5()
    with open(filename,'rb') as file:
        #loop till the end of the file
        chunk =0
        while chunk != b'':
            #read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()        


def main():

    if(len(sys.argv)<2):
        help()
        sys.exit(1)

    command = sys.argv[1]

    if(command == 'init'):
        vcs.init()
        print("A new empty bhavu repository created")

    elif(command == 'add'):
        
        file = sys.argv[2]
        vcs.add(file)

    elif(command == 'status'):
        vcs.status()    

    elif(command == 'help'):
        help()
    
    else:
        help()



class VersionControlSystem:

    def __init__(self,repo_path=".bhavu"):

        self.repo_path = repo_path
        self.object_path = os.path.join('.bhavu','objects')
        self.branch_path = os.path.join('.bhavu','branches')
        self.main_branch = os.path.join(self.branch_path,'main')
        self.index_file = os.path.join(repo_path,'index.json')
        self.add_file = os.path.join(repo_path,'added.json')
        self.user_file = os.path.join(repo_path,'user.txt')
        

    def init(self):

        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
        
        if not os.path.exists(self.branch_path):
            os.makedirs(self.branch_path)

        if not os.path.exists(self.object_path):
            os.makedirs(self.object_path)    
    
        #creating the main branch

        if not os.path.exists(self.main_branch):
            os.makedirs(self.main_branch)

        files_to_be_created = [self.index_file,self.add_file]
        

        for file in files_to_be_created:
            if not os.path.exists(file):
                with open(file, "w") as index:
                    json.dump({}, index)   


        if not os.path.exists(self.user_file):
                
            user_name = input("Enter your username: ")
            if user_name == "":
                user_name = "Unknown"
            date_time = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S") 
            with open(self.user_file, "w") as user_data:
                user_data.write(f"{date_time} {user_name}")

    
    def add(self,file):
        if not os.path.exists(file):
            print(f"File {file} does not exist.")
        else:
            self.add_to_json(file)
            print("File added successfully")
            

    def add_to_json(self,file):
        f1 = open(self.index_file,'r')
        f2 = open(self.add_file,'r')
            
        data1 = json.load(f1)
        data2 = json.load(f2)
                
        if(os.path.isdir(file)):
            hash = md5_dir(file)
        else:
            hash = hash_file(file)
            
        data1[file] = hash
        data2[file] = hash
            
        f1 = open(self.index_file,'w')
        f2 = open(self.add_file,'w')

        json.dump(data1,f1)
        json.dump(data2,f2)
    
    def status(self):
        untracked_files=set()
        f1 = open(self.index_file,'r')
        data = json.load(f1)
        
        
        for file in os.listdir():
            if(os.path.isdir(file)):
                continue
            if(file =='.bhavu'):
                continue
            untracked_files.add(file)

        untrackedFiles = {}
        for file in untracked_files:
            hash = hash_file(file)
            if(data[file]):
                if data[file] != hash:
                    untrackedFiles[file]='modified'
            else:
                untrackedFiles[file]='added'
        for file in untrackedFiles:
            print(f"{untrackedFiles[file]}:   {file}")
        



        

        


        

if __name__ == "__main__": 
    vcs = VersionControlSystem()
    main()
    
    
