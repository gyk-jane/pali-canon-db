import os
from prefect import flow
from etl_scripts.util import get_postgres_data
from etl_scripts.transform.stage.generate_hierarchy import preprocess_graph, insert_graph_to_postgres

@flow(log_prints=True)
def stage_load_hierarchy_table():
    edges = get_postgres_data('dev_raw', 'super_nav_details_edges_arangodb')
    graph = preprocess_graph(edges)
    insert_graph_to_postgres(graph)
    
@flow(log_prints=True)
def run_dbt_stage():
    project_dir = 'pali_canon_dbt'
    os.chdir(project_dir)
    
    print('Current working directory:', os.getcwd())
    
    os.system('env_dbt')
    os.system('dbt run --select stage')

@flow(log_prints=True)
def transform_stage_flow():
    run_dbt_stage()
    stage_load_hierarchy_table()
    