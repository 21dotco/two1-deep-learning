import os
import sys
import logging
import boto3

from deep21 import settings

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

USERDATA_TEMPLATE = """#cloud-config

runcmd:
 - export LD_LIBRARY_PATH=/home/ubuntu/torch-distro/install/lib:/usr/local/cuda/lib64:/home/ubuntu/cudnn/:$LD_LIBRARY_PATH
 - export PATH=/home/ubuntu/torch-distro/install/bin:/home/ubuntu/anaconda/bin:/usr/local/cuda/bin:$PATH
 - export DYLD_LIBRARY_PATH=/home/ubuntu/torch-distro/install/lib:$DYLD_LIBRARY_PATH
 - export PYTHONPATH=/home/ubuntu/caffe/python:$PYTHONPATH
 - export TH_RELEX_ROOT=/home/ubuntu/th-relation-extraction
 - export HOME=/home/ubuntu
 - cd /style-transfer-torch
 - aws --region {region} s3 cp s3://{bucket}/{content} ./{content}
 - aws --region {region} s3 cp s3://{bucket}/{style} ./{style}
 - th neural_style.lua -style_image {style} -content_image {content} -output_image {output} -gpu 0 -backend cudnn -cudnn_autotune -print_iter 50 -image_size 500 -num_iterations 500 -init image
 - aws --region {region} s3 cp ./{output} s3://{bucket}/{output}
 - shutdown -h now
"""


def num_running_instances():
    ec2 = boto3.client('ec2')

    instances = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running', 'pending']},
            {'Name': 'instance-type', 'Values': [settings.EC2_INSTANCE_TYPE]},
            {'Name': 'image-id', 'Values': [settings.EC2_AMI_ID]},
        ]
    )

    return len(instances['Reservations'])


def upload_to_s3(local_filename, s3_filename):
    logger.info('Uploading file {} to S3://{}'.format(local_filename, s3_filename))
    s3 = boto3.client('s3')
    s3.upload_file(local_filename, settings.S3_BUCKET_NAME, s3_filename)


def download_from_s3(local_filename, s3_filename):
    logger.info('Downloading file to {} from S3://{}'.format(local_filename, s3_filename))
    s3 = boto3.client('s3')
    s3.download_file(settings.S3_BUCKET_NAME, s3_filename, local_filename)


def spin_up(data):
    ec2 = boto3.resource('ec2')

    instances = ec2.create_instances(
        ImageId=settings.EC2_AMI_ID,
        InstanceType=settings.EC2_INSTANCE_TYPE,
        KeyName=settings.EC2_SSH_KEYPAIR_ID,
        MinCount=1,
        MaxCount=1,
        IamInstanceProfile={
            'Arn': settings.EC2_IAM_INSTANCE_PROFILE_ARN
        },
        InstanceInitiatedShutdownBehavior='terminate',
        SecurityGroupIds=[settings.EC2_SECURITY_GROUP_NAME],
        UserData=USERDATA_TEMPLATE.format(**data)
    )

    instance = instances[0]
    logger.info('Spinning up instance with id {} at {}'.format(instance.id, instance.launch_time))

    return instance.id


def launch(local_filepaths, data):
    '''
        Copy the local files to S3, and then launch the aws instance with
        the appropriate parameters for the USER_DATA script.
    '''

    for key, filepath in local_filepaths.items():
        filename = os.path.split(filepath)[1]
        data[key] = filename

        if key in [settings.CONTENT_SUFFIX, settings.STYLE_SUFFIX]:
            upload_to_s3(filepath, filename)

    data['bucket'] = settings.S3_BUCKET_NAME
    data['region'] = settings.AWS_DEFAULT_REGION
    return spin_up(data)
