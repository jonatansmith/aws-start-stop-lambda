# Description
This script is used in conjunction with crontab to shutdown a Linux if there is no active SSH session.
# Goal
There are cases where an EC2 instance is only used for small purposes and this automation can prevent cost waste
# Installation
Edit crontab (crontab -e) and add:  
`*/30 * * * * /home/ec2-user/autoshutdown.sh`

### Search tags
Script to shutdown EC2 if no use
Bash to stop EC2 instance after idle period
Shell script to save costs with EC2
