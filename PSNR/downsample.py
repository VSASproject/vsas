import open3d as o3d
import numpy as np


pcd = o3d.io.read_point_cloud("Ply/Longdress/longdress_vox10_1051.ply")
Down_Sample_Rate = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
for down_sample_rate in Down_Sample_Rate:
    pcdFileName = "Ply/Longdress/longdress_" + str(round(1/down_sample_rate, 2)) + ".ply"
    down_pcd = pcd.uniform_down_sample(down_sample_rate)
    down_pcd.points = down_pcd.points.astype(np.float32)
    o3d.io.write_point_cloud(pcdFileName, down_pcd, compressed=True, write_ascii=True)
