import os 
import sys 
import shutil
import hashlib
import json 
import datetime 
import base64

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
        
        vcs.add_with_subdirs(file)
        print("Files added successfully")
        
        

    elif(command == 'rmadd'):
        
        file = sys.argv[2]
        
        vcs.rmadd_with_subdirs(file)
        # print("File removed from added")
        
        

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

    elif(command == 'rmcommit'):
        vcs.rmcommit()    

    elif(command == 'help'):
        help()
    
    elif(command == 'test'):
        file = sys.argv[2]
        foldername =sys.argv[3]
        vcs.test_function(file,foldername)

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
        self.commit_path = os.path.join(self.object_path,'commit')
        self.content_path = os.path.join(self.object_path,'content')
        
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
        if not os.path.exists(self.commit_path):
            os.makedirs(self.commit_path) 
        if not os.path.exists(self.content_path):
            os.makedirs(self.content_path)           
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
    
    def add(self,file_path_full,file_path_relative):   

        if not os.path.exists(file_path_full):
            print(f"File {file_path_relative} does not exist.")
            return
        
        file_path_relative = file_path_relative if file_path_relative else os.path.normpath(
                file_path_full)
        self.add_to_json(file_path_relative)

    def index_file_update(self):
        with open(self.index_file,'r') as f1:
            data1 = json.load(f1)
        
        delKeys  = []
        for key in data1:
            if not os.path.exists(key):
                delKeys.append(key)
        for key in delKeys:
            del data1[key]
        with open(self.index_file,'w') as f1:
            json.dump(data1,f1)   

    def added_file_update(self):
        with open(self.add_file,'r') as f1:
            data1 = json.load(f1)
        
        delKeys  = []
        for key in data1:
            if not os.path.exists(key):
                delKeys.append(key)
        for key in delKeys:
            del data1[key]
        with open(self.add_file,'w') as f1:
            json.dump(data1,f1)   


    def add_with_subdirs(self,dir_path):
        
        if(self.not_init('.')):
            print("'.bhavu' folder is not initialized...")
            print("Run 'bhavu init' command to initialize")
            return
        
        if not os.path.isdir(dir_path):
            self.add(dir_path,dir_path)
            return 

        self.index_file_update()
        self.added_file_update()
        for root,dirs,files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d not in ['.bhavu','_pycache_','.git']]
            files[:] = [f for f in files if f not in ['vcs.py','.gitignore']]
            # print(files)

            for file in files:
                file_path_full = os.path.normpath(os.path.join(root,file))
                file_path_relative = os.path.normpath(file_path_full)
                self.add(file_path_full,file_path_relative )


    
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
    
    def rmadd_to_json(self,file):
        f1 = open(self.index_file,'r')
        f2 = open(self.add_file,'r')
            
        data1 = json.load(f1)
        data2 = json.load(f2)
                
        if file in data1:
            del data1[file]
        if file in data2:
            del data2[file]
            
        f1 = open(self.index_file,'w')
        f2 = open(self.add_file,'w')

        json.dump(data1,f1)
        json.dump(data2,f2)

    def rmadd(self,file_path_full,file_path_relative):
        if not os.path.exists(file_path_full):
            print(f"File {file_path_relative} is not removed.")
            return False
        file_path_relative = file_path_relative if file_path_relative else os.path.normpath(
                file_path_full)
        self.rmadd_to_json(file_path_relative)

    def rmadd_with_subdirs(self,dir_path):
        if(self.not_init('.')):
            print("'.bhavu' folder is not initialized...")
            print("Run 'bhavu init' command to initialize")
            return
        
        if not os.path.isdir(dir_path):
            bool = self.rmadd(dir_path,dir_path)
            if(bool == False):
                print("Add it first to stage it")
            return 

        for root,dirs,files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d not in ['.bhavu','_pycache_','.git']]
            files[:] = [f for f in files if f not in ['vcs.py','.gitignore']]
            # print(files)

            for file in files:
                file_path_full = os.path.normpath(os.path.join(root,file))
                file_path_relative = os.path.normpath(file_path_full)
                self.rmadd(file_path_full,file_path_relative )
        print("File removed from added")
            


    def status(self):
        if self.not_init('.'):
            print("'.bhavu' folder is not initialized...")
            print("Run 'bhavu init' command to initialize")
            return
        untracked_files=set()
        f1 = open(self.index_file,'r')
        data = json.load(f1)
        
        for root, dirs, files in os.walk(os.getcwd()):
            dirs[:] = [d for d in dirs if d not in [
                '.bhavu', '_pycache_', '.git']]
            # print("dirs: ", dirs)
            for file in files:
                file_path = os.path.join(root, file)
                
                hash = hash_file(file_path)
                rel_path = os.path.relpath(file_path, os.getcwd())

                if rel_path in data.keys() and data[rel_path] == hash:
                    status = 'Tracked'
                else:
                    status = 'Untracked'

                print(f"{status}: {rel_path}")

       

    def dump_data(self,commit_data):
        json_data = json.dumps(commit_data)
        return json_data
    
    def get_object_hash(self,commit_data):
        return hashlib.sha1(commit_data.encode('utf-8')).hexdigest()
    
    def get_object_path(self,object_hash):
        return os.path.join(self.commit_path,object_hash)
    
    def encrypt_data(self,file_path):

        with open(file_path,'r') as f:
                data = f.read()
                encrpted_data = base64.b64encode(data.encode()).decode('utf-8')
        return encrpted_data
    def decrypt_data(self,file_path):
        with open(file_path,'r') as f:
                data = f.read()
                decrpted_data = base64.b64decode(data).decode('utf-8')
        return decrpted_data    
         
    def save_object(self,commit_data):
        object_hash = self.get_object_hash(commit_data)
        object_path = self.get_object_path(object_hash)

        if not os.path.exists(object_path):
            with open(object_path,'w') as obj:           
                commit_data_encrypted = base64.b64encode(commit_data.encode()).decode('utf-8')
                obj.write(commit_data_encrypted)
        return object_hash

    def get_unadded_files(self,added):
        unadded_files=set()
        for root, dirs, files in os.walk(os.getcwd()):
            dirs[:] = [d for d in dirs if d not in [
                '.bhavu', '_pycache_', '.git']]
            files[:] = [f for f in files if f not in ['vcs.py', '.gitignore']]
            for file in files:
                file_path = os.path.join(root, file)
                hash = hash_file(file_path)
                rel_path = os.path.relpath(file_path, os.getcwd())
                if rel_path not in added or added[rel_path]!=hash:
                    unadded_files.add(rel_path)
        return unadded_files

    def commit(self,message,author):
        if self.not_init('.'):
            print("'.bhavu' folder is not initialized...")
            print("Run 'bhavu init' command to initialize")
            return

        with open(self.index_file,'r') as index_data:
                index = json.load(index_data)

        with open(self.add_file,'r') as add_data:
                added = json.load(add_data)
        
        unadded_files = self.get_unadded_files(added)
        
        if unadded_files:
            print("Unadded files are present.\n")
            for file in unadded_files:
                print("Untracked:",file)
            print()
            flag = input("Do you want to add the changes? (y/n): ")
            if flag == "y":
                self.add_with_subdirs('.')

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

        for file_path,file_hash in added.items():
            encrpted_data = self.encrypt_data(file_path)
            content_file = os.path.join(self.content_path,file_hash)
            if not os.path.exists(content_file):
                with open(content_file,'w') as f:
                    f.write(encrpted_data )           

        print(f"Commit successfully with <HEAD> hash : {commit_hash}")

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

    def get_head_commit(self):
        current_branch = "main" 
        head_path = os.path.join(self.branch_path,current_branch)
        current_head = os.path.join(head_path,'HEAD')
        with open(current_head,"r")as head:
            head_commit = head.read()
        
        head_commit = head_commit.strip().split("\n")[-1]
        return head_commit
        

    def get_second_head_commit(self):
        current_branch = "main" 
        head_path = os.path.join(self.branch_path,current_branch)
        current_head = os.path.join(head_path,'HEAD')
        with open(current_head,"r")as head:
            second_head_commit = head.read()
        
        second_head_commit = second_head_commit.strip().split("\n")
        if len(second_head_commit) > 1:
            second_head_commit = second_head_commit[-2]
        else:
            second_head_commit = ""
        return second_head_commit
    
    def get_commited_files(self,commit_file,type):
        data = self.decrypt_data(commit_file)
        data = json.loads(data)
        added_files = data[type]
        return added_files

    def test_function(self,destionation_path,folder_name):
        print("Test function")
        vcs.push(destionation_path,folder_name)

    def rmcommit(self):
        if self.not_init('.'):
            print("'.bhavu' folder is not initialized...")
            print("Run 'bhavu init' command to initialize")
            return
        #Currently implementing it for the main branch

        head_commit = self.get_head_commit()

        if head_commit == "":
            print("No commits to remove. Commit first to remove the last commit.")
            return

        second_head_commit = self.get_second_head_commit()
        
        self.clear_directory(os.getcwd())

        if head_commit and second_head_commit =="":
            head_path = os.path.join(self.branch_path,"main")
            head_file = os.path.join(head_path,'HEAD')
            head_commit_file = os.path.join(self.commit_path,head_commit)
            commited_files = get_commited_files(head_commit_file,"added")

            for file_path,file_hash in commited_files.items():
                content_file = os.path.join(self.content_path,file_hash)
                os.remove(content_file)

            os.remove(head_commit_file)
            with open(head_file, "w") as f:
                f.write("")
            with open(self.add_file,'w') as f:
                json.dump({}, f)
            with open(self.index_file,'w') as f:
                json.dump({}, f)
            print("Last commit removed successfully")
            return
            #if both head commit and second head commit are there
        else:
            
            head_path = os.path.join(self.branch_path,"main")
            head_file = os.path.join(head_path,'HEAD')
            #remove last line in head_file 

            with open(head_file, "r") as f:
                lines = f.readlines()
                lines = lines[:-1]
            with open(head_file, "w") as f:
                f.writelines(lines)            

            head_commit_file = os.path.join(self.commit_path,head_commit)
            commited_files = self.get_commited_files(head_commit_file,"added")

            for file_path,file_hash in commited_files.items():
                content_file = os.path.join(self.content_path,file_hash)
                os.remove(content_file)

            os.remove(head_commit_file)
            second_head_commit_file = os.path.join(self.commit_path,second_head_commit)

            commited_files = self.get_commited_files(second_head_commit_file,"index")
            for file_path,file_hash in commited_files.items():
                content_file = os.path.join(self.content_path,file_hash)
                encrpted_data = self.decrypt_data(content_file)
                with open(file_path,'w') as f:
                    f.write(encrpted_data)


            print("Last commit removed successfully")
            return

    def push(self,destionation_path,folder_name):
        if self.not_init('.'):
            print("'.bhavu' folder is not initialized...")
            print("Run 'bhavu init' command to initialize")
            return
        
        if not os.path.exists(destionation_path):
            os.makedirs(destionation_path)
        # destionation_path = os.path.join(destionation_path,"pushed_files")
        destionation_path = os.path.join(destionation_path,folder_name)
        if not os.path.exists(destionation_path):
            os.makedirs(destionation_path)

        head_commit = self.get_head_commit()
        head_commit_file = os.path.join(self.commit_path,head_commit)
        commited_files = self.get_commited_files(head_commit_file,'index')
        for file_path,file_hash in commited_files.items():
                content_file = os.path.join(self.content_path,file_hash)
                encrpted_data = self.decrypt_data(content_file)
                with open(os.path.join(destionation_path,file_path),'w') as f:
                    f.write(encrpted_data)    
                
        print("Files pushed successfully")
        

if __name__ == "__main__": 
    vcs = VersionControlSystem()
    main()
    
    
