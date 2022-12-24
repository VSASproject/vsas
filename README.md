# Voxy
Voxy is a HTTP-based volumetric video streaming framework, with MPEG V-PCC support.
## Setup Pipeline
1. The Rate-Distortion model training data is located in `voxy_rd1/data`. 
2. First step is use the Rate-Distortion model to prepare the chunks with N discreite bitrate levels [b1,b2,b3,..].
3. Enter the directory voxy_rd1, train the R-D model by running `python rd_fit.py`, the model parameters are then stored in the cache located in `voxy_rd1/param_cache`.
4. Then call the `python rd_optim.py` to compute the QP value for each bitrate.
5. edit the `condition/rate/ctc-r1.cfg`, update the QP to be the QP computed in step 5.
6. Create the following path: `mpeg-pcc-tmc2/data/8i/8iVFBv2/`, download Longdress, Loot, RedandBlack and Soldier datasets into it. 
7. Run PccEncoder command [1] to compress one of the 8i dataset point cloud sequence. E.g, loot. http://plenodb.jpeg.org/pc/8ilabs. (For convenience, please drag `Scripts/mpeg_script.py` into `mpeg-pcc-tmc2/`, and run by `python mpeg_script.py`, remember to modify variable `sequence_config` into the corresponding cfg/sequence .cfg file.)
8. Follow the quic-go README to configure the Golang enviroment. https://github.com/lucas-clemente/quic-go. Then run our modified HTTP server, with frame-dropping support in `quic-go/example/local_server.sh` by `bash local_server.sh`.
9. Start quic-go client in `quic-go/example/local_client.sh` by `bash local_client.sh`, the PSNR and stalling time log will be recorded in `quic-go/example/stall_timing.log`.
## Drawing Pipeline
1. Rename `stall_timing.log` and drag it into `VV-Video_trace_handling/stall_timing_logs/`, run `log_extracation.py` to extract log information. After this step, run `PSNR_Script.py`, `QoE.py`, `Real_time.py`, `Stall_timing_bar.py` and `VPCC_Drop_No_Drop_Compare.py` to get network transmission figures in the paper. (Shown in directory ``)
2. To get mpeg/PSNR figures in the paper, run `nohup python mpeg_script.py` as steps in Setup Pipeline part. Rename `nohup.out` and drag it into `PSNR/nohup_records/`. the corresponding `cache/S15.ply` to `cache/S35.ply` files (`cache is record of mpeg_script.py`) can be put in Directories inside `Ply` (Optional).
3. Run `PSNR/extract_br.py` and `PSNR/General_PSNR.py` to extract csv files (`PSNR/Output/*.csv`) from logs.
4. Move all csv files in `PSNR/Output/` to `voxy_rd1/data/`, run `voxy_rd1/Multi_rd_fit.py ` and `voxy_rd1/rd_fig1.py`.
5. Now, all output pictures in step 4. can be checked in `voxy_rd1/figures/`

## Explain:
[1] `./bin/PccAppEncoder    --configurationFolder=cfg/      --config=cfg/common/ctc-common.cfg      --config=cfg/condition/ctc-all-intra.cfg        --config=cfg/sequence/longdress_vox10.cfg       --config=cfg/rate/ctc-me.cfg    --uncompressedDataFolder=./data/         --frameCount=1  --reconstructedDataPath=S26C03R03_rec_%04d.ply  --compressedStreamPath=S26C03R03.bin`

## Installation
### Dependency
+ Ubuntu 20.04.5 LTS
+ python 3.10
+ build-essential
+ cvxpy 1.2.2
+ go 1.19.4
+ pip packages: `requirements.txt`
### Install

`git clone --recursive https://github.com/VOXYproject/voxy.git`

# Manifest
## Manifest Example:
```json
[{
    "nal_no": 1000, 
    "filename": "G100ai_1000", 
    "type": -1
},
{"nal_no": 1000, "filename": "G100gi_1000", "type": -1}, 
{"nal_no": 1000, "filename": "G100oi_1000", "type": -1}, 
{"nal_no": 1000, "filename": "G101ai_1000", "type": -1}, 
{"nal_no": 1000, "filename": "G101gi_1000", "type": -1}, 
{"nal_no": 1000, "filename": "G101oi_1000", "type": -1}, 
{"nal_no": 1001, "filename": "G100ai_1001", "type": -1}, 
{"nal_no": 1001, "filename": "G100gi_1001", "type": -1}, 
{"nal_no": 1001, "filename": "G100oi_1001", "type": -1}, 
{"nal_no": 1001, "filename": "G101ai_1001", "type": -1}, 
{"nal_no": 1001, "filename": "G101gi_1001", "type": -1}, 
{"nal_no": 1001, "filename": "G101oi_1001", "type": -1}, 
{"nal_no": 1002, "filename": "G100ai_1002", "type": -1}, 
{"nal_no": 1002, "filename": "G100gi_1002", "type": -1}, 
{"nal_no": 1002, "filename": "G100oi_1002", "type": -1}, 
{"nal_no": 1002, "filename": "G101ai_1002", "type": -1}, 
{"nal_no": 1002, "filename": "G101gi_1002", "type": -1},
]
```
