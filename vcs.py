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
        

    elif(command == 'add'):
        
        file = sys.argv[2]
        if(file =='.'):
            vcs.add_with_subdirs(file)
            print("Files added successfully")
        
        else: 
            vcs.add(file)
            print("File added successfully")

    elif(command == 'status'):
        vcs.status()    

    elif(command == 'commit'):
        if "-m" not in sys.argv:
            print("Error: Please provide a commit message using  flag -m.")
            sys.exit(1)
        message_index = sys.argv.index('-m')+1
        message = sys.argv[message_index]
        user = vcs.get_current_user()
        vcs.commit(message,user)
        
        

    elif(command == 'help'):
        help()
    
    else:
        help()



class VersionControlSystem:

    def __init__(self,repo_path=".bhavu"):

        self.repo_path = repo_path
        self.object_path = os.path.join('.bhavu','objects')
        self.branch_path = os.path.join('.bhavu','branches')
        
        self.index_file = os.path.join(repo_path,'index.json')
        self.add_file = os.path.join(repo_path,'added.json')
        self.user_file = os.path.join(repo_path,'user.txt')
        
    def not_init(self,dir_path):
        files_and_dirs = os.listdir(dir_path)
        if '.bhavu' not in files_and_dirs:
             
            return True   
        return False

    def get_current_user(self):
        with open(self.user_file,'r') as current_user:
            user = current_user.read()
        user =user.strip().split()[2:]
        user_name=""
        for value in user: 
            user_name = user_name +" " + value
        return user_name

    def create_branch(self,branch_name):
        branch_path_name = os.path.join(self.branch_path,branch_name)

        if not os.path.exists(branch_path_name):
            os.makedirs(branch_path_name)

        #create a file to store the latest commit hash
        branch_file = os.path.join(branch_path_name,'HEAD')
        if not os.path.exists(branch_file):
            with open(branch_file,'w') as w:
                w.write("")


    def init(self):
        if os.path.exists(self.repo_path):
            print("Reinitialized empty repository")
            return

        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)

        
        if not os.path.exists(self.branch_path):
            os.makedirs(self.branch_path)

        if not os.path.exists(self.object_path):
            os.makedirs(self.object_path)    
    
        #creating the main branch
        self.create_branch('main')
        
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
        print("A new empty bhavu repository created")
    
    def add(self,file):   

        if not os.path.exists(file):
            print(f"File {file} does not exist.")
        else:

            self.add_to_json(file)
            # print("File added successfully")

    def add_with_subdirs(self,dir_path):
        
        if(self.not_init('.')):
            print("'.bhavu' folder is not initialized...")
            print("Run 'bhavu init' command to initialize")
            return
        
        if not os.path.isdir(dir_path):
            self.add(dir_path)
            return 
        files_and_dirs= [os.path.join(dir_path,file) for file in os.listdir(dir_path)]
        for file in files_and_dirs:
            filename = os.path.basename(file)
            if(filename=='.git'):
                continue
            if(filename=='.bhavu'):
                continue
            
            if os.path.isdir(file):
                # print(file)                
                self.add_with_subdirs(file)
            else:
                self.add(file)



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
        if self.not_init('.'):
            print("'.bhavu' folder is not initialized...")
            print("Run 'bhavu init' command to initialize")
            return
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
            if file in data.keys():
                if data[file] != hash:
                    untrackedFiles[file]='Untracked'
                else:
                    untrackedFiles[file]='Tracked'
                    

            else:
                untrackedFiles[file]='Untracked'
        
        for file in untrackedFiles:
            print(f"{untrackedFiles[file]}: {file}")

    def dump_data(self,commit_data):
        json_data = json.dumps(commit_data)
        return json_data
    
    def get_object_hash(self,commit_data):
        return hashlib.sha1(commit_data.encode('utf-8')).hexdigest()
    
    def get_object_path(self,object_hash):
        return os.path.join(self.object_path,object_hash)
    
    def save_object(self,commit_data):
        object_hash = self.get_object_hash(commit_data)
        object_path = self.get_object_path(object_hash)

        if not os.path.exists(object_path):
            with open(object_path,'w') as obj:
                obj.write(commit_data)
        return object_hash


    def commit(self,message,author):
        if self.not_init('.'):
            print("'.bhavu' folder is not initialized...")
            print("Run 'bhavu init' command to initialize")
            return

        with open(self.index_file,'r') as index_data:
                index = json.load(index_data)

        with open(self.add_file,'r') as add_data:
                added = json.load(add_data)
        
        if not added :
            print("No changes to commit")
            return 
        
        timestamp= (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

        commit_data ={
            "timestamp":timestamp,
            "message": message,
            "author": author,
            "index": index,
            "added": added,        
        }

        commit_file = self.dump_data(commit_data)
        
        commit_hash = self.save_object(commit_file)      

        with open(self.add_file,'w') as f:
            json.dump({}, f)
        
        #Currently implementing it for the main branch
        current_branch = "main" 
        head_path = os.path.join(self.branch_path,current_branch)
        current_head = os.path.join(head_path,'HEAD')
        with open(current_head,"a")as head:
            head.write(commit_hash+"\n")            

        print(f"Commit successfully with <HEAD> hash : {commit_hash}")


        

if __name__ == "__main__": 
    vcs = VersionControlSystem()
    main()
    
    
