#!/usr/bin/env python

import boto3


ec2 = boto3.resource('ec2')
ec2client = boto3.client('ec2')


#-----Define Lambda function-----#
def lambda_handler(event, context):

#-----Check& filter Instances which  Instance State is running-----#
    instances = ec2client.describe_instances(
        Filters=[{
            'Name': 'instance-state-name',
            'Values': ['pending', 'running']
        }]
        )

#-----Define dictionary to store Tag Key & value------#
    dict={}

    mytags = [{
        "Key" : "test_key", "Value" : "test_value"
        }]

#-----Store Key & Value of Instance ------#
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            ec2.create_tags(
                Resources = [instance["InstanceId"] ],
                Tags = mytags)
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    print ( instance['InstanceId'],tag['Value'])
                    #ids.append(( instance['InstanceId'],tag['Value']))
                    dict[instance['InstanceId']]= tag['Value']
                
#-----Store Key & Value with attached instance ID of all volumes ------#     
    volumes = ec2.volumes.all() 
    for volume in volumes:

#-----compare dictionary value Key:InstanceID and volume attached Key:InstanceID ------#     
        for a in volume.attachments:
            for key, value in dict.items():


#-----Add tags to volumes ------#     

                if a['InstanceId'] == key:
                     volume.create_tags(Tags =[{
                        'Key': 'test_key', 'Value': 'test_value'}
                    ])
