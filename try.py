import json
import os
import shutil
import hashlib
from pathlib import Path
            
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


current_path = input("Enter the path that you want to organize:")
os.chdir(current_path)

data = []

with open(".json",'w') as out_file:

    for file in os.listdir():
        if file == '.git':
            continue
        if(os.path.isdir(file)):
            hash = md5_dir(file)
        else:
            hash = hash_file(file)
        name,ext = os.path.splitext(file)
        # print(hash)
        file_size = os.path.getsize(file)
        data1 = { 'filename':name, 'filesize':file_size,'filehash':hash}
        data.append(data1)
    json.dump(data,out_file)
    print("Written")
# import datetime

# today = datetime.date.today()
# tomorrow = today + datetime.timedelta(days = 1)

# data = [{
#     "date": str(tomorrow),
#     "price": {
#         "amount": 15100
#     }
# }]

# data1 ={
#     "date": str(tomorrow),
#     "price": {

#         "amount": 15100
#     }
# }