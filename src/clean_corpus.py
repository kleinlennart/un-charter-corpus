import os
from pathlib import Path

data_folder = Path("data")

input_dir = data_folder / "raw"
output_dir = data_folder / "processed"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Iterate through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        input_path = os.path.join(input_dir, filename)
        output_filename = filename.replace("raw_", "clean_")
        output_path = os.path.join(output_dir, output_filename)

        # Read the content of the file
        with open(input_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Clean white spaces
        cleaned_content = " ".join(content.split())

        # Write the cleaned content to the output file
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(cleaned_content)
