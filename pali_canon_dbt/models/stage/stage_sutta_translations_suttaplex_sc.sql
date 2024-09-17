{{ config(
    schema='stage',
    alias='sutta_translations_suttaplex_sc',
    materialized='table'
) }}

with exploded_translations as (
    select
        s.uid,
        t.id as translation_id,
        t.lang,
        t.title,
        t.author,
        t.is_root,
        t.volpage,
        t.lang_name,
        t.segmented,
        t.author_uid,
        t.has_comment,
        t.author_short,
        t.publication_date
    from {{ ref('stage_sutta_suttaplex_sc') }} as s,
        jsonb_to_recordset(s.translations) as t (
            id text,
            lang text,
            title text,
            author text,
            is_root boolean,
            volpage text,
            lang_name text,
            segmented boolean,
            author_uid text,
            has_comment boolean,
            author_short text,
            publication_date text
        )
)

select * from exploded_translations
