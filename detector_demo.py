
# Press the green button in the gutter to run the script.
# for uploading new images on AWS
from S3Camera import S3Camera
from darknet import draw_boxes

    # DEMO DETAIL ABOUT THE CAMERA
CAM_PHY_ADDRESS = "12as 213 5442 3g223"
CAM_PHY_PORT = "8004 : 0002"
s = S3Camera(CAM_PHY_ADDRESS, CAM_PHY_PORT)

    # connect the object with the name of the same project
s.cam_commission("image-buffer-test")

## Perform continous detection on streaming images.
s.cam_stream_detect(delay_sec = 5)