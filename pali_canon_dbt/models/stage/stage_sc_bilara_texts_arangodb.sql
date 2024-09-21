{{ config(
    schema='stage',
    alias='sc_bilara_texts_arangodb',
    materialized='table',
    post_hook=[create_index('sc_bilara_texts_arangodb','_key')]
) }}

with transform_file_path as (
    select 
        *,
        replace(file_path, '/opt/sc/sc-flask/sc-data/', 'sc-data/') as local_file_path
    from {{ source('dev_raw', 'sc_bilara_texts_arangodb') }}
)

select * from transform_file_path

