.
├── README.md
├── __pycache__
│   ├── get_sc_data.cpython-312.pyc
│   ├── ingest.cpython-312.pyc
│   └── util.cpython-312.pyc
├── data_dump
│   ├── arangodb-dump
│   │   ├── ENCRYPTION
│   │   ├── child_range_6b2cdad1dab6ad57d8d8698a5d1f9dd0.data.json.gz
│   │   ├── child_range_6b2cdad1dab6ad57d8d8698a5d1f9dd0.structure.json
│   │   ├── dump.json
│   │   ├── html_text_8a00c848c7b3360945795d3bc52ebe88.data.json.gz
│   │   ├── html_text_8a00c848c7b3360945795d3bc52ebe88.structure.json
│   │   ├── instant_search.view.json
│   │   ├── instant_volpage_search.view.json
│   │   ├── relationship_3ac08b26844221faa442e1e7eeb8a6c2.data.json.gz
│   │   ├── relationship_3ac08b26844221faa442e1e7eeb8a6c2.structure.json
│   │   ├── sc_bilara_texts_ede6cd7605f17ff53d131a783fb228e9.data.json.gz
│   │   ├── sc_bilara_texts_ede6cd7605f17ff53d131a783fb228e9.structure.json
│   │   ├── segmented_text_contents_f73a905174ffcc1e5e07b426d2e06286.data.json.gz
│   │   ├── segmented_text_contents_f73a905174ffcc1e5e07b426d2e06286.structure.json
│   │   ├── segmented_text_instant_search.view.json
│   │   ├── super_nav_details_5febf07b537b88983238c9e43447bf54.data.json.gz
│   │   ├── super_nav_details_5febf07b537b88983238c9e43447bf54.structure.json
│   │   ├── super_nav_details_edges_7d4f496668e092fa95470d8d61cf83ae.data.json.gz
│   │   ├── super_nav_details_edges_7d4f496668e092fa95470d8d61cf83ae.structure.json
│   │   ├── text_contents_ebaa3362f3751c240ff7f23fbf8b785f.data.json.gz
│   │   ├── text_contents_ebaa3362f3751c240ff7f23fbf8b785f.structure.json
│   │   ├── v_dict.view.json
│   │   └── v_text.view.json
│   ├── html_text.json
│   ├── relationship.json
│   ├── sc_bilara_texts.json
│   ├── super_nav_details.json
│   ├── super_nav_details_edges.json
│   └── text_contents.json
├── directory_structure_full.md
├── etl_scripts
│   ├── directory_structure.md
│   ├── extract
│   │   ├── __pycache__
│   │   │   ├── api_fetch.cpython-312.pyc
│   │   │   └── arangodb_fetch.cpython-312.pyc
│   │   ├── api_fetch.py
│   │   ├── arangodb_fetch.py
│   │   └── load_raw.py
│   ├── load
│   ├── orchestration
│   ├── tests
│   ├── transform
│   │   └── stage
│   │       └── parent_uid.py
│   └── util
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-312.pyc
│       │   ├── arangodb_helpers.cpython-312.pyc
│       │   └── db_connection.cpython-312.pyc
│       ├── arangodb_helpers.py
│       ├── db_connection.py
│       └── run_suttacentral.sh
├── example
│   ├── my_first_dbt_model.sql
│   ├── my_second_dbt_model.sql
│   └── schema.yml
├── logs
│   └── dbt.log
├── old
│   ├── main.py
│   ├── notes.md
│   ├── schemas
│   │   ├── abhidhamma_schema.sql
│   │   ├── sutta_schema.sql
│   │   └── vinaya_schema.sql
│   └── scripts
│       ├── __pycache__
│       │   ├── create_lang_dbs.cpython-312.pyc
│       │   ├── fetch_sc_data.cpython-312.pyc
│       │   ├── final_data_ingestion.cpython-312.pyc
│       │   └── utils.cpython-312.pyc
│       ├── create_lang_dbs.py
│       ├── fetch_sc_data.py
│       ├── final_data_ingestion.py
│       ├── preprocessing
│       │   ├── __pycache__
│       │   │   ├── data_cleanup.cpython-312.pyc
│       │   │   └── preprocessing_data_loader.cpython-312.pyc
│       │   ├── data_cleanup.py
│       │   └── preprocessing_data_loader.py
│       └── utils.py
├── pali_canon_dbt
│   ├── README.md
│   ├── analyses
│   ├── dbt_project.yml
│   ├── logs
│   │   └── dbt.log
│   ├── macros
│   ├── models
│   │   ├── source.yml
│   │   └── stage
│   │       ├── stage_html_text_arangodb.sql
│   │       ├── stage_sc_bilara_texts_arangodb.sql
│   │       ├── stage_sutta_suttaplex_sc.sql
│   │       └── stage_sutta_translations_suttaplex_sc.sql
│   ├── seeds
│   ├── snapshots
│   ├── target
│   │   ├── compiled
│   │   │   ├── pali_canon
│   │   │   │   └── models
│   │   │   │       ├── raw
│   │   │   │       │   ├── raw_html_text_arangodb.sql
│   │   │   │       │   ├── raw_sc_bilara_texts_arangodb.sql
│   │   │   │       │   ├── raw_super_nav_details_arangodb.sql
│   │   │   │       │   ├── raw_super_nav_details_edges_arangodb.sql
│   │   │   │       │   └── raw_sutta_suttaplex_sc.sql
│   │   │   │       └── stage
│   │   │   │           ├── stage_html_text_arangodb.sql
│   │   │   │           └── stage_sc_bilara_texts_arangodb.sql
│   │   │   └── pali_canon_dbt
│   │   │       └── models
│   │   │           └── stage
│   │   │               ├── stage_html_text_arangodb.sql
│   │   │               ├── stage_sc_bilara_texts_arangodb.sql
│   │   │               ├── stage_sutta_suttaplex_sc.sql
│   │   │               └── stage_sutta_translations_suttaplex_sc.sql
│   │   ├── graph.gpickle
│   │   ├── graph_summary.json
│   │   ├── manifest.json
│   │   ├── partial_parse.msgpack
│   │   ├── run
│   │   │   ├── pali_canon
│   │   │   │   └── models
│   │   │   │       ├── raw
│   │   │   │       │   ├── raw_html_text_arangodb.sql
│   │   │   │       │   ├── raw_sc_bilara_texts_arangodb.sql
│   │   │   │       │   ├── raw_super_nav_details_arangodb.sql
│   │   │   │       │   ├── raw_super_nav_details_edges_arangodb.sql
│   │   │   │       │   └── raw_sutta_suttaplex_sc.sql
│   │   │   │       └── stage
│   │   │   │           ├── stage_html_text_arangodb.sql
│   │   │   │           └── stage_sc_bilara_texts_arangodb.sql
│   │   │   └── pali_canon_dbt
│   │   │       └── models
│   │   │           └── stage
│   │   │               ├── stage_html_text_arangodb.sql
│   │   │               ├── stage_sc_bilara_texts_arangodb.sql
│   │   │               ├── stage_sutta_suttaplex_sc.sql
│   │   │               └── stage_sutta_translations_suttaplex_sc.sql
│   │   ├── run_results.json
│   │   └── semantic_manifest.json
│   └── tests
├── scratch.ipynb
└── suttacentral (this is the suttacentral github repo)
        

4215 directories, 34117 files
