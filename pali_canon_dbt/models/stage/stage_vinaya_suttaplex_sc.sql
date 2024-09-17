{{ config(
    schema='stage',
    alias='vinaya_suttaplex_sc',
    materialized='table'
) }}

with distinct_suttaplex as (
    select distinct *
    from {{ source('dev_raw', 'vinaya_suttaplex_sc') }}
)

select * from distinct_suttaplex