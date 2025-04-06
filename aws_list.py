import boto3
import sys
import os

#Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#Check commands are available
def check_command_availability(command_name):
    if not os.system(f"command -v {command_name} > /dev/null 2>&1"):
        return True
    else:
        print(f"ERROR: Unable to locate the {command_name} binary.")
        print(f"FIX: Please make sure the {command_name} utility is installed and available in PATH.")
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
    required_commands = ['aws', 'cat']
    for command in required_commands:
        check_command_availability(command)

    # List running EC2 instances
    list_running_instances()


if __name__ == "__main__":
    main()