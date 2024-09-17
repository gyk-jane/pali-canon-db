# pali-canon-db

## Download the databases
Download the pre-uploaded databases:

1. Go to the project's repository on GitHub: [link to repository](https://github.com/username/tipitaka-db)
2. Navigate to the "Databases" folder.
3. Download the desired database files.


## Generate the databases
To run the files and access the databases, follow these steps:

1. Make sure you have the necessary dependencies installed. You can find the list of dependencies in the project's `requirements.txt` file.

2. Clone the repository to your local machine:
    ```
    git clone https://github.com/username/tipitaka-db.git
    ```

3. Navigate to the project directory:
    ```
    cd tipitaka-db
    ```

4. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

    1. Run the `main.py` file to start the application and initialize the database:
        ```
        python main.py
        ```
    2. Once the application is running, you can access the SQLite database using a tool like SQLite Browser or the command line interface. Make sure you have SQLite installed on your machine.

    That's it! You should now be able to run the files and access the databases for the `tipitaka-db` project.

## Navigating the Pali Canon Database

This database contains a comprehensive collection of texts from the Pali Canon, along with their translations and related metadata. Below is a guide on how to navigate and use this database effectively.

### Database Structure

The database consists of five main tables:

1. **Authors**
2. **Languages**
3. **TextInfo**
4. **LeafLineage**
5. **Translations**

#### Authors Table

This table contains information about the authors of the translations.

- `author_uid`: Unique identifier for each author
- `author_short`: Short name or abbreviation for the author
- `author_fullname`: Full name of the author

#### Languages Table

This table lists the languages used in the database.

- `lang`: Language code
- `lang_name`: Full name of the language

#### TextInfo Table

This table contains metadata about each text in the Pali Canon.

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

This table shows the lineage or hierarchy of texts.

- `uid`: Unique identifier of the text (corresponds to TextInfo.uid)
- `lineage`: Represents the hierarchical path of the text

#### Translations Table

This table contains the actual translations of the texts.

- `id`: Unique identifier for each translation
- `uid`: Identifier of the original text (corresponds to TextInfo.uid)
- `lang`: Language code of the translation
- `lang_name`: Full name of the translation language
- `author_uid`: Identifier of the translator (corresponds to Authors.author_uid)
- `file_path`: Path to the translation file
- `text`: The translated text content

### Querying the Database

To navigate and query the database effectively, consider the following approaches:

1. **Finding a specific text**: 
   Use the `TextInfo` table to search by `uid`, `original_title`, or `translated_title`.

2. **Exploring the canon structure**: 
   Use the `LeafLineage` table in conjunction with `TextInfo` to understand the hierarchical organization of texts.

3. **Retrieving translations**: 
   Join the `Translations` table with `TextInfo` to get translations for specific texts.

4. **Finding works by a specific author**: 
   Use the `Authors` table joined with `Translations` to find all translations by a particular author.

5. **Exploring texts by difficulty or type**: 
   Query the `TextInfo` table using the `difficulty` or `type` fields to find texts of a particular category or complexity level.

Example SQL query to get all translations of a specific text:

```sql
SELECT t.text, t.lang_name, a.author_fullname
FROM Translations t
JOIN TextInfo ti ON t.uid = ti.uid
JOIN Authors a ON t.author_uid = a.author_uid
WHERE ti.original_title = 'Your Text Title Here';
```

This structure allows for flexible navigation and querying of the Pali Canon texts, their translations, and associated metadata.
