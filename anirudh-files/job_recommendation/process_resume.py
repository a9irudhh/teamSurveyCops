from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import pytesseract
from pdf2image import convert_from_path
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

app = Flask(__name__)
socketio = SocketIO(app)



tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def extract_text_from_pdf(file):
    images = convert_from_path(file)
    text = ''
    for image in images:
        page_text = pytesseract.image_to_string(image)
        text += page_text
    return text


def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)

    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return embeddings


def calculate_similarities(scraped_data_embeddings, cv_embedding):
    similarities = cosine_similarity(cv_embedding, scraped_data_embeddings)
    return similarities


def process_recommendations(scraped_data, cv_data):
    # Generate embeddings for all scraped job descriptions
    scraped_data_embeddings = np.vstack([get_bert_embedding(text) for text in scraped_data])
    
    # Generate embedding for the CV
    cv_embeddings = np.vstack([get_bert_embedding(text) for text in cv_data])
    
    # Calculate similarities
    similarities = calculate_similarities(scraped_data_embeddings, cv_embeddings)
    
    # Create DataFrame for recommendations
    recommendations = pd.DataFrame({
        'JobID': range(len(scraped_data)),
        'title': [f"Job {i}" for i in range(len(scraped_data))],  # Example titles
        'career level': ["Level 1"] * len(scraped_data),  # Example career levels
        'company': ["Company A"] * len(scraped_data),  # Example companies
        'location': ["Location A"] * len(scraped_data),  # Example locations
        'industry': ["Industry A"] * len(scraped_data),  # Example industries
        'salary': [50000 + 1000 * i for i in range(len(scraped_data))],  # Example salaries
        'webpage': ["webpage_url"] * len(scraped_data),  # Example webpages
        'score': similarities.flatten()
    })
    
    # Sort recommendations by similarity score
    recommendations.sort_values(by='score', ascending=False, inplace=True)
    return recommendations


@socketio.on('upload_pdf')
def handle_upload_pdf(data):
    file = data['file']  # Assuming 'file' is base64 encoded or similar format

    # Decode and save the file if necessary
    # e.g., with open('temp.pdf', 'wb') as f:
    #          f.write(file.decode('base64'))

    cv_text = extract_text_from_pdf(file)
    cv_data = [cv_text]  # Example CV data

    # Example dummy data for job descriptions
    scraped_data = [
        "Software engineer with experience in Python and machine learning.",
        "Data scientist with skills in deep learning and data analysis.",
        "Web developer proficient in HTML, CSS, and JavaScript."
    ]

    # Calculate recommendations
    recommendations = process_recommendations(scraped_data, cv_data)

    emit('response', {"message": "Processed successfully", "recommendations": recommendations.head().to_dict(orient='records')})


if __name__ == '__main__':
    socketio.run(app, debug=True)