import os
import gzip
import json
import subprocess
from prefect import task

@task(log_prints=True)
def export_arangodb_data(collections: list, output_dir: str = '/tmp/arangodb-dump') -> None:
    """Export arangodb data from arangodump command inside Docker container.

    Args:
        output_dir (str, optional): Docker output directory. 
            Defaults to '/tmp/arangodb-dump'.
        collection (list): List of collections to be exported.
    """
    try:
        # Run arangodump command inside Docker container
        arangodump_cmd = [
            "docker", "exec", "sc-arangodb",
            "arangodump",
            "--server.endpoint", "tcp://127.0.0.1:8529",
            "--server.database", "suttacentral",
            "--output-directory", output_dir,
            "--overwrite", "true",
            "--server.password", "test"
        ]
        for collection in collections:
            arangodump_cmd.extend(["--collection", collection])
        
        print("Running command:", " ".join(arangodump_cmd))
        subprocess.run(arangodump_cmd, check=True)
              
        # Copy dump from container to project's data_dumps folder
        local_output_path = 'data_dump'
        docker_cp_cmd = [
            "docker", "cp", f"sc-arangodb:{output_dir}", local_output_path
        ]
        print("Running command:", " ".join(docker_cp_cmd))
        subprocess.run(docker_cp_cmd, check=True)
        
        print(f'Data exported and copied to {local_output_path}')
        
    except subprocess.CalledProcessError as e:
        print(f'Error during ArangoDB data dump: {e}')
        
@task(log_prints=True)
def extract_gz_file(input_gz_path: str, collection: str) -> list:
    """
    Extract a .gz file in-memory and return the JSON content as a list of dictionaries.
    Also saves it on disk.

    Args:
        input_gz_path (str): Path to the .gz file.
        collection(str): Name of the collection

    Returns:
        list: List of parsed JSON objects from the .gz file.
    """
    json_data = []  # Initialize an empty list to hold multiple JSON objects
    output_file_path = f'data_dump/{collection}.json'
    
    try:
        # Open and read the gzip file content
        with gzip.open(input_gz_path, 'rt', encoding='utf-8') as f_in:
            with open(output_file_path, 'w', encoding='utf-8') as f_out:
                # Iterate over each line and parse it as a JSON object
                for line in f_in:
                    try:
                        json_obj = json.loads(line.strip())  # Parse each line as JSON
                        json_data.append(json_obj)  # Add the parsed JSON object to the list
                        f_out.write(line)  # Write the line to the output file
                    except json.JSONDecodeError as e:
                        print(f"Error parsing line: {e}")
        
        print(f"Successfully extracted and parsed {len(json_data)} JSON objects from {input_gz_path}")
        print(f"File written to {output_file_path}")
        return json_data


    except Exception as e:
        print(f"Error extracting {input_gz_path}: {e}")
        return None
    
    