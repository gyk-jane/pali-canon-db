from scripts.fetch_sc_data import main as fetch_suttaplex_data
from scripts.preprocessing.preprocessing_data_loader import main as load_preprocess_db
from scripts.final_data_ingestion import main as ingest_data

if __name__  == '__main__':
    print('Fetching suttaplex from SuttaCentral API...')
    fetch_suttaplex_data()
    
    print('Loading data to preprocess.db...')
    load_preprocess_db()
    
    print('Starting final ingestion to tipitaka_db...')
    ingest_data()
    
    print('Done!')
