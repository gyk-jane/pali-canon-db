{{ config(
    schema='erd',
    materialized='view'
) }}

with all_info as (
    select
        sc.uid,
        graph.parent_uid,
        sc.blurb,
        sc.original_title,
        sc.translated_title,
        sc.acronym,
        sc.difficulty,
        'sutta' as basket,
        sc.root_lang_name,
        sc.root_lang,
        sc.type
    from
        {{ ref('stage_sutta_suttaplex_sc') }} as sc
    join
        {{ source('dev_stage', 'graph_table') }} as graph
        on graph.child_uid = uid

    union all

    select
        sc.uid,
        graph.parent_uid,
        sc.blurb,
        sc.original_title,
        sc.translated_title,
        sc.acronym,
        sc.difficulty,
        'vinaya' as basket,
        sc.root_lang_name,
        sc.root_lang,
        sc.type
    from
        {{ ref('stage_vinaya_suttaplex_sc') }} as sc
    join
        {{ source('dev_stage', 'graph_table') }} as graph
        on graph.child_uid = uid

    union all

    select
        sc.uid,
        graph.parent_uid,
        sc.blurb,
        sc.original_title,
        sc.translated_title,
        sc.acronym,
        sc.difficulty,
        'abhidhamma' as basket,
        sc.root_lang_name,
        sc.root_lang,
        sc.type
    from
        {{ ref('stage_abhidhamma_suttaplex_sc') }} as sc
    join
        {{ source('dev_stage', 'graph_table') }} as graph
        on graph.child_uid = uid
)

select * from all_info
