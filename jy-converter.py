#!/bin/python3

# Copyright Maen Artimy, 2024

import json
import yaml
import argparse
import os

def json_to_yaml(input_file, output_file):
    with open(input_file, 'r') as f:
        json_data = json.load(f)
    with open(output_file, 'w') as f:
        yaml.dump(json_data, f, default_flow_style=False)
    print(f"Converted JSON to YAML and saved to {output_file}")

def yaml_to_json(input_file, output_file):
    with open(input_file, 'r') as f:
        yaml_data = yaml.safe_load(f)
    with open(output_file, 'w') as f:
        json.dump(yaml_data, f, indent=4)
    print(f"Converted YAML to JSON and saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert between JSON and YAML files.")
    parser.add_argument("input_file", help="Input file name")
    parser.add_argument("output_file", nargs='?', help="Output file name (optional)")

    args = parser.parse_args()

    input_ext = os.path.splitext(args.input_file)[1].lower()

    if args.output_file:
        output_ext = os.path.splitext(args.output_file)[1].lower()
    else:
        # Determine the output file name based on input file extension
        if input_ext == ".json":
            args.output_file = os.path.splitext(args.input_file)[0] + ".yaml"
            output_ext = ".yaml"
        elif input_ext in [".yml", ".yaml"]:
            args.output_file = os.path.splitext(args.input_file)[0] + ".json"
            output_ext = ".json"
        else:
            print("Unsupported input file extension. Please use a .json or .yaml file.")
            return

    if input_ext == ".json" and output_ext in [".yml", ".yaml"]:
        json_to_yaml(args.input_file, args.output_file)
    elif input_ext in [".yml", ".yaml"] and output_ext == ".json":
        yaml_to_json(args.input_file, args.output_file)
    else:
        print("Unsupported file conversion. Please ensure you are converting JSON to YAML or YAML to JSON.")

if __name__ == "__main__":
    main()
