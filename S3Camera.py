import os
import time

import cv2
import boto3
import cv2
from termcolor import colored
from datetime import datetime
import os
import json


class S3Camera:

    def __init__(self, camera_phy_mac="undefined", camera_phy_port="undefined", nvgstcapture=False):

        self.camera_phy_mac = camera_phy_mac
        self.camera_phy_port = camera_phy_port
        self.nvgstcapture = nvgstcapture

        # Camera project association is a Tag that is unique for a project. Managers at AWS S3 utilize this tag to create a bucket for the project which act as
        # a memory buffer for saving current image and results of detection.
        self.camera_project_association = "undefined"
        self.camera_commission_status = "Not Commissioned"
        self.camera_s3_client = None

        # Variables to store file names. Current image captured is saved as "CURRENT_IMG.jpg" and Detection result is
        # saved as "detection_result.json"
        self.default_image_name = "CURRENT_IMG.jpg"
        self.default_detection_ID = "detection_result.json"
        self.darknet_detection_ID = "result.json"
        self.default_downloaded_img_ID = "Downloaded_file.jpg"

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

    def cam_download_currentImg(self, Filename='Downloaded_file.jpg'):
        data = False
        self.default_downloaded_img_ID = Filename
        self.default_downloaded_img_ID = "Downloaded_file.jpg"
        if self.camera_commission_status != "Not Commissioned":
            self.camera_s3_client.download_file(self.camera_project_association, Key=self.default_image_name,
                                                Filename=Filename)
            print("Data upload Successful \n Bucket used : " + colored(self.camera_project_association,
                                                                       'green') + "With Key: " + colored(
                self.default_image_name, 'green'))
            print("File downloaded to file :" + colored(Filename, 'red'))
            data = True

        elif self.camera_commission_status == "Not Commissioned":
            print("Camera not commissioned")
        else:
            print("Error with commissioning, Please check Bucket credential and try again:")

        return data

    def cam_capture(self, webcam_id):
        if self.nvgstcapture:
            ## if nvsgtcapture is true then v4l2 based capture is done
            #gst v4l2 based image capture
            ## do cmd line capture using nvgstcapture
            from subprocess import run, call, DEVNULL, STDOUT, check_call
            call(["nvgstcapture-1.0",
                  "--camsrc="+str(webcam_id), "--cap-dev-node="+str(webcam_id), ## webcam address /dev/video<N> where N is webcamid
                  "-m","1",
                  "--prev-res=4", "--image-res=4", #resolution 4 = 1900x1080
                  "--automate", "--capture-auto",
                  "--filename="+self.default_image_name  # image path and name
                  ],stdout=False)
        else:
            ## opencv based image capture
            cam = cv2.VideoCapture(webcam_id)
            height = 1080
            width = 1900
            cam.set(3, height)
            cam.set(4, width)
            img, frame = cam.read()
            ret = cv2.imwrite(self.default_image_name, frame)
            cam.release()
        return ret

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

                    print("Dummy thing do")
                    flag = True
                    print(str(index) + "th image clicked and uploaded")
                    index = index + 1

                else:
                    if (datetime.now().time().second % delay != 0) & (flag == True):
                        flag = False
                        print("---- Resetting Flag ----")

        except KeyboardInterrupt:
            print("Keyboard Interrupt made")
            interrupt = input("Enter 'stop' to exit Stream and 'C' to continue:   ")
        print("Stream stopped ")

    # Function to capture images at regular interval and upload on aws bucket from a commissisoned camera.
    # The image is updated after every delay_sec. Camera id is needed or else default webcam_id = 0.

    def cam_stream_upload(self, webcam_id=0, delay_sec=5):
        start = time.time()
        action = True
        try:
            while action:
                current_time = time.time()
                elapsed_time = current_time - start
                print(str(round(elapsed_time, 0)) + "Seconds elapsed", end='\r')
                if elapsed_time > delay_sec:
                    print("Called function")

                    # Camera capture function called
                    ret = self.cam_capture(webcam_id)

                    # Camera upload function called
                    if ret:
                        self.cam_upload_currentImg()
                    else:
                        action = False

                    # Resetting the timer
                    start = time.time()
        except KeyboardInterrupt:
            print("Keyboard Interrupt made")
            interrupt = input("Enter 'stop' to exit Stream and 'C' to continue:   ")

        print("...........Stream stopped..............")
        return action

    # function to Stream current images from a commissisoned camera. The image is updated after ecery delay_sec.

    def cam_stream_download(self, delay_sec=5):
        start = time.time()
        action = True
        try:
            while action:
                current_time = time.time()
                elapsed_time = current_time - start
                print(str(round(elapsed_time, 0)) + "Seconds elapsed", end='\r')
                if elapsed_time > delay_sec:
                    print("Called function")

                    # Image download function
                    ret = self.cam_download_currentImg()
                    # write condition for download failure
                    if ret:
                        print("Image Downloaded")
                    else:
                        print("Image Downloading failed")
                        action = False
                    # Resetting the timer
                    start = time.time()
        except KeyboardInterrupt:
            print("Keyboard Interrupt made")
            interrupt = input("Enter 'stop' to exit Stream and 'C' to continue:   ")
        print("...........Stream Download stopped..............")
        return action

    def cam_stream_detect(self, delay_sec=5, online_update=True):
        # has dependencies on darknet
        start = time.time()
        action = True
        try:
            while action:
                current_time = time.time()
                elapsed_time = current_time - start
                print(str(round(elapsed_time, 0)) + "Seconds elapsed", end='\r')
                if elapsed_time > delay_sec:
                    print("Called function")

                    # Image download function
                    ret = self.cam_download_currentImg()
                    # write condition for download failure
                    ret = True
                    if ret:
                        print("Image Downloaded")
                        ## calling darknet subprocess to detect objects in the image
                        ## darknet isntalled locally in the same folder
                        ## no dependecies on darknet locations
                        self.subp_cmd_single_img_det_beta()

                        print("............Prediction done .......")
                        pred = json.load(open("result.json"))
                        print(pred)

                        # Upload prediction on bucket
                        if (online_update):
                            self.camera_s3_client.upload_file(Filename=self.darknet_detection_ID,
                                                              Bucket=self.camera_project_association,
                                                              Key=self.default_detection_ID)
                    else:
                        print("Image Downloading failed")
                        action = False

                    # Resetting the timer
                    start = time.time()
        except KeyboardInterrupt:
            print("Keyboard Interrupt made")
            interrupt = input("Enter 'stop' to exit Stream and 'C' to continue:   ")

        print("...........Stream Download stopped..............")
        return action

    ## will deprecate when darknet is locally installed
    ## hardcoded information need to be dynamic

    def os_cmd_list_based_darknet_detect(self):
        home_path = "/home/chaoster/S3Camera/"
        darknet_path = "/home/chaoster/darknet/"
        os.system(darknet_path + "./darknet detector test " +
                  darknet_path + "cfg/coco.data " +
                  darknet_path + "cfg/yolov4.cfg " +
                  darknet_path + "yolov4.weights" +
                  " -ext_output -dont_show -out result.json <" +
                  darknet_path + "current_img_dir.txt")

    # if local = True then current image is used in prediction
    # if local is false then image is downloaded
    def subp_cmd_single_img_det_beta(self, local=True):
        from subprocess import run, call, DEVNULL, STDOUT, check_call
        if not local:
            call(["./darknet", "detector", "test", "cfg/coco.data",
                  "cfg/yolov4.cfg",  # concerned cfg file
                  "yolov4.weights",  # model weights
                  "-ext_output", "-dont_show", "-out",
                  self.default_detection_ID,  # output file name
                  self.default_downloaded_img_ID  # image path and name
                  ],
                 stdout=False)
        else:
            call(["./darknet", "detector", "test", "cfg/coco.data",
                  "cfg/yolov4.cfg",  # concerned cfg file
                  "yolov4.weights",  # model weights
                  "-ext_output", "-dont_show", "-out",
                  self.default_detection_ID,  # output file name (json)
                  self.default_image_name  # image path and name
                  ],
                 stdout=False)

    # Function for site PC with cam detection and upload facilities
    # Image captured locally and fed to darknet installed on the system
    # Once the predection is made, The result jason script is uploaded along with curre
    def local_cam_detect(self, webcam_id=0, delay_sec=5, result_update=False, image_update=False):
        start = time.time()
        action = True
        try:
            while action:
                current_time = time.time()
                elapsed_time = current_time - start
                print(str(round(elapsed_time, 0)) + "Seconds elapsed", end='\r')
                if elapsed_time > delay_sec:
                    print("Called function")

                    # Camera capture function called
                    ret = self.cam_capture(webcam_id)

                    # Camera upload function called
                    if ret:
                        print("Image Captured")
                        ## calling darknet subprocess to detect objects in the image
                        ## darknet isntalled locally in the same folder
                        ## no dependecies on darknet locations
                        self.subp_cmd_single_img_det_beta(local=True)
                        self.draw_boxes()

                        print("............Prediction done .......")
                        pred = json.load(open(self.default_detection_ID))
                        print(pred)

                        # Upload prediction on bucket
                        if result_update:
                            self.camera_s3_client.upload_file(Filename=self.default_detection_ID,
                                                              Bucket=self.camera_project_association,
                                                              Key=self.default_detection_ID)
                            print("Prediction results uploaded successfully")

                        if image_update:
                            self.camera_s3_client.upload_file(Filename=self.default_image_name,
                                                              Bucket=self.camera_project_association,
                                                              Key=self.default_image_name)
                            print("Prediction Image uploaded successfully")
                    else:
                        print("Image Capturing failed")
                        action = False
                    # Resetting the timer
                    start = time.time()
        except KeyboardInterrupt:
            print("Keyboard Interrupt made")
            interrupt = input("Enter 'stop' to exit Stream and 'C' to continue:   ")

        print("...........Stream stopped..............")
        return action

    def draw_boxes(self):
        pred = json.load(open(self.default_detection_ID))
        image = cv2.imread(self.default_image_name)

        colors = (0, 255, 255)

        for objects in pred[0].get('objects'):
            yolo_coordinates = []
            label = objects.get('name')
            confidence = objects.get('confidence')
            center_x = objects.get('relative_coordinates').get('center_x') * image.shape[1]
            center_y = objects.get('relative_coordinates').get('center_y') * image.shape[0]
            width = objects.get('relative_coordinates').get('width') * image.shape[1]
            height = objects.get('relative_coordinates').get('height') * image.shape[0]

            x_start = int(round(center_x - (width / 2)))
            y_start = int(round(center_y - (height / 2)))
            x_end = int(round(center_x + (width / 2)))
            y_end = int(round(center_y + (height / 2)))

            print(str(x_start) + ":" + str(y_start) + ":" + str(x_end) + ":" + str(y_end))
            image = cv2.rectangle(image, (x_start, y_start), (x_end, y_end), colors, 1)
            cv2.putText(image, "{} [{:.2f}]".format(label, float(confidence)),
                        (x_start, y_start - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        colors, 2)

        cv2.imwrite("box_img.jpg", image)

# Prediction result evaluator
class Lighting_schema:
    detectec_objects = []
    Active_scheme = []