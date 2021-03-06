# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from S3Camera import S3Camera

    CAM_PHY_ADDRESS = "12as 213 5442 3g223"
    CAM_PHY_PORT = "8004 : 0002"
    ## Make flag true if working on Jetson Xavier
    nvgstcapture = True
    s = S3Camera(CAM_PHY_ADDRESS, CAM_PHY_PORT, nvgstcapture=nvgstcapture)
    s.cam_commission("image-buffer-test")

    #s.cam_capture(0)
    #s.cam_stream(0)
    #key = s.cam_upload_currentImg()
    #print("Image uploaded with key " + key)

    #s.cam_download_currentImg()

    #s.cam_stream(0)

    #s.cam_stream_upload()
    s.local_cam_detect(webcam_id=0,delay_sec=5,result_update=True, image_update=True)