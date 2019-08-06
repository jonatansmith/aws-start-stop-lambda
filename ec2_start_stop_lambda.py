#Author: Jonatan Smith (jonatansmith@gmail.com)
#Date of first release: 20190530
#Description: Start or stop an EC2 instance in AWS. Can be used with a cron rule (CloudWatch) to schedule automatically and manage lifecycle.
#How to Use: tag EC2 resource with a key of your preference, the same in JSON input (activationTag) and value 'true' to start / stop it
#     Create rule in cloudwatch to schedule (cron) and configure input as "Constant (JSON Text)" using the following format:
#     JSON: '{ "activationTag": "ScheduledStartStopTest" }'
#            '{ "activationTag": "ScheduledStartStopTest", "startOrStop": "start" }'
#        Where the value of :
#            "activationTag" have to be the same used in the resources you want to manage. In this example it is "ScheduledStartStopTest"
#            "startOrStop" accept "start", "stop", which control the action of lifecycle management.
import boto3
import sys, traceback
from datetime import datetime
from time import sleep

def startOrStop_EC2_instances(activationTag,startOrStop):
    start_time = datetime.now()
    # starting ec2 client
    ec2_client = boto3.client('ec2')
    regions = ec2_client.describe_regions()
    print ("tag: "+ activationTag)
    print ("Start or Stop?: "+ startOrStop)
    for region in regions['Regions']:
        try:
            ec2_client = boto3.client('ec2', region_name=region['RegionName'])
            instances = ec2_client.describe_instances()
            instanceIds = list()

            if startOrStop == "start":
                for reservation in instances['Reservations']:
                    for instance in reservation['Instances']:
                        if instance['State']['Name'] == "stopped" and not instance['Tags'] is None : 
                            for tag in instance['Tags']:
                                try:
                                    if tag['Key'] == activationTag and tag['Value'].lower() == 'true':
                                        instanceIds.append(instance['InstanceId'])
                                except:
                                    print "Not expected error: ", traceback.print_exc()
                if len(instanceIds) > 0 : 
                    print "Starting instances: " + str(instanceIds)
                    ec2_client.start_instances(InstanceIds=instanceIds)                                                   
            else:
                if startOrStop == "stop":
                    for reservation in instances['Reservations']:
                        for instance in reservation['Instances']:
                            if instance['State']['Name'] == "running" and not instance['Tags'] is None : 
                                for tag in instance['Tags']:
                                    try:
                                        if tag['Key'] == activationTag and tag['Value'].lower() == 'true':
                                            instanceIds.append(instance['InstanceId'])
                                    except:
                                        print "Not expected error: ", traceback.print_exc()
                    if len(instanceIds) > 0 : 
                        print "Stopping instances: " + str(instanceIds)
                        ec2_client.stop_instances(InstanceIds=instanceIds, Force=True)                                                    
        except:
            print "Not expected error:", traceback.print_exc()
                                                           
    end_time = datetime.now()
    took_time = end_time - start_time
    print "Total time of execution: " + str(took_time)    

def lambda_handler(event, context):
    print('Managing lifecycle of EC2 instances...')
    startOrStop_EC2_instances(event['activationTag'],event['startOrStop'])