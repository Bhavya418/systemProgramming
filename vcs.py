import os 
import sys 
import shutil
import hashlib
import json 
import datetime 
import base64

#importing the other files and classes 
from hash import HashCalculator
from file_handler import FileHandler
from utility import Utility
from help import help
from file_functions import Filefunctions

class VersionControlSystem:

    def __init__(self,repo_path=".bhavu"):
        try:
            #initializing the paths
            self.repo_path = repo_path
            self.object_path = os.path.join(repo_path,'objects')
            self.branch_path = os.path.join(repo_path,'branches')
            self.index_file = os.path.join(repo_path,'index.json')
            self.add_file = os.path.join(repo_path,'added.json')
            self.user_file = os.path.join(repo_path,'user.txt')
            self.commit_path = os.path.join(self.object_path,'commit')
            self.content_path = os.path.join(self.object_path,'content')
            #class objects
            self.hash = HashCalculator()
            self.file_handler = FileHandler()
            self.file_function = Filefunctions()
            self.utility = Utility()
        except Exception as e:
            print(f"An error occurred while initializing the VersionControlSystem: {str(e)}")

    # get the current user    
    def get_current_user(self):
        try:
            user = self.file_handler.read_file(self.user_file)
            user = user.strip().split()[2:]
            user_name = ""
            for value in user: 
                user_name = user_name + " " + value
            return user_name
        except Exception as e:
            print(f"An error occurred while getting the current user: {str(e)}")
            return None

    # change the current user
    def change_user(self, user_name):
        try:
            date_time = self.utility.get_date_time()
            self.file_handler.write_file(self.user_file, f"{date_time} {user_name}")
        except Exception as e:
            print(f"An error occurred while changing the user: {str(e)}")

    #create a new branch    
    def create_branch(self, branch_name="main"):
        try:
            branch_path_name = os.path.join(self.branch_path, branch_name)

            if not self.file_function.check_file_exists(branch_path_name):
                os.makedirs(branch_path_name)

            # create a file to store the latest commit hash
            branch_file = os.path.join(branch_path_name, 'HEAD')
            if not self.file_function.check_file_exists(branch_file):
                self.file_handler.write_file(branch_file, "")
        except Exception as e:
            print(f"An error occurred while creating the branch: {str(e)}")


    def init(self):
        try:
            if self.file_function.check_file_exists(self.repo_path):
                print(f"Reinitialized empty repository at : {os.getcwd()}")
                return

            if not self.file_function.check_file_exists(self.repo_path):
                os.makedirs(self.repo_path)

            
            if not self.file_function.check_file_exists(self.branch_path):
                os.makedirs(self.branch_path)

            if not self.file_function.check_file_exists(self.object_path):
                os.makedirs(self.object_path)    
            if not self.file_function.check_file_exists(self.commit_path):
                os.makedirs(self.commit_path) 
            if not self.file_function.check_file_exists(self.content_path):
                os.makedirs(self.content_path)           
            #creating the main branch
            self.create_branch('main')
            
            files_to_be_created = [self.index_file,self.add_file]
            
            for file in files_to_be_created:
                if not self.file_function.check_file_exists(file):
                    self.utility.dump_json({}, file)
                    
            if not self.file_function.check_file_exists(self.user_file):
                    
                user_name = input("Enter your username: ")
                if user_name == "":
                    user_name = "Unknown"
                date_time = self.utility.get_date_time()
                self.file_handler.write_file(self.user_file, f"{date_time} {user_name}") 

            print(f"A new empty bhavu repository created successfully at :{os.getcwd()}")

        except Exception as e:
            print(f"An error occurred while initializing the repository: {str(e)}")
    
    
    
    def add_to_json(self, file):
        try:
            data1 = self.utility.read_json(self.index_file)
            data2 = self.utility.read_json(self.add_file)
                    
            if self.file_function.check_dir(file):
                hash = self.hash.md5_dir(file)
            else:
                hash = self.hash.hash_file(file)
                
            data1[file] = hash
            data2[file]=hash
            self.utility.dump_json(data1, self.index_file)
            self.utility.dump_json(data2, self.add_file)
        
        except Exception as e:
            print(f"An error occurred while adding the file to JSON: {str(e)}")

    
    def add(self, file_path_full, file_path_relative):   
        try:
            if not self.file_function.check_file_exists(file_path_full):
                print(f"File {file_path_relative} does not exist.")
                return
            
            file_path_relative = file_path_relative if file_path_relative else os.path.normpath(file_path_full)
            self.add_to_json(file_path_relative)
        
        except Exception as e:
            print(f"An error occurred while adding the file: {str(e)}")

    
    def add_with_subdirs(self, dir_path):
        try:
            if self.utility.not_init('.'):
                self.utility.printLine()
                return

            if not self.file_function.check_dir(dir_path):
                self.add(dir_path, dir_path)
                return

            self.file_function.file_update(self.index_file)
            self.file_function.file_update(self.add_file)

            for root, dirs, files in os.walk(dir_path):
                dirs[:] = [d for d in dirs if d not in ['.bhavu', '_pycache_', '.git']]
                files[:] = [f for f in files if f not in ['vcs.py', '.gitignore']]

                for file in files:
                    file_path_full = os.path.normpath(os.path.join(root, file))
                    file_path_relative = os.path.normpath(file_path_full)
                    self.add(file_path_full, file_path_relative)
        
        except Exception as e:
            print(f"An error occurred while adding files with subdirectories: {str(e)}")

        
    def rmadd_to_json(self, file):
        try:
            data1 = self.utility.read_json(self.index_file)
            data2 = self.utility.read_json(self.add_file)
            
            if file in data1:
                del data1[file]
            if file in data2:
                del data2[file]
            
            self.utility.dump_json(data1, self.index_file)
            self.utility.dump_json(data2, self.add_file)
        
        except Exception as e:
            print(f"An error occurred while removing the file from JSON: {str(e)}")

    def rmadd(self,file_path_full,file_path_relative):
        try:
            if not self.file_function.check_file_exists(file_path_full):
                print(f"File {file_path_relative} is not added.")
                return False
            file_path_relative = file_path_relative if file_path_relative else os.path.normpath(
                    file_path_full)
            self.rmadd_to_json(file_path_relative)
        except Exception as e:
            print(f"An error occurred while removing the file: {str(e)}")

    def rmadd_with_subdirs(self, dir_path):
        try:
            if self.utility.not_init('.'):
                self.utility.printLine()
                return

            if not self.file_function.check_dir(dir_path):
                bool = self.rmadd(dir_path, dir_path)
                if bool == False:
                    print("add the file first to stage it")
                return

            for root, dirs, files in os.walk(dir_path):
                dirs[:] = [d for d in dirs if d not in ['.bhavu', '_pycache_', '.git']]
                files[:] = [f for f in files if f not in ['vcs.py', '.gitignore']]

                for file in files:
                    file_path_full = os.path.normpath(os.path.join(root, file))
                    file_path_relative = os.path.normpath(file_path_full)
                    self.rmadd(file_path_full, file_path_relative)
            print("File removed from stage successfully...")
        except Exception as e:
            print(f"An error occurred while removing the file from stage: {str(e)}")
        

    def status(self):
        try:
            if self.utility.not_init('.'):
                self.utility.printLine()
                return
            data = self.utility.read_json(self.index_file)

            for root, dirs, files in os.walk(os.getcwd()):
                dirs[:] = [d for d in dirs if d not in [
                    '.bhavu', '_pycache_', '.git']]
                # print("dirs: ", dirs)
                for file in files:
                    file_path = os.path.join(root, file)

                    hash = self.hash.hash_file(file_path)
                    rel_path = os.path.relpath(file_path, os.getcwd())

                    if rel_path in data.keys() and data[rel_path] == hash:
                        status = 'Tracked'
                    else:
                        status = 'Untracked'

                    print(f"{status}: {rel_path}")
        except Exception as e:
            print(f"An error occurred while checking the status: {str(e)}")
          
         
    def commit(self, message, author):
        try:
            if self.utility.not_init('.'):
                self.utility.printLine()
                return
            index = self.utility.read_json(self.index_file)
            added = self.utility.read_json(self.add_file)

            unadded_files = self.file_function.get_unadded_files(added)

            if unadded_files:
                print("unstaged files are present.\n")
                for file in unadded_files:
                    print("Untracked:", file)
                print()
                flag = input("Do you want to add the changes? (y/n): ")
                if flag == "y":
                    self.add_with_subdirs('.')

            index = self.utility.read_json(self.index_file)
            added = self.utility.read_json(self.add_file)

            if not added:
                print("No changes to commit")
                return

            timestamp = self.utility.get_date_time()

            commit_data = {
                "timestamp": timestamp,
                "message": message,
                "author": author,
                "index": index,
                "added": added,
            }

            commit_file = self.utility.dump_data(commit_data)

            commit_hash = self.file_function.save_object(self.commit_path, commit_file)
            self.utility.dump_json({}, self.add_file)

            # Currently implementing it for the main branch
            current_branch = "main"
            head_path = os.path.join(self.branch_path, current_branch)
            current_head = os.path.join(head_path, 'HEAD')

            self.file_handler.append_file(current_head, "{}\n".format(commit_hash))

            for file_path, file_hash in added.items():
                encrpted_data = self.utility.encrypt_data(file_path)
                content_file = os.path.join(self.content_path, file_hash)
                if not os.path.exists(content_file):
                    with open(content_file, 'w') as f:
                        f.write(encrpted_data)

            print(f"Commit successfully with <HEAD> hash: {commit_hash}")
        except Exception as e:
            print(f"An error occurred while committing: {str(e)}")
  
    def checkout(self, commit_hash):
        try:
            if self.utility.not_init('.'):
                self.utility.printLine()
                return

            current_branch = "main"
            head_commit = self.utility.get_head_commit(current_branch, self.branch_path)

            if head_commit == commit_hash:
                print("already at the commit")
                return

            head_file = os.path.join(self.branch_path, "main", 'HEAD')

            head_commit = self.file_handler.read_file(head_file)
            head_commit = head_commit.strip().split("\n")

            if commit_hash not in head_commit:
                print("commit hash not found")
                return
            # try to make the commit_index as the head commit but will do it afterwards
            # commit_index = head_commit.index(commit_hash)

            head_commit_file = os.path.join(self.commit_path, commit_hash)

            commited_files = self.utility.get_commited_files(head_commit_file, "index")

            self.file_function.clear_directory(os.getcwd())

            for file_path, file_hash in commited_files.items():
                file_path = os.path.join(os.getcwd(), file_path)
                dir_name = os.path.dirname(file_path)
                if not self.file_function.check_file_exists(dir_name):
                    os.makedirs(dir_name)

            for file_path, file_hash in commited_files.items():
                content_file = os.path.join(self.content_path, file_hash)
                decrpyted_data = self.utility.decrypt_data_file_path(content_file)
                self.file_handler.write_file(file_path, decrpyted_data)

            self.utility.dump_json(commited_files, self.index_file)

            print(f"checked out successfully to {commit_hash}")
        except Exception as e:
            print(f"An error occurred during checkout: {str(e)}")


    def rmcommit(self):

        try:
            if self.utility.not_init('.'):
                self.utility.printLine()
                return
            current_branch = "main"    
            #Currently implementing it for the main branch
            head_commit = self.utility.get_head_commit(current_branch, self.branch_path)

            if head_commit == "":
                print("No commits to remove. Commit first to remove the last commit.")
                return

            second_head_commit = self.utility.get_second_head_commit(current_branch, self.branch_path)
            
            self.file_function.clear_directory(os.getcwd())
            head_file = os.path.join(self.branch_path,"main",'HEAD')
            head_commit_file = os.path.join(self.commit_path,head_commit)

            if head_commit and second_head_commit =="":
                
                commited_files = self.file_function.get_commited_files(head_commit_file,"added")

                for file_path,file_hash in commited_files.items():
                    content_file = os.path.join(self.content_path,file_hash)
                    os.remove(content_file)

                os.remove(head_commit_file)
                self.file_handler.write_file(head_file, "")
                self.utility.dump_json({}, self.add_file)
                self.utility.dump_json({}, self.index_file)
                print("Last commit removed successfully")
                return

                #if both head commit and second head commit are there
            else:
                #remove last line in head_file 
                self.utility.remove_last_line(head_file)          
                commited_files = self.file_function.get_commited_files(head_commit_file,"added")

                for file_path,file_hash in commited_files.items():
                    content_file = os.path.join(self.content_path,file_hash)
                    os.remove(content_file)

                os.remove(head_commit_file)

                second_head_commit_file = os.path.join(self.commit_path,second_head_commit)
                commited_files = self.get_commited_files(second_head_commit_file,"index")

                for file_path,file_hash in commited_files.items():
                    file_path = os.path.join(os.getcwd(),file_path)
                    dir_name= os.path.dirname(file_path)
                    if not self.file_function.check_file_exists(dir_name):
                        os.makedirs(dir_name)   

                for file_path,file_hash in commited_files.items():
                    content_file = os.path.join(self.content_path,file_hash)
                    decrypted_data = self.utility.decrypt_data_file_path(content_file)
                    self.file_handler.write_file(file_path,decrypted_data)

                self.utility.dump_json(commited_files,self.index_file)

                print("Last commit removed successfully")
                return
        except Exception as e:
            print(f"An error occurred during commit removal: {str(e)}")

    def push(self, destionation_path, folder_name):
        try:
            if self.utility.not_init('.'):
                self.utility.printLine()
                return
            
            if not self.file_function.check_file_exists(destionation_path):
                os.makedirs(destionation_path)

            destionation_path = os.path.join(destionation_path, folder_name)
            if not self.file_function.check_file_exists(destionation_path):
                os.makedirs(destionation_path)

            head_commit = self.utility.get_head_commit("main", self.branch_path)
            if head_commit == "":
                quit("No commits to push. Commit first to push the files.")
                return

            head_commit_file = os.path.join(self.commit_path, head_commit)
            commited_files = self.utility.get_commited_files(head_commit_file, 'index')
            for file_path, file_hash in commited_files.items():
                content_file = os.path.join(self.content_path, file_hash)
                encrypted_data = self.utility.decrypt_data_file_path(content_file)
                file_path_push = os.path.join(destionation_path, file_path)
                dir_path = os.path.dirname(file_path_push)
                if not self.file_function.check_file_exists(dir_path):
                    os.makedirs(dir_path)
                self.file_handler.write_file(file_path_push, encrypted_data)

            print("Files pushed successfully")
        except Exception as e:
            print(f"An error occurred while pushing files: {str(e)}")
    

    def log(self):
        try:
            if self.utility.not_init('.'):
                self.utility.printLine()
                return

            head_path = os.path.join(self.branch_path, "main", 'HEAD')
            head_commit = self.file_handler.read_file(head_path)
            head_commit = head_commit.strip().split("\n")

            if head_commit == "":
                print("No commits to show")
                return

            for commit in head_commit:
                commit_file = os.path.join(self.commit_path, commit)
                data = self.utility.decrypt_data_file_path(commit_file)
                data = self.utility.read_data(data)
                print(f"commit: {commit}")
                print(f"Author: {data['author']}")
                print(f"Date: {data['timestamp']}")
                print(f"Message: {data['message']}")
                print()
                print("Added/Modifies files:")
                print("----------------------")
                for file in data['added']:
                    print(file, "\n")
                print("All files:")
                print("----------------------")
                for file in data['index']:
                    print(file, "\n")

            print("Log successfully shown")
        except Exception as e:
            print(f"An error occurred while showing the log: {str(e)}")


