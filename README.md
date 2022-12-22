# Voxy
Voxy is a HTTP-based volumetric video streaming framework, with MPEG V-PCC support.
## Pipeline
1. The Rate-Distortion model training data is located in `voxy_rd1/data`. 
2. First step is use the Rate-Distortion model to prepare the chunks with N discreite bitrate levels [b1,b2,b3,..].
3. Enter the directory voxy_rd1, train the R-D model by running `python rd_fit.py`, the model parameters are then stored in the cache located in `voxy_rd1/param_cache`.
4. Then call the `python rd_optim.py` to compute the QP value for each bitrate.
5. edit the `condition/rate/ctc-r1.cfg`, update the QP to be the QP computed in step 5.
6. Run PccEncoder command to compress one of the 8i dataset point cloud sequence. E.g, loot. http://plenodb.jpeg.org/pc/8ilabs.
7. Follow the quic-go README to configure the Golang enviroment. https://github.com/lucas-clemente/quic-go. Then run our modified HTTP server, with frame-dropping support in `quit-go/quic-server` by `go run quic-server`.
8. Start quic-go client `quic-client`, the PSNR and stalling time log will be recorded then.
   
## Installation
### Dependency
+ Ubuntu 20.04.5 LTS
+ python 3.10
+ build-essential
+ cvxpy 1.2.2
+ pip packages: `requirements.txt`
### Install

`git clone https://github.com/VOXYproject/voxy.git`

## Config
### Basic Config
Example:
```json
{
    "id": "101"
}
```
