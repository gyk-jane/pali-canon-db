(proposed)

/pali-canon-etl/
│
├── /extract/
│   ├── api_fetch.py  # Functions to fetch data from the APIs (e.g., SC API, ArangoDB)
│   ├── db_extract.py  # For pulling data from ArangoDB backend
│   ├── create_tables.py  # SQL scripts to dynamically create tables in PostgreSQL
│   └── load_raw.py  # Load raw data into the new schema in PostgreSQL
│
├── /transform/
│   ├── /stage/
│   │   ├── deduplication.py  # Basic cleanup and deduplication scripts
│   │   ├── create_stage_tables.py  # Create staging tables
│   │   ├── transform_stage.py  # Simple transformations, e.g., handling duplicates
│   │   └── decode_unicode.py  # Custom transformations like decoding Unicode
│   ├── /model/
│   │   ├── create_model_tables.py  # Scripts for creating model tables (fact/dim tables)
│   │   └── transform_model.py  # More complex transformations to model the data
│   └── dbt_models/  # Store dbt transformation models (e.g., `sutta_plex_sc`, `author_info`)
│
├── /load/
│   ├── load_to_postgres.py  # Final loading of cleaned/model tables to PostgreSQL
│   └── ready_for_query/  # Ready-to-use SQL for querying or testing the final data structure
│
├── /orchestration/
│   ├── prefect_flow.py  # Prefect flow for orchestrating the ETL process
│   └── config.py  # Configuration settings for Prefect and database connections
│
├── /tests/
│   └── test_extract.py  # Test cases for extraction step
│   └── test_transform.py  # Test cases for transformations
│   └── test_load.py  # Test cases for loading step
│
└── README.md  # Documentation for the ETL pipeline setup and usage