from prefect import flow
from orchestration.extract_flow import extract_flow
from orchestration.transform_flow import transform_flow
from orchestration.load_flow import load_flow

@flow
def main_flow():
    extract_flow()
    transform_flow()
    load_flow()
    
if __name__ == '__main__':
    main_flow()
