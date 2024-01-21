import os

#To get the current path
current_path = os.getcwd()
print(f"This is current path",current_path)

#To change the directory
os.chdir('/Users/shahb/Documents/')

current_path = os.getcwd()
print(f"This is current path",current_path)

#To get all the files or folders in the directory
current_files = os.listdir()

for file in current_files:
    name,ext = os.path.splitext(file)
    print(name)
    print(ext)


