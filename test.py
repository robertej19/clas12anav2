import json

json_file = "file_structure.json"

with open(json_file) as f:
	fs = json.load(f)

print(fs)

print(fs["fonts_dir"])
