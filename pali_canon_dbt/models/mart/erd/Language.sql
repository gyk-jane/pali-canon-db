{{ config(
    schema='erd',
    materialized='view'
) }}

with all_languages as (
    select lang, lang_name, 1 as priority
    from {{ ref('stage_sutta_translations_suttaplex_sc') }}
    union all
    select lang, lang_name, 2 as priority
    from {{ ref('stage_vinaya_translations_suttaplex_sc') }}
    union all
    select lang, lang_name, 3 as priority
    from {{ ref('stage_abhidhamma_translations_suttaplex_sc') }}
),
ranked_languages as (
    select *,
           row_number() over (partition by lang order by priority) as rn
    from all_languages
)

select t.lang,
       max(rl.lang_name) as lang_name
from {{ ref('Translation') }} t
left join ranked_languages rl 
    on t.lang = rl.lang 
    and rl.rn = 1
group by t.lang