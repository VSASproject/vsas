#The builder takes a directory as the input
#Then output a json manifest including all the files in the directory

#INPUT: the path to the directory that includes all the mesh files
#OUTPUT: a json string that includes all the file's filename
import os
import numpy as np
import json
from operator import itemgetter

def build_man(root_path):
    filename_list = []
    nal_no_list = []
    type_list = []
    for filename in os.listdir(root_path):
        f = os.path.join(root_path, filename)
        if os.path.isfile(f):
            filename_list.append(filename)
    filename_list = np.array(filename_list)
    filename_list.sort()
    json_list = []
    for filename in filename_list:
        fragment_type = -1
        if filename[0] == 'i':
            fragment_type = 0
        elif filename[0] == 'p':
            fragment_type = 1
        nal_no = filename.split("_")[1].split('.')[0]
        nal_no = int(nal_no)
        #print(nal_no)
        #print(fragment_type)
        #print(filename)
        json_list.append({"nal_no":nal_no,"filename":filename,"type":fragment_type})
    json_list.sort(key=itemgetter('nal_no'))
    return json_list

if __name__=="__main__":
    path = "C:\\work\\nals"
    result = build_man(path)
    jsonStr = json.dumps(result)
    manifest_path = "manifest.json"
    with open(manifest_path,'w') as f1:
        f1.write(jsonStr)