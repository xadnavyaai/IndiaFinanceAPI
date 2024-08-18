import os
import logging

from datetime import datetime

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline


# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("fund_matching.log"),
        logging.StreamHandler()
    ]
)

mf_embeddings_path = os.environ.get("mf_embeddings_path", "/home/ubuntu/finbotbackend/data/fund_embeddingas.npy")

if not os.path.exists(mf_embeddings_path):
    raise RuntimeError(f"Couldnt fine Numpy embeddings file for MF names at {mf_embeddings_path}, please set proper value in env 'mf_embeddings_path'!")

def load_embeddings(filename=mf_embeddings_path):
    """Load fund data and embeddings from a .npy file."""
    start_time = datetime.now()
    logging.info("Starting to load embeddings from file.")
    
    try:
        data = np.load(filename, allow_pickle=True).item()
    except Exception as e:
        logging.error(f"Failed to load embeddings: {e}")
        raise
    
    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds()
    logging.info(f"Finished loading embeddings. Time taken: {elapsed_time:.2f} seconds.")
    
    return data['fund_data'], data['embeddings']

def create_fund_to_code_mapping(fund_data):
    return {i[0]: i[1] for i in fund_data}

# Load data and create mappings
fund_data, embeddings = load_embeddings(mf_embeddings_path)
fund_to_code_dict = create_fund_to_code_mapping(fund_data)
    
def find_top_fund_matches(query_fund_name, fund_data=fund_data, embeddings=embeddings, fund_to_code_dict=fund_to_code_dict, top_n=3):
    """Find the top N matching mutual funds for a given query."""
    logging.info(f"Finding matches for query fund: {query_fund_name}")
    
    if query_fund_name in fund_to_code_dict:
        logging.info(f"Exact match found for fund: {query_fund_name}")
        return [{
            "fund_name": query_fund_name,
            "fund_code": fund_to_code_dict[query_fund_name],
            "cosine_similarity_score": 1.0
        }]
    else:
        logging.info("No exact match found. Calculating similarities.")
        embedder = pipeline('feature-extraction', model='sentence-transformers/all-MiniLM-L6-v2')
        query_embedding = np.array(embedder(query_fund_name)[0][0])
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        ret_list = []
        for i in top_indices:
            fund_info = {
                "fund_name": fund_data[i][0],
                "fund_code": fund_data[i][1],
                "cosine_similarity_score": similarities[i]
            }
            ret_list.append(fund_info)
            logging.info(f"Match found: {fund_info['fund_name']} with score {fund_info['cosine_similarity_score']:.2f}")
        
        return ret_list

if __name__ == "__main__":
    # Example queries
    query_fund_name = "SBI Bluechip Fund"
    top_matches = find_top_fund_matches(query_fund_name)
    print(top_matches)

    query_fund_name = "Principal Emerging Bluechip Fund - Growth Option"
    top_matches = find_top_fund_matches(query_fund_name)
    print(top_matches)
