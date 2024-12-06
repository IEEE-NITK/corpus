import json
import re
import os

# Get the directory of the script file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the input and output JSON file paths
INPUT_FILE = os.path.join(SCRIPT_DIR, "blog_data_cpy2.json")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "blog_data_cpy3.json")

# Regex pattern to match {% static 'path' %}
STATIC_PATTERN = r"{%\s*static\s*'([^']+)'?\s*%}"
REPLACEMENT = r"media\1"

def replace_static_in_json(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Process each entry in the JSON file
    for entry in data:
        if "text" in entry:
            # Replace static tags in the "text" field
            entry["text"] = re.sub(STATIC_PATTERN, REPLACEMENT, entry["text"])

    # Save the updated data back to a new file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Updated JSON saved to {output_file}")

# Run the function
replace_static_in_json(INPUT_FILE, OUTPUT_FILE)
