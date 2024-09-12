import gzip
import shutil
import subprocess
from prefect import task, flow

@task(log_prints=True)
def export_arangodb_data(output_dir: str = '/tmp/arangodb-dump') -> None:
    """Export arangodb data from arangodump command inside Docker container.

    Args:
        output_dir (str, optional): Docker output directory. 
            Defaults to '/tmp/arangodb-dump'.
    """
    try:
        # Run arangodump command inside Docker container
        arangodump_cmd = [
            "docker", "exec", "sc-arangodb",
            "arangodump",
            "--server.endpoint", "tcp://127.0.0.1:8529",
            "--server.database", "suttacentral",
            "--collection", "html_text",
            "--collection", "sc_bilara_texts",
            "--output-directory", output_dir,
            "--overwrite", "true",
            "--server.password", "test"
        ]
        print("Running command:", " ".join(arangodump_cmd))
        subprocess.run(arangodump_cmd, check=True)
              
        # Copy dump from container to project's data_dumps folder
        local_output_path = '/Users/janekim/Developer/tipitaka_db/data_dump'
        docker_cp_cmd = [
            "docker", "cp", f"sc-arangodb:{output_dir}", local_output_path
        ]
        print("Running command:", " ".join(docker_cp_cmd))
        subprocess.run(docker_cp_cmd, check=True)
        
        print(f'Data exported and copied to {local_output_path}')
    except subprocess.CalledProcessError as e:
        print(f'Error during ArangoDB data dump: {e}')
        
@task(log_prints=True)
def extract_gz_file(input_gz_path: str, output_file_path: str) -> None:
    """
    Extract a .gz file and write the decompressed content to an output file.

    Args:
        input_gz_path (str): Path to the .gz file.
        output_file_path (str): Path where the decompressed content will be written.
    """
    try:
        with gzip.open(input_gz_path, 'rb') as f_in:
            with open(output_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"File extracted to {output_file_path}")
    except Exception as e:
        print(f"Error extracting {input_gz_path}: {e}")    
        
if __name__ == "__main__":
    html_in = 'data_dump/arangodb-dump/html_text_8a00c848c7b3360945795d3bc52ebe88.data.json.gz'
    sc_bilara_in = 'data_dump/arangodb-dump/sc_bilara_texts_ede6cd7605f17ff53d131a783fb228e9.data.json.gz'
    html_out = 'data_dump/html_text.json'
    sc_bilara_out = 'data_dump/sc_bilara_texts.json'
    export_arangodb_data()
    extract_gz_file(html_in, html_out)
    extract_gz_file(sc_bilara_in, sc_bilara_out)
    