{{ config(
    schema='erd',
    materialized='view'
) }}

with all_authors as (
    select author_uid, author_short, author, 1 as priority
    from {{ ref('stage_sutta_translations_suttaplex_sc') }}
    union all
    select author_uid, author_short, author, 2 as priority
    from {{ ref('stage_vinaya_translations_suttaplex_sc') }}
    union all
    select author_uid, author_short, author, 3 as priority
    from {{ ref('stage_abhidhamma_translations_suttaplex_sc') }}
),
ranked_authors as (
    select *,
           row_number() over (partition by author_uid order by priority) as rn
    from all_authors
)

select t.author_uid,
       max(ra.author_short) as author_short,
       max(ra.author) as author
from {{ ref('Translation') }} t
left join ranked_authors ra 
    on t.author_uid = ra.author_uid 
    and ra.rn = 1
group by t.author_uid
