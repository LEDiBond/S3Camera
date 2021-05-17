import os
import cv2
import boto3
import cv2

class S3Camera:
    ## Class i sused to prod
    ##camera_phy_mac = ""
    ##camera_phy_port = ""
    ##camera_project_association = ""

   # def __int__(self):
   #     self.camera_phy_mac = "undefined"
   #     self.camera_phy_port = "undefined"
   #     self.camera_project_association = "undefined"
   #     self.camera_commission_status= "Not Commissioned"
   #     self.camera_s3_resource = None
   #     self.default_image_name = "CURRENT_IMG.jpeg"

    def __init__(self, camera_phy_mac = "undefined", camera_phy_port = "undefined"):
        self.camera_phy_mac = camera_phy_mac
        self.camera_phy_port = camera_phy_port
        self.camera_project_association = "undefined"
        self.camera_commission_status = "Not Commissioned"
        self.camera_s3_resource = None
        self.default_image_name = "CURRENT_IMG.jpeg"

    def __str__(self):
        return "Camera Physical address : " + self.camera_phy_mac + " \n " + \
               "Camera Physical port : " + self.camera_phy_port + " \n " + \
               "Camera Commissioned to Bucket : " + self.camera_project_association + " \n "

    def cam_commission(self, project_name, service = 's3'):
        self.camera_project_association = project_name

        if service == boto3.resource(service).meta.service_name:
            self.camera_s3_resource = boto3.resource(service)
            for bucket in self.camera_s3_resource.buckets.all():
                if bucket.name == self.camera_project_association:
                    print("Related Project found")
                    self.camera_commission_status = "Commissioned to :" + bucket.name
                    print ("Commissioned to :" + bucket.name)
                    break
            if self.camera_commission_status.startswith("Commissioned to :"):
                print("Commissioning Complete")
            else:
                print("No related project found in Database: Aborting commissioning. \n Please create a related bucket in AWS S3 with a correct Project name and try again")
        else:
            print(" Resources mentioned other than S3")

    def cam_capture_upload(self):
        try:
            data = open("CURRENT_IMG.jpeg", 'rb')
            key = self.default_image_name
            self.camera_s3_resource.Bucket(self.camera_project_association).put_object( Key = self.default_image_name, Body = data)
            data.close()
            return key
        except IOError:
            print(IOError)

    def cam_capture(self, webcam_id):
        cam = cv2.VideoCapture(webcam_id)
        img, frame = cam.read()
        cv2.imwrite(self.default_image_name, frame)
        cam.release()

