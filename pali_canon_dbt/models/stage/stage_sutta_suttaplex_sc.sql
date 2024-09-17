{{ config(
    schema='stage',
    alias='sutta_suttaplex_sc',
    materialized='table'
) }}

with distinct_suttaplex as (
    select distinct *
    from {{ source('dev_raw', 'sutta_suttaplex_sc') }}
)

select * from distinct_suttaplex