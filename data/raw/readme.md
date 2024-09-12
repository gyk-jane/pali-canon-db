# Collections source

The .json files in this directory are from the SuttaCentral arangodb database. 
The arangodb database can be accessed through Docker, directions [here](https://github.com/suttacentral/suttacentral?tab=readme-ov-file#15-working-with-arangodb).
(Note: make sure to go through [Setting up the project and first run](https://github.com/suttacentral/suttacentral?tab=readme-ov-file#10-setting-up-the-project-and-first-run)
before running docker compose)

To export the collections `html_text` and `sc_bilara_texts`, run the following commands:

        docker exec -it sc-arangodb arangodump --server.endpoint tcp://127.0.0.1:8529 --server.database suttacentral --collection html_text --collection sc_bilara_texts --output-directory /tmp/arangodb-dump

        docker cp sc-arangodb:/tmp/arangodb-dump /your/path

Then extract .gz files to retrieve the .json files.