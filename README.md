# Pali Canon SQL database
All data from [SuttaCentral](https://github.com/suttacentral).

## Download the databases

[Download here](https://github.com/username/tipitaka-db)

Contains...

1. Database files separated by basket with all available languages in SuttaCentral 
2. Database files separated by basket, English translations and Pali only

Baskets separated by other languages coming soon, but it should be easy to filter out for specific langauges once you have the files downloaded by using the languge field.

## Generate the databases

1. Clone repository:
    ```
    git clone https://github.com/username/tipitaka-db.git
    ```
2. Install required dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run `main.py` file to initialize and install the database:
        ```
        python main.py
        ```
   
## Navigating the Pali Canon Database

`tipitaka-sqlite-db` contains a comprehensive collection of texts from the Pali Canon, along with their translations and related metadata. Below is a guide on navigation...

### Database Structure

The database consists of five main tables:

1. **Authors**
2. **Languages**
3. **TextInfo**
4. **LeafLineage**
5. **Translations**

#### Authors Table

Contains information about the authors of the translations.

- `author_uid`: Unique identifier for each author
- `author_short`: Short name or abbreviation for the author
- `author_fullname`: Full name of the author

#### Languages Table

Lists the languages used in the database.

- `lang`: Language code
- `lang_name`: Full name of the language

#### TextInfo Table

Contains metadata about each text in the Pali Canon.

- `uid`: Unique identifier for each text
- `parent_uid`: Identifier of the parent text (for hierarchical organization)
- `blurb`: Brief description of the text
- `original_title`: Title in the original language
- `translated_title`: Translated title
- `acronym`: Acronym or short code for the text
- `difficulty`: Indicates the difficulty level of the text
- `basket`: Specifies which basket of the Pali Canon the text belongs to
- `root_lang_name`: Name of the original language
- `root_lang`: Code of the original language
- `type`: Type or category of the text

#### LeafLineage Table

Shows the lineage or hierarchy of texts.

- `uid`: Unique identifier of the text (corresponds to TextInfo.uid)
- `lineage`: Represents the hierarchical path of the text

#### Translations Table

Contains the actual translations of the texts.

- `id`: Unique identifier for each translation
- `uid`: Identifier of the original text (corresponds to TextInfo.uid)
- `lang`: Language code of the translation
- `lang_name`: Full name of the translation language
- `author_uid`: Identifier of the translator (corresponds to Authors.author_uid)
- `file_path`: Path to the translation file (these are file paths from [sc-data](https://github.com/suttacentral/sc-data) and [bilara-data](https://github.com/suttacentral/bilara-data))
- `text`: The translated text content

### Querying

A few uses cases, querying `sutta_en.db`:

1. **Finding a specific text**:
    ```sql
    SELECT uid, original_title, translated_title
    FROM TextInfo
    WHERE original_title LIKE '%metta%' OR translated_title LIKE '%kindness%';
    ```

    Retrieves texts with "metta" and/or "kindness" in their titles.

2. **Exploring the canon structure**: 
    ```sql
    SELECT ti.uid, ti.original_title, ll.lineage
    FROM TextInfo ti
    JOIN LeafLineage ll ON ti.uid = ll.uid
    ORDER BY ll.lineage
    LIMIT 10;
    ```

    Retrieves the first 10 texts in sutta basket and their lineage.

3. **Retrieving translations**:
    ```sql
    SELECT ti.original_title, t.lang, a.author_fullname, t.text
    FROM Translations t
    JOIN TextInfo ti ON t.uid = ti.uid
    JOIN Authors a ON t.author_uid = a.author_uid
    WHERE ti.uid = 'dn1' AND t.lang = 'en'
    ```

    Retrieves basic information of the available English translations of the Digha Nikaya 1 (DN 1).
   
4. **Finding works by a specific author**: 
    ```sql
    SELECT ti.original_title, t.lang_name
    FROM Translations t
    JOIN TextInfo ti ON t.uid = ti.uid
    JOIN Authors a ON t.author_uid = a.author_uid
    WHERE a.author_fullname = 'Bhikkhu Bodhi'
    LIMIT 5;
    ```

    Lists first 5 texts translated by Bhikku Bodhi. 

5. **Exploring texts by difficulty or type**: 
    ```sql
    SELECT original_title, translated_title, difficulty
    FROM TextInfo
    WHERE difficulty like '%intermediate%'
    LIMIT 5;
    ```

    Finds first 5 suttas of intermediate difficulty.
