import os
import json
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python diun_notify.py <path_to_json_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    # 1. Gather all DIUN environment variables
    notification_data = {k: v for k, v in os.environ.items() if k.startswith('DIUN_')}
    
    if not notification_data:
        print("No DIUN environment variables found. Exiting.")
        sys.exit(0)

    # 2. Load existing data or initialize an empty array
    data = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Ensure the root element is a list
                if not isinstance(data, list):
                    data = []
        except json.JSONDecodeError:
            # File exists but is empty or invalid; start fresh
            data = []

    # 3. Append the new object and write back to the file
    data.append(notification_data)
    
    # Ensure the target directory exists
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"Successfully appended notification to {file_path}")

if __name__ == "__main__":
    main()