
import os
from pathlib import Path
import logging

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    exp_path = "exp_output"
    protocol_list = ["partial","udp","quic"]
    for protocol in protocol_list:
        protocol_path = os.path.join(exp_path,protocol)
        Path(protocol_path).mkdir(parents=True, exist_ok= True)
        cmd_drop = "python nal_dropper_"+protocol+".py"
        logging.debug(cmd_drop)
        os.system(cmd_drop)
        cmd_psnr_parse = "python psnr_log_parser.py " + "--output=" + protocol_path
        logging.debug(cmd_psnr_parse )
        os.system(cmd_psnr_parse )
        cmd_ssim_parse = "python ssim_log_parser.py " + "--output=" + protocol_path
        logging.debug(cmd_ssim_parse)
        os.system(cmd_ssim_parse)
