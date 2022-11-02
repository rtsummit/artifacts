
import os
import shutil
import filecmp

def file_compare(file_name:str, target_path:str):
    same = False
    try:
        same = filecmp.cmp(file_name, target_path + '/' + file_name)
    except:
        pass

    return same

def file_move(file_name:str, target_path:str):
    try:
        os.remove(target_path + '/' + file_name)
    except:
        pass

    shutil.move(file_name, target_path)
