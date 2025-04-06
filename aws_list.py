import boto3
import sys
import os

#Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#Check AWS command installsed
def check_aws_cli():
    aws = os.system("command -v aws > /dev/null 2>&1")
    if aws != 0:
        print("ERROR: The aws binary does not exist.")
        print("FIX: Please install the AWS CLI or ensure it is available in your PATH.")
        sys.exit(1)

def list_running_instances():
    ec2_client = boto3.client('ec2')
    try:
        response = ec2_client.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )

        print("List all the running EC2 instances with their InstanceIDs, Names, States, and Private IPs")
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance.get('InstanceId', 'N/A')
                state = instance.get('State', {}).get('Name', 'N/A')
                private_ip = instance.get('PrivateIpAddress', 'N/A')

                # Fetch the Name tag if it exists
                name = 'N/A'
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                        break

                print(f"InstanceID: {instance_id}, Name: {name}, State: {state}, Private IP: {private_ip}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


def main():
    clear_screen()

    # Check if AWS CLI is available
    check_aws_cli()

    # List running EC2 instances
    list_running_instances()


if __name__ == "__main__":
    main()