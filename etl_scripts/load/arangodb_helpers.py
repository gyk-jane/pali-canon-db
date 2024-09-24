import subprocess
import subprocess
import platform
import time
import os
from prefect import task, flow

@task(log_prints=True)
def is_docker_running():
    """Check if Docker daemon is running."""
    try:
        subprocess.run(["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

@task(log_prints=True)
def start_docker():
    """Start Docker depending on the OS."""
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            print("Starting Docker on macOS...")
            subprocess.run(["open", "-a", "Docker"], check=True)
        elif system == "Linux":
            print("Starting Docker on Linux...")
            subprocess.run(["sudo", "systemctl", "start", "docker"], check=True)
        else:
            raise Exception(f"Unsupported operating system: {system}")
        
        # Wait for Docker to start
        print("Waiting for Docker to start...")
        for _ in range(10):  # Wait up to ~30 seconds
            if is_docker_running():
                print("Docker is running.")
                return True
            time.sleep(3)
        print("Docker did not start in time.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error starting Docker: {e}")
        return False

def start_suttacentral():
    """Start suttacentral service."""
    if not is_docker_running():
        start_docker()
        
    try:
        print("Starting sc-arangodb service...")
        subprocess.run(["docker-compose", "up", "-d"], cwd="suttacentral", check=True)
        print("suttacentral service started.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting suttacentral service: {e}")

@task(log_prints=True)
def start_sc_arangodb():
    if not is_docker_running():
        start_docker()
        
    try:
        # Start the sc-arangodb service using Docker Compose
        print("Starting sc-arangodb service...")
        subprocess.run(["docker-compose", "up", "-d", "sc-arangodb"], cwd="suttacentral", check=True)
        print("sc-arangodb service started.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting sc-arangodb service: {e}")
        
@task(log_prints=True)
def pull_submodules():
    """Update all submodules to their latest commits"""
    subprocess.run(["git", "submodule", "update", "--remote", "--merge"], check=True)
    print("All submodules updated.")
    
@task(log_prints=True)
def refresh_arangodb():
    """Pull the latest updates and refresh ArangoDB."""
    try:
        if not is_docker_running():
            print("Docker is not running.")
            if not start_docker():
                print("Failed to start Docker.")
                return

        # Start the suttacentral service if it's not running
        start_suttacentral()
        
        # Load new data into ArangoDB
        bash_script_path = 'etl_scripts/util/run_suttacentral.sh'
        subprocess.run([bash_script_path], cwd='suttacentral', check=True, shell=True)
        print("Bash script executed successfully.") 
        print("Waiting for Docker containers to initialize...")
        time.sleep(10)
        
        print("Checking Docker container status...")    
        subprocess.run(["docker", "ps"], check=True)
        
        print("Suttacentral container refreshed.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during data refresh: {e}")

if __name__ == "__main__":
    refresh_arangodb()