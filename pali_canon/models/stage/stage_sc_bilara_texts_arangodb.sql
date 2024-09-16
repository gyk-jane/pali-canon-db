{{ config(
    schema='stage',
    alias='sc_bilara_texts_arangodb',
    materialized='view'
) }}

with transform_file_path as (
    select 
        *,
        replace(file_path, '/opt/sc/sc-flask/sc-data/', 'sc-data/') as local_file_path
    from {{ source('dev_raw', 'sc_bilara_texts_arangodb') }}
)

select * from transform_file_path

