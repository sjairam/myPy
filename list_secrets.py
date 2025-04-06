import subprocess
import sys
import argparse
import json
#Initial version - sj


#Check command availability .. pass as params
def check_command_availability(command, name):
    try:
        path = subprocess.check_output(['which', command]).decode().strip()
        return path
    except subprocess.CalledProcessError:
        print(f"ERROR: The {name} binary does not exist.")
        print(f"FIX: Please make sure {name} is installed and available in PATH.")
        sys.exit(1)

def help_message():
    print("Displays IN PLAIN TEXT the Key-Value pairs for secrets in Secrets Manager")
    print()
    print("Syntax: list_secrets.py [-h|-s env/stack-secrets| -a]")
    print("options:")
    print("-h                     Print this message.")
    print("-s env/stack-secrets   Prints just secrets for that stack.")
    print("-a                     Prints all secrets in Secrets Manager (not advised).")
    print()

def list_all_secrets():
    result = subprocess.check_output([
        'aws', 'secretsmanager', 'list-secrets',
        '--query', 'SecretList[*].Name',
        '--output', 'text'
    ]).decode().strip()
    return result.split()

def describe_secret(secret_name):
    try:
        secret_value = subprocess.check_output([
            'aws', 'secretsmanager', 'get-secret-value',
            '--secret-id', secret_name,
            '--query', 'SecretString',
            '--output', 'text'
        ]).decode().strip()

        print(f"Secret Name: {secret_name}")
        print("Key-Value Pairs:")
        print(json.loads(secret_value))
    except subprocess.CalledProcessError as e:
        print(f"Failed to describe secret {secret_name}: {e}")
        sys.exit(1)

def find_whitespaces(secret_name):
    try:
        raw_output = subprocess.check_output([
            'aws', 'secretsmanager', 'get-secret-value',
            '--secret-id', secret_name
        ]).decode()

        secret_string = json.loads(raw_output).get('SecretString', '')
        if ' ' in secret_string or '\'' in secret_string:
            print(f"{secret_name} WHITESPACEs FOUND - check the output for leading or trailing spaces.")
        else:
            print("No whitespace found.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to check secret {secret_name} for whitespaces: {e}")
        sys.exit(1)

def main():
    # Check if AWS CLI and jq are available
    check_command_availability('aws', 'AWS CLI')
    check_command_availability('jq', 'jq')

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process some secrets.")
    parser.add_argument('-a', action='store_true', help="Prints all secrets in Secrets Manager (not advised).")
    parser.add_argument('-s', metavar='secret_name', type=str, help="Prints just secrets for that stack.")
    args = parser.parse_args()

    if args.a:
        print("Listing all secrets:")
        all_secrets = list_all_secrets()
        for secret in all_secrets:
            describe_secret(secret)
    elif args.s:
        describe_secret(args.s)
        find_whitespaces(args.s)
    else:
        help_message()

if __name__ == "__main__":
    main()