#created on 2022/06/22, 11:50 (UTC+8)
#The psnr log parser, that taking the config file as the input
#output a csv file including the psnr for each video type
import json
import os
import logging
import pandas as pd
import numpy as np
import argparse
from pathlib import Path

def mean_psnr_not_null(psnr_log_path):
    psnr_avgs = []
    frame_drops = 0
    with open(psnr_log_path,'r') as f1:
        lines = f1.readlines()
        for line in lines:
            psnr_avg_str = line.split()[5].split(":")[1]
            logging.debug("the current psnr avg is " + psnr_avg_str)
            try:
                psnr_avg = float(psnr_avg_str)
                if psnr_avg < 15:
                    frame_drops += 1
                elif psnr_avg > 100:
                    psnr_avg = 60
                    psnr_avgs.append(psnr_avg)
                else:
                    psnr_avgs.append(psnr_avg)
            except ValueError:
                frame_drops += 1
    if len(psnr_avgs) == 0:
        psnr_avgs.append(0)
    mean_psnr = np.array(psnr_avgs).mean()
    return mean_psnr, frame_drops

def psnr_log_parse(confg_path,csv_root):
    with open(config_path) as f1:
        jconfig = json.load(f1)
        psnr_prefix = "psnr_"
        csv_path = os.path.join(csv_root, psnr_prefix+str(jconfig["exp_id"]) + ".csv")
        video_types = jconfig["video_types"]
        loss_rate_list = jconfig["loss_rate"]
        attr_psnr_list = []
        geo_psnr_list = []
        occ_psnr_list = []
        frame_drop_list = []
        for loss_rate in loss_rate_list:
            for video_type in video_types:
                video_type_path = os.path.join(jconfig["origin_path"], video_type)
                manifest_path = os.path.join(video_type_path, "manifest/manifest.json")
                tmp_root = jconfig["tmp_path"]
                tmp_path = os.path.join(tmp_root, video_type)
                tmp_psnr_path = os.path.join(tmp_path, "psnr_log")
                psnr_log_path = os.path.join(tmp_psnr_path, str(loss_rate) + ".log")
                (psnr,frame_drop) = mean_psnr_not_null(psnr_log_path)
                if video_type == "attribute":
                    attr_psnr_list.append(psnr)
                    frame_drop_list.append(frame_drop)
                elif video_type == "geometry":
                    geo_psnr_list.append(psnr)
                elif video_type == "occupancy":
                    occ_psnr_list.append(psnr)
                else:
                    logging.error("wrong video type, quit")
                    exit(1)
        df = pd.DataFrame({"loss": loss_rate_list,
                           "attribute_psnr": attr_psnr_list,
                           "geometry_psnr": geo_psnr_list,
                           "occupancy_psnr": occ_psnr_list,
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
    psnr_log_parse(config_path,csv_root)


