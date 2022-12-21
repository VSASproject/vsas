#The nal assembler
#take the root path and the manifest as input
#output the reassembled h264 file
#The manifest must be sorted
import json
import os
import logging


def manifest_to_list(manifest_path):
    with open(manifest_path, 'r') as myfile:
        data = myfile.read()
    # parse file
    obj = json.loads(data)
    return obj

def nal_assemble(data_root,manifest_path,output_path):
    man = manifest_to_list(manifest_path)
    with open(output_path, 'wb') as f1:
        logging.debug("refreshing the file")
    with open(output_path,'wb+') as f1:
        for nal in man:
            filename = nal["filename"]
            logging.debug("attaching nal"+filename)
            nal_path = os.path.join(data_root,filename)
            with open(nal_path,'rb') as f2:
                buf = f2.read(1000000)
                f1.write(buf)
    return 0

if __name__=="__main__":
    #data_root = "C:\\work\\nals"
    data_root = "C:\\Users\\walter\\source\\repos\\vpcc_attr_disassemplerV1\\vpcc_attr_disassemplerV1"
    nal_assemble(data_root,"manifest.json","a.h264")