def main():
    if len(sys.argv) < 2:
        help()
        sys.exit(1)

    command = sys.argv[1]

    if command == 'init':
        if len(sys.argv) != 2:
            print("Error: Too many arguments.")
            print("Usage: bhavu init")
            sys.exit(1)

        vcs.init()

    elif command == 'add':
        if len(sys.argv) != 3:  
            print("Error: Too many arguments.")
            print("Usage: bhavu add <file>")
            sys.exit(1)
        file = sys.argv[2]
        vcs.add_with_subdirs(file)
        print("File/s added successfully")

    elif command == 'rmadd':
        if len(sys.argv) != 3:
            print("Error: Too many arguments.")
            print("Usage: bhavu rmadd <file>")
            sys.exit(1)
        file = sys.argv[2]
        vcs.rmadd_with_subdirs(file)

    elif command == 'status':
        if len(sys.argv) != 2:
            print("Error: Too many arguments.")
            print("Usage: bhavu status")
            sys.exit(1)
        vcs.status()

    elif command == 'commit':
        if len(sys.argv) < 3:
            print("Error: Too few arguments.")
            print("Usage: bhavu commit -m <message>")
            sys.exit(1)
        if "-m" not in sys.argv:
            print("Error: Please provide a commit message using the -m flag.")
            sys.exit(1)
        message_index = sys.argv.index('-m') + 1
        message = sys.argv[message_index]
        user = vcs.get_current_user()
        vcs.commit(message, user)

    elif command == 'rmcommit':
        if len(sys.argv) != 2:
            print("Error: Too many arguments.")
            print("Usage: bhavu rmcommit")
            sys.exit(1) 
        vcs.rmcommit()

    elif command == 'help':
        if len(sys.argv)>3:
            print("Error: Too many arguments.")
            print("Usage: bhavu help")
            sys.exit(1)
        help()

    elif command == 'push':
        if len(sys.argv) != 4:
            print("Error: Please provide a path to push the files.")
            print("Usage: bhavu push <path>")
            sys.exit(1)
        file = sys.argv[2]
        foldername = sys.argv[3]
        vcs.push(file, foldername)

    elif command == 'user':
        if len(sys.argv) < 3:
            print("Error: Please provide a command.")
            sys.exit(1)
        sub_command = sys.argv[2]
        if sub_command == 'show':
            print("Author:", vcs.get_current_user())
        elif sub_command == 'set':
            user_name = sys.argv[3]
            vcs.change_user(user_name)
            print(f"Author changed to '{user_name}' successfully")
        else:
            help()

    elif command == 'checkout':
        if len(sys.argv) != 3:
            print("Error: Too many arguments.")
            print("Usage: bhavu checkout <commit>")
            sys.exit(1)
        commit_hash = sys.argv[2]
        vcs.checkout(commit_hash)

    elif command == 'log':
        if len(sys.argv) != 2:
            print("Error: Too many arguments.")
            print("Usage: bhavu log")
            sys.exit(1)
        vcs.log()

    else:
        help()

if __name__ == "__main__": 
    vcs = VersionControlSystem()
    main()
    
    
