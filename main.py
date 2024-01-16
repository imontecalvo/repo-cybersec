import os
import hashlib

def get_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as file:
        f = file.read()
        hash_md5.update(f)
    return hash_md5.hexdigest()

def get_current_hashes(path):
    hashes = {}
    for file in os.listdir(path):
        hash = get_hash(path+file)
        hashes[file] = hash

    return hashes

path = './PyJ Systems/'

original_hashes = {
    "copia.sh":"90965b0eb20e68b7d0b59accd2a3b4fd",
    "log.txt":"0b29406e348cd5f17c2fd7b47b1012f9",
    "pass.txt":"6d5e43a730490d75968279b6adbd79ec",
    "plan-A.txt":"129ea0c67567301df1e1088c9069b946",
    "plan-B.txt":"4e9878b1c28daf4305f17af5537f062a",
    "script.py":"66bb9ec43660194bc066bd8b4d35b151",
}


current_hashes = get_current_hashes(path)


for k,v in current_hashes.items():
    if original_hashes[k] != v:
        print(f"File {k} has been changed")
        break
