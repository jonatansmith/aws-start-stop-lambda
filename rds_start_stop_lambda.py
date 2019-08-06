#Author: Jonatan Smith (jonatansmith@gmail.com)
#Date of first release: 20190530
#Description: Start or stop an RDS instance in AWS. Can be used with a cron rule (CloudWatch) to schedule automatically and manage lifecycle.
#How to Use: tag RDS resource with a key of your preference, the same in JSON input (activationTag) and value 'true' to start / stop it
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

def startOrStop_rds_instances(activationTag,startOrStop):
    start_time = datetime.now()
    # starting ec2 client to get region list
    ec2_client = boto3.client('ec2')
    regions = ec2_client.describe_regions()
    print ("tag: "+ activationTag)
    print ("Start or Stop?: "+ startOrStop)
    for region in regions['Regions']:
        try:
            # starting RDS client
            rds = boto3.client('rds',region_name=region['RegionName'])
            dbs = rds.describe_db_instances()
            for db in dbs['DBInstances']:
                #print ("DB#: %s@%s:%s %s %s") % (
                #db['MasterUsername'],
                #db['Endpoint']['Address'],
                #db['Endpoint']['Port'],
                #db['DBInstanceStatus'],
                #db['DBInstanceIdentifier'])
                tagresponse = rds.list_tags_for_resource(ResourceName=db['DBInstanceArn'])
                taglist = tagresponse['TagList']
                if startOrStop == "start":
                    for tag in taglist:
                        if tag['Key'] == activationTag and tag['Value'].lower() == 'true':
                            print ("Instance to start: " + str(db['DBInstanceIdentifier']))
                            if db['DBInstanceStatus'] == "stopped":
                                print "Starting instance '"+str(db['DBInstanceIdentifier']) + "'"
                                rds.start_db_instance(DBInstanceIdentifier=db['DBInstanceIdentifier'])
                            else:
                                print ("Not started. The instance is not stopped. The current status of instance %s is %s") %     (db['DBInstanceIdentifier'], db['DBInstanceStatus'])
                else:
                    if startOrStop == "stop":
                        for tag in taglist:
                            if tag['Key'] == activationTag and tag['Value'].lower() == 'true':
                                print ("Instance to stop: " + str(db['DBInstanceIdentifier']))
                                if db['DBInstanceStatus'] == "available":
                                    print "Stopping instance '"+str(db['DBInstanceIdentifier']) + "'"
                                    rds.stop_db_instance(DBInstanceIdentifier=db['DBInstanceIdentifier'])
                                else:
                                    print ("Not stopped. The instance is not available. The current status of instance %s is     %s")     % (db['DBInstanceIdentifier'], db['DBInstanceStatus'])
        except:
            print "Not expected error:", traceback.print_exc()
    print "---------------------------------------"
    #print("List: "+str(instanceIds))
    end_time = datetime.now()
    took_time = end_time - start_time
    print "Total time of execution: " + str(took_time)    

def lambda_handler(event, context):
    print('Managing lifecycle of RDS instances...')
    
    startOrStop_rds_instances(event['activationTag'],event['startOrStop'])