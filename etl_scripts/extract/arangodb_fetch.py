import subprocess
from prefect import task, flow

@task(log_prints=True)
def export_arangodb_data(output_dir: str ='./data_dump/arangodb_dump') -> None:
    """Export arangodb data from arangodump command inside Docker container.

    Args:
        output_dir (str, optional): Output directory. Defaults to './data_dump'.
    """
    try:
        # Run arangodump command inside Docker container
        arangodump_cmd = [
            "docker", "exec", "-it", "sc-arangodb",
            "arangodump",
            "--server.endpoint", "tcp://127.0.0.1:8529",
            "--server.database", "suttacentral",
            "--collection", "html_text",
            "--collection", "sc_bilara_texts",
            "--output-directory", output_dir
        ]
        subprocess.run(arangodump_cmd, check=True)
        
        # Copy dump from container to project's data_dumps folder
        local_output_path = ''
        docker_cp_cmd = [
            "docker", "cp", f"sc-arangodb:{output_dir}", local_output_path
        ]
        subprocess.run(docker_cp_cmd, check=True)
        
        print(f'Data exported and copied to {local_output_path}')
    except subprocess.CalledProcessError as e:
        print(f'Error during ArangoDB data dump: {e}')