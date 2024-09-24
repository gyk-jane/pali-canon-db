import os
from prefect import flow
from etl_scripts.util import get_postgres_data
from etl_scripts.transform.stage.generate_hierarchy import preprocess_graph, insert_graph_to_postgres
from etl_scripts.transform.stage.get_text_contents import update_translations_in_parallel

@flow(log_prints=True)
def stage_load_hierarchy_table():
    """Create and ingest hierarchical table to dev_stage
    """
    edges = get_postgres_data('dev_raw', 'super_nav_details_edges_arangodb')
    graph = preprocess_graph(edges)
    insert_graph_to_postgres(graph)
    print('graph_table created')

@flow(log_prints=True)
def run_dbt(dir: str):
    """Run dbt process to create tables in PostgreSQL.
    
    Args:
        dir (str): Directory to be run
    """
    project_dir = 'pali_canon_dbt'
    
    print('Current working directory:', os.getcwd())
    if os.path.basename(os.getcwd()) != project_dir:
        os.chdir(project_dir)
    
    os.system('env_dbt')
    os.system(f'dbt run --select {dir}')
    
@flow(log_prints=True)
def transform_stage_flow():
    """Flow to run dbt and transform data to create stage tables 
    """
    run_dbt('stage')
    stage_load_hierarchy_table()
    
    os.chdir('..')
    update_translations_in_parallel('dev_stage', 'html_text_arangodb')
    update_translations_in_parallel('dev_stage', 'sc_bilara_texts_arangodb')
    
@flow(log_prints=True)
def transform_mart_flow():
    """Flow to run dbt for mart tables.
    """
    run_dbt('mart.erd')
    