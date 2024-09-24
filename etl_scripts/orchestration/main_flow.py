import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from prefect import flow
from etl_scripts.orchestration.extract_and_load_flow import extract_and_load_flow, extract_arangodb_flow
from etl_scripts.orchestration.transform_flow import transform_stage_flow, transform_mart_flow

@flow(log_prints=True)
def main_flow():
    # Extract and load source tables to PostgreSQL
    extract_and_load_flow()
    
    # Transform - Stage
    transform_stage_flow()
    
    # Transform - Model
    transform_mart_flow()
    
if __name__ == '__main__':
    main_flow.serve(name="Pali Canon ETL")
