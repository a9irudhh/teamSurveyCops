from flask import Flask, jsonify, request
from transformers import BertTokenizer, BertModel
import torch
from sklearn.neighbors import NearestNeighbors
import PyPDF2
import nltk, spacy, os
import pandas as pd
import google.generativeai as genai
from flask_cors import CORS

# Initialize spacy and nltk
# nlp = spacy.load('en_core_web_sm')
# nltk.download('stopwords')

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure Generative AI client
API_KEY = 'AIzaSyC_iJ_seRtx_OtEJO6rKYuuyOv8HrcQmvo'
genai.configure(api_key=API_KEY)

# Initialize the Generative Model
config = {
    'temperature': 0,
    'top_k': 20,
    'top_p': 0.9,
    'max_output_tokens': 500
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=config,
    safety_settings=safety_settings
)

# Load the job data
df = pd.read_csv('job_final.csv')

# Initialize BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

def get_bert_embeddings(text_list):
    inputs = tokenizer(text_list, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    # Mean pooling to get (batch_size, hidden_size)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings

def train_knn_model():
    global job_embeddings, knn_model
    job_embeddings = get_bert_embeddings(df['Job_Description'].tolist())
    knn_model = NearestNeighbors(n_neighbors=20, metric='cosine').fit(job_embeddings)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
   
    print(f"Extracted text from PDF: {text}")
    return text

def get_skills_from_gemini(resume_text):
    try:
        prompt = f"Extract the skills from the following resume text and give them as a comma-separated list:\n\n{resume_text}"
        response = model.generate_content(prompt)
        print(f"Response from GEMINI: {response.text}")
        return response.text.split(',')
    except Exception as e:
        print(f"Error fetching skills from GEMINI: {e}")
        return []

@app.route('/submit', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        f = request.files['userfile']
        f.save(f.filename)
       
        jd_text = request.form.get('jd', '').strip()
       
        try:
            resume_text = extract_text_from_pdf(f.filename)
            resume_skills = get_skills_from_gemini(resume_text)
            skills_text = ' '.join(resume_skills)
        except Exception as e:
            print(f"Error processing resume: {e}")
            skills_text = ""
       
        resume_embeddings = get_bert_embeddings([skills_text])
        jd_embeddings = get_bert_embeddings([jd_text])
       
        # Retrieve the top 11 matches (1 best match + 10 additional)
        nbrs = NearestNeighbors(n_neighbors=11, metric='cosine').fit(job_embeddings)
        distances, jd_indices = nbrs.kneighbors(jd_embeddings)
       
        # Extract the most matched job and the next 10 closest jobs
        classified_job_indices = jd_indices[0][1:11]  # Skipping the first one as it's the best match
        best_match_index = jd_indices[0][0]
        classified_jobs = df.iloc[classified_job_indices]
        best_match_job = df.iloc[[best_match_index]]
       
        # Combine the best match and the other 10 jobs
        combined_jobs = pd.concat([best_match_job, classified_jobs])

        combined_embeddings = job_embeddings[classified_job_indices].unsqueeze(0)
        nbrs_classified = NearestNeighbors(n_neighbors=combined_jobs.shape[0], metric='cosine').fit(combined_embeddings)
        distances, indices = nbrs_classified.kneighbors(resume_embeddings)
       
        similarity_scores = 1 - distances[0]
        match_percentages = similarity_scores * 100
       
        matches = pd.DataFrame({
            'Position': combined_jobs['Position'].iloc[indices[0]],
            'Company': combined_jobs['Company'].iloc[indices[0]],
            'Location': combined_jobs['Location'].iloc[indices[0]],
            'URL': combined_jobs['url'].iloc[indices[0]],
            'Match Percentage': match_percentages
        })
       
        matches['Location'] = matches['Location'].str.replace(r'[^\x00-\x7F]', '', regex=True)
        matches['Location'] = matches['Location'].str.replace("â€“", "")
       
        dropdown_locations = sorted(matches['Location'].unique())
        job_list = matches.to_dict(orient='records')
       
        os.remove(f.filename)
       
        return jsonify({
            "job_list": job_list,
            "dropdown_locations": dropdown_locations
        })

if __name__ == "__main__":
    train_knn_model()
    print("KNN model trained successfully!")
    app.run(debug=True)