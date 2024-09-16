{{ config(
    schema='stage',
    alias='html_text_arangodb',
    materialized='view'
) }}

with transform_file_path as (
    select 
        *,
        replace(file_path, '/opt/sc/sc-flask/sc-data/', 'sc-data/') as local_file_path
    from {{ source('dev_raw', 'html_text_arangodb') }}
)

select * from transform_file_path

