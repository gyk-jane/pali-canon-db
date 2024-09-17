{{ config(
    schema='erd',
    materialized='view'
) }}

with sutta_info as (
    select
        uid,
        graph.parent_uid,
        blurb,
        original_title,
        translated_title,
        acronym,
        difficulty,
        'sutta' as basket,
        root_lang_name,
        root_lang,
        type
    from
        {{ ref('stage_sutta_suttaplex_sc') }} as sc
    join
        {{ source('dev_stage', 'graph_table') }} as graph
        on graph.child_uid = uid
),
vinaya_info as (
    select
        uid,
        graph.parent_uid,
        blurb,
        original_title,
        translated_title,
        acronym,
        difficulty,
        'vinaya' as basket,
        root_lang_name,
        root_lang,
        type
    from
        {{ ref('stage_vinaya_suttaplex_sc') }} as sc
    join
        {{ source('dev_stage', 'graph_table') }} as graph
        on graph.child_uid = uid
),
abhidhamma_info as (
    select
        uid,
        graph.parent_uid,
        blurb,
        original_title,
        translated_title,
        acronym,
        difficulty,
        'abhidhamma' as basket,
        root_lang_name,
        root_lang,
        type
    from
        {{ ref('stage_abhidhamma_suttaplex_sc') }} as sc
    join
        {{ source('dev_stage', 'graph_table') }} as graph
        on graph.child_uid = uid
)

select * from sutta_info
union all
select * from vinaya_info
union all
select * from abhidhamma_info
