import sys
import os

def check_command_availability(command_name):
    if not os.system(f"command -v {command_name} > /dev/null 2>&1"):
        return True
    else:
        print(f"ERROR: Unable to locate the {command_name} binary.")
        print(f"FIX: Please make sure the {command_name} utility is installed and available in PATH.")
        sys.exit(1)

def concatenate_sort_uniq(file1, file2):
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            content = f1.readlines() + f2.readlines()

        # Sort and remove duplicates
        unique_sorted_content = sorted(set(content))
        return unique_sorted_content

    except FileNotFoundError as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

def main():
    # Equivalent to checking command with 'command -v'
    required_commands = ['cat', 'sort', 'uniq']
    for command in required_commands:
        check_command_availability(command)

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} file1 file2")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]

    if not os.path.isfile(file1):
        print(f"ERROR: File '{file1}' does not exist.")
        sys.exit(1)

    if not os.path.isfile(file2):
        print(f"ERROR: File '{file2}' does not exist.")
        sys.exit(1)

    result = concatenate_sort_uniq(file1, file2)
    for line in result:
        print(line, end='')

if __name__ == "__main__":
    main()