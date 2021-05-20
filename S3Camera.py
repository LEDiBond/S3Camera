import os
import cv2
import boto3
import cv2
from termcolor import colored
from datetime import datetime


class S3Camera:

    def __init__(self, camera_phy_mac="undefined", camera_phy_port="undefined"):
        self.camera_phy_mac = camera_phy_mac
        self.camera_phy_port = camera_phy_port
        self.camera_project_association = "undefined"
        self.camera_commission_status = "Not Commissioned"
        self.camera_s3_client = None
        self.default_image_name = "CURRENT_IMG.jpg"

    def __str__(self):
        return "Camera Physical address : " + self.camera_phy_mac + " \n " + \
               "Camera Physical port : " + self.camera_phy_port + " \n " + \
               "Camera Commissioned to Bucket : " + self.camera_project_association + " \n "

    def cam_commission(self, project_name, service='s3'):
        self.camera_project_association = project_name

        if service == boto3.resource(service).meta.service_name:
            self.camera_s3_client = boto3.client(service)
            for bucket in self.camera_s3_client.list_buckets()['Buckets']:
                if bucket['Name'] == self.camera_project_association:
                    print("Related Project found")
                    self.camera_commission_status = "Commissioned to :" + bucket['Name']
                    print("Commissioned to :" + bucket['Name'])
                    break
            if self.camera_commission_status.startswith("Commissioned to :"):
                print("Commissioning Complete")
            else:
                print(
                    "No related project found in Database: Aborting commissioning. \n Please create a related bucket in AWS S3 with a correct Project name and try again")
        else:
            print(" Resources mentioned other than S3")

    def cam_upload_currentImg(self):
        try:
            key = self.default_image_name
            self.camera_s3_client.upload_file(Filename=self.default_image_name, Bucket=self.camera_project_association,
                                              Key=self.default_image_name)
            print("File upload successfull")
            print("File " + colored(self.default_image_name, 'green') + " uploaded to bucket :" + colored(
                self.camera_project_association, 'green') + " with key :" + colored(self.default_image_name, 'green'))
            return key
        except IOError:
            print(IOError)

    def cam_download_currentImg(self):
        if self.camera_commission_status != "Not Commissioned":
            data = self.camera_s3_client.download_file(self.camera_project_association, Key=self.default_image_name,
                                                       Filename='Downloaded_file.jpg')
            print("Data upload Successful \n Bucket used : " + colored(self.camera_project_association,
                                                                       'green') + "With Key: " + colored(
                self.default_image_name, 'green'))
            print("File downloaded to file" + colored('Downloaded_file.jpeg', 'red'))
        elif self.camera_commission_status == "Not Commissioned":
            print("Camera not commissioned")
        else:
            print("Error with commissioning, Please check Bucket credential and try again:")
        return data

    def cam_capture(self, webcam_id):
        cam = cv2.VideoCapture(webcam_id)
        height = 1080
        width =  1900
        cam.set(3, height)
        cam.set(4, width)
        img, frame = cam.read()
        cv2.imwrite(self.default_image_name, frame)
        cam.release()

    def cam_stream(self, webcam_id, delay=10):
        print("Starting Stream from " + colored("webcam_id ", 'green') + ":" + colored(webcam_id, 'red'))
        interrupt = "null"
        index = 1
        # Flag is used here as a one time flag indicator to show if the image has been clicked once in a delay period
        # once the image has been clicked on the "delay" second, it is set to True.
        flag = False
        try:
            while interrupt != "stop":
                if (datetime.now().time().second % delay == 0) & (flag == False):

                    self.cam_capture(webcam_id)
                    #self.cam_upload_currentImg()
                    print("Dummy thing do")
                    flag = True
                    print( str(index) + "th image clicked and uploaded")
                    index = index + 1

                else:
                    if (datetime.now().time().second % delay != 0) & (flag == True):
                        flag = False
                        print("---- Resetting Flag ----")

        except KeyboardInterrupt:
            print("Keyboard Interrupt made")
            interrupt = input("Enter 'stop' to exit Stream and 'C' to continue:   ")
        print("Stream stopped ")
