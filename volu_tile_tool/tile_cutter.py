#created by walter on 2022/04/12, 12:47
#cut the ply into smaller pieces

import os
import math

NUM_CELL = 8

def tile_cut(poly_path,target_path):
    poly_name = os.path.basename(poly_path)
    file_size = os.path.getsize(poly_path)
    tile_size = math.ceil(file_size / NUM_CELL)
    buf_bin = bytearray(tile_size)
    try:
        with open(poly_path,'rb') as f1:
            for cell in range(NUM_CELL):
                buf_bin = f1.read(tile_size)
                #print(buf_bin)
                tile_poly_name = poly_name + "_" + str(cell) + ".tile"
                target_poly_path = os.path.join(target_path,tile_poly_name)
                with open(target_poly_path,'wb') as f2:
                    f2.write(buf_bin)
    except:
        print("Failed to cut tile...")
        return False
    return True

def tile_assemble(poly_path,target_path):
    try:
        target_poly_path = os.path.join(target_path,os.path.basename(poly_path))
        print(target_poly_path)
        with open(target_poly_path,'wb') as f1:
            for cell in range(NUM_CELL):
                source_poly_path = poly_path + "_" + str(cell) + ".tile"
                #print(source_poly_path)
                source_poly_size = os.path.getsize(source_poly_path)
                #print(source_poly_size)
                with open(source_poly_path, 'rb') as f2:
                    buf_bin = f2.read(source_poly_size)
                    f1.write(buf_bin)
    except:
        print("Failed to assemble tile...")
        return False
    return True

if __name__=="__main__":
    path = "E:\\volumetric\\dataset\\fvv\\BreakDancers\\TrackedMeshes"
    target_path="."
    filename = "Mesh-F00001.ply"
    poly_path = os.path.join(path,filename)
    ok = tile_cut(poly_path,target_path)
    if ok:
        print("Tile Succeded " + poly_path)
    local_path = "."
    local_poly_path = os.path.join(local_path,filename)
    ok = tile_assemble(local_poly_path,target_path)
    if ok:
        print("Tile Assembled" + target_path+os.path.basename(poly_path))
