#created on 2022/06/22, 11:50 (UTC+8)
#The ssim log parser, that taking the config file as the input
#output a csv file including the ssim for each video type
import json
import os
import logging
import pandas as pd
import numpy as np
import argparse
from pathlib import Path

def mean_ssim_not_null(ssim_log_path):
    ssim_avgs = []
    frame_drops = 0
    with open(ssim_log_path,'r') as f1:
        lines = f1.readlines()
        for line in lines:
            ssim_avg_str = line.split()[4].split(":")[1]
            logging.debug("the current ssim avg is " + ssim_avg_str)
            try:
                ssim_avg = float(ssim_avg_str)
                if ssim_avg < 0.78:
                    frame_drops += 1
                else:
                    ssim_avgs.append(ssim_avg)
            except ValueError:
                frame_drops += 1
    if len(ssim_avgs) == 0:
        ssim_avgs.append(0)
    mean_ssim = np.array(ssim_avgs).mean()
    return mean_ssim, frame_drops

def ssim_log_parse(confg_path,csv_root):
    with open(config_path) as f1:
        jconfig = json.load(f1)
        ssim_prefix = "ssim_"
        csv_path = os.path.join(csv_root, ssim_prefix+str(jconfig["exp_id"]) + ".csv")
        video_types = jconfig["video_types"]
        loss_rate_list = jconfig["loss_rate"]
        attr_ssim_list = []
        geo_ssim_list = []
        occ_ssim_list = []
        frame_drop_list = []
        for loss_rate in loss_rate_list:
            for video_type in video_types:
                video_type_path = os.path.join(jconfig["origin_path"], video_type)
                manifest_path = os.path.join(video_type_path, "manifest/manifest.json")
                tmp_root = jconfig["tmp_path"]
                tmp_path = os.path.join(tmp_root, video_type)
                tmp_ssim_path = os.path.join(tmp_path, "ssim_log")
                ssim_log_path = os.path.join(tmp_ssim_path, str(loss_rate) + ".log")
                (ssim,frame_drop) = mean_ssim_not_null(ssim_log_path)
                if video_type == "attribute":
                    attr_ssim_list.append(ssim)
                    frame_drop_list.append(frame_drop)
                elif video_type == "geometry":
                    geo_ssim_list.append(ssim)
                elif video_type == "occupancy":
                    occ_ssim_list.append(ssim)
                else:
                    logging.error("wrong video type, quit")
                    exit(1)
        df = pd.DataFrame({"loss": loss_rate_list,
                           "attribute_ssim": attr_ssim_list,
                           "geometry_ssim": geo_ssim_list,
                           "occupancy_ssim": occ_ssim_list,
                          "frame_drop": frame_drop_list})
        df.to_csv(csv_path, index=False)

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output path")
    args = parser.parse_args()
    output_path = "."
    if args.output:
        logging.debug("output exp logs to " + args.output)
        output_path = args.output

    config_path = "exp_config.json"
    csv_root = output_path
    Path(csv_root).mkdir(parents=True, exist_ok=True)
    ssim_log_parse(config_path,csv_root)


