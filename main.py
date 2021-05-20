# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from S3Camera import S3Camera

    CAM_PHY_ADDRESS = "12as 213 5442 3g223"
    CAM_PHY_PORT = "8004 : 0002"
    s = S3Camera(CAM_PHY_ADDRESS, CAM_PHY_PORT)
#    s.cam_commission("image-buffer-test")

# TIME bASED LOOP TO CAPTURE AND UPLOAD IMAGES.
# lOOP EXIT KEY DEFINED AS EXIT.CC

    s.cam_capture(0)
    #s.cam_stream(0)

    #key = s.cam_upload_currentImg()
    #print("Image uploaded with key " + key)
    #s.cam_download_currentImg()

    #s.cam_stream(0)
