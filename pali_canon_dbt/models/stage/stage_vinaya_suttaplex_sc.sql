{{ config(
    schema='stage',
    alias='vinaya_suttaplex_sc',
    materialized='table',
    post_hook=[create_index('vinaya_suttaplex_sc','uid')]
) }}

with deduplicated_suttaplex as (
    select distinct on (uid) *
    from {{ source('dev_raw', 'vinaya_suttaplex_sc') }}
    where uid is not null
    order by uid
)

select * from deduplicated_suttaplex