{{ config(
    schema='erd',
    materialized='view'
) }}

with author as (
    select
        distinct t.author_uid,
        coalesce(s.author_short, v.author_short, a.author_short) as author_short,
        coalesce(s.author, v.author, a.author) as author
    from 
        {{ ref('Translation') }} as t
    left join
        {{ ref('stage_sutta_translations_suttaplex_sc') }} as s
        on t.author_uid = s.author_uid
    left join
        {{ ref('stage_vinaya_translations_suttaplex_sc') }} as v
        on t.author_uid = v.author_uid
    left join
        {{ ref('stage_abhidhamma_translations_suttaplex_sc') }} as a
        on t.author_uid = a.author_uid
)

select * from author
