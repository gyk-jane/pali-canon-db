{{ config(
    schema='erd',
    materialized='view'
) }}

with all_translations as (
    select 
        t.translation_id, 
        t.uid,
        t.lang,
        t.author_uid,
        coalesce(html.local_file_path, sc.local_file_path) as local_file_path,
        'sutta' as basket
    from 
        {{ ref('stage_sutta_translations_suttaplex_sc') }} as t
    left join
        {{ ref('stage_html_text_arangodb') }} as html
        on t.translation_id = html._key
    left join {{ ref('stage_sc_bilara_texts_arangodb') }} as sc
        on t.translation_id = sc._key

    union all

    select 
        t.translation_id, 
        t.uid,
        t.lang,
        t.author_uid,
        coalesce(html.local_file_path, sc.local_file_path) as local_file_path,
        'vinaya' as basket
    from 
        {{ ref('stage_vinaya_translations_suttaplex_sc') }} as t
    left join
        {{ ref('stage_html_text_arangodb') }} as html
        on t.translation_id = html._key
    left join {{ ref('stage_sc_bilara_texts_arangodb') }} as sc
        on t.translation_id = sc._key

    union all

    select 
        t.translation_id, 
        t.uid,
        t.lang,
        t.author_uid,
        coalesce(html.local_file_path, sc.local_file_path) as local_file_path,
        'abhidhamma' as basket
    from 
        {{ ref('stage_abhidhamma_translations_suttaplex_sc') }} as t
    left join
        {{ ref('stage_html_text_arangodb') }} as html
        on t.translation_id = html._key
    left join {{ ref('stage_sc_bilara_texts_arangodb') }} as sc
        on t.translation_id = sc._key
)

select * from all_translations
where uid not in ('sutta', 'abhidhamma', 'vinaya')
