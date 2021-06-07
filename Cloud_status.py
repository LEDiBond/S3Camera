from S3Camera import S3Camera
import boto3

AWS_obj = S3Camera()
l1= boto3.client('s3')
l = l1.list_buckets()
l.keys()
print(l['Buckets'][1]['Name'])
l['Buckets']

a=l1.list_objects(Bucket = 'image-buffer-test')