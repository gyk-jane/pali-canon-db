{{ config(
    schema='stage',
    alias='test',
    materialized='table',
    post_hook=[create_index("test", "uid")]
) }}

with distinct_suttaplex as (
    select *
    from {{ source('dev_raw', 'abhidhamma_suttaplex_sc') }}
)

select * from distinct_suttaplex