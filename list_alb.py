import subprocess
import sys


def check_aws_cli():
    try:
        # Try to find the AWS CLI command
        aws_path = subprocess.check_output(['which', 'aws']).decode().strip()
        return aws_path
    except subprocess.CalledProcessError:
        # If the command fails, AWS CLI is not installed
        print("ERROR: The aws binary does not exist.")
        print("FIX: Please make sure AWS CLI is installed and available in PATH.")
        sys.exit(1)


def list_load_balancers():
    try:
        # Execute AWS CLI command to describe load balancers
        result = subprocess.check_output([
            'aws', 'elbv2', 'describe-load-balancers',
            '--query', "LoadBalancers[?Type=='application'].{Name:LoadBalancerName, ARN:LoadBalancerArn}",
            '--output', 'text'
        ]).decode().strip()

        # Check the result and print the appropriate message
        if not result:
            print("No Application Load Balancers found.")
        else:
            print("Application Load Balancers:")
            print(result)

    except subprocess.CalledProcessError as e:
        # If there's an error with the AWS CLI command
        print(f"Failed to list load balancers: {e}")
        sys.exit(1)


def main():
    check_aws_cli()
    list_load_balancers()


if __name__ == "__main__":
    main()