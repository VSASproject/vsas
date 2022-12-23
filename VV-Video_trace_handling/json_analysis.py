import json
import os

with open('manifest_nil.json', 'r') as jsonfile:
    json_string = json.load(jsonfile)


size_list = []

for element in json_string:
    filename = element['filename']
    size = os.path.getsize("Mixed_lox_h264/"+filename)
    size_list.append(size)
print(size_list)