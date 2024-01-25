import os
import shutil


current_path = input("Enter the path that you want to organize:")
os.chdir(current_path)

for file in os.listdir():
    if(os.path.isdir(file)):
        continue
    if(file =='.git'):
        continue
    name,ext = os.path.splitext(file)
    
    new_path = f"{current_path}/{ext}" 
    print(new_path)
    if not os.path.exists(new_path):
        print("does not exist")
        os.mkdir(new_path)     
    else:
        print("does exist")
    shutil.move(file,new_path)

    