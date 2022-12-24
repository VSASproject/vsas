import open3d as o3d
import csv
import numpy as np

def RGB2YUV(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]

def psnr_space(original_pcd, downsampled_pcd):
    original_pcd = o3d.io.read_point_cloud(original_pcd)
    downsampled_pcd = o3d.io.read_point_cloud(downsampled_pcd)
    dists = original_pcd.compute_point_cloud_distance(downsampled_pcd)
    ori_length = len(original_pcd.points)
    sum = 0
    for d in dists:
        mse = np.mean(np.square(d))
        if mse == 0:
            psnr = 70
        else:
            psnr = min(10 * np.log10(1 / mse), 70)
        sum += psnr
    return sum/ori_length

def psnr(original_pcd, downsampled_pcd):
    original_pcd = o3d.io.read_point_cloud(original_pcd)
    downsampled_pcd = o3d.io.read_point_cloud(downsampled_pcd)
    ds_length = len(downsampled_pcd.points)
    ori_length = len(original_pcd.points)
    rate = ds_length/ori_length
    sum = 0
    for i in range(len(original_pcd.points)):
        rgb_ori = original_pcd.colors[i]
        rgb_project = downsampled_pcd.colors[min(int(i*rate), ori_length-1)]
        Y_ori = RGB2YUV(rgb_ori)
        Y_project = RGB2YUV(rgb_project)
        mse = np.mean(np.square(Y_ori-Y_project))
        if mse == 0:
            psnr = 70
        else:
            psnr = min(10 * np.log10(1 / mse), 70)
        sum += psnr
    return sum/ori_length


with open("Output/aqp_dr_psnr.csv", "w") as voxy_csv:
    csv_writer = csv.writer(voxy_csv)
    csv_writer.writerow(["Dr", "AQP", "PSNR"])
    for QP in range(15, 36):
        _psnr = str(round(psnr_space("Ply/Longdress/longdress_1.0.ply", "Ply/AQP0.1/S" + str(QP) +".ply"), 3))
        print("Current:", _psnr)
        csv_writer.writerow(["0.1", str(QP), _psnr])
    for QP in range(15, 36):
        _psnr = str(round(psnr_space("Ply/Longdress/longdress_1.0.ply", "Ply/AQP0.33/S" + str(QP) +".ply"), 3))
        print("Current:", _psnr)
        csv_writer.writerow(["0.33", str(QP), _psnr])
    for QP in range(15, 36):
        _psnr = str(round(psnr_space("Ply/Longdress/longdress_1.0.ply", "Ply/AQP1/S" + str(QP) +".ply"), 3))
        print("Current:", _psnr)
        csv_writer.writerow(["1", str(QP), _psnr])

