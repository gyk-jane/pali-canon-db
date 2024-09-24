import json
from collections import defaultdict
from etl_scripts.util import connect_to_db, get_postgres_data

def preprocess_graph(edges: list) -> json:
    """Generate preprocess graph dictionary structure s.t. 
    keys are parent_uids and children are list of child_uids.

    Returns:
        json: The graph dictionary of parent and children uids
    """
    parent_to_child = defaultdict(list)
    child_uids = set()
    for edge in edges:
        _, _, _from, _to, _ = edge
        _from = _from.split('/')[1]
        _to = _to.split('/')[1]
        if _to not in child_uids:
            parent_to_child[_from].append(_to)
        child_uids.add(_to)
        
    return parent_to_child

def insert_graph_to_postgres(graph: dict) -> None:
    conn = connect_to_db()
    cur = conn.cursor()
    
    create_sql = """
    create table if not exists pali_canon.dev_stage.graph_table (
        parent_uid text,
        child_uid text
    );
    """
    cur.execute(create_sql)
    
    insert_sql = """
    insert into pali_canon.dev_stage.graph_table
    (parent_uid, child_uid) values (%s, %s)
    """
    for parent, children in graph.items():
        for child in children:
            cur.execute(insert_sql, (parent, child))
            
    conn.commit()
    cur.close()
    
    