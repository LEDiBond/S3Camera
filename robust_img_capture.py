from S3Camera import S3Camera

CAM_PHY_ADDRESS = "12as 213 5442 3g223"
CAM_PHY_PORT = "8004 : 0002"
## Make flag true if working on Jetson Xavier
from subprocess import run, call, DEVNULL, STDOUT, check_call
nvgstcapture = False
s = S3Camera(CAM_PHY_ADDRESS, CAM_PHY_PORT, nvgstcapture=nvgstcapture)

s.cam_commission("image-buffer-test")
s.cam_capture(0)