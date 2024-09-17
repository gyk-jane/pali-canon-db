{{ config(
    schema='erd',
    materialized='view'
) }}

with langauge as (
    select
        distinct t.lang,
        coalesce(s.lang_name, v.lang_name, a.lang_name) as lang_name
    from 
        {{ ref('Translation') }} as t
    left join
        {{ ref('stage_sutta_translations_suttaplex_sc') }} as s
        on t.lang = s.lang
    left join
        {{ ref('stage_vinaya_translations_suttaplex_sc') }} as v
        on t.lang = v.lang
    left join
        {{ ref('stage_abhidhamma_translations_suttaplex_sc') }} as a
        on t.lang = a.lang
)

select * from langauge
