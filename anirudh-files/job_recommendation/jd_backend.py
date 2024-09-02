from flask import Flask, render_template, redirect, request
import pandas as pd
import re
from transformers import BertTokenizer, BertModel
import torch
from sklearn.neighbors import NearestNeighbors
from pyresparser import ResumeParser # type: ignore
from docx import Document # type: ignore
import nltk #type: ignore


nltk.download('stopwords')
# Initialize the Flask app
app = Flask(__name__)

# Load the job data
df = pd.read_csv('job_final_testing.csv')
# print("Loaded job data successfully.")

# Initialize BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
# print("BERT model and tokenizer loaded.")

def get_bert_embeddings(text_list):
    # Tokenize the text
    inputs = tokenizer(text_list, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        # Get the embeddings from BERT
        outputs = model(**inputs)
    # Return the mean of the token embeddings as the text representation
    return outputs.last_hidden_state.mean(dim=1)


@app.route('/submit', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        f = request.files['userfile']
        f.save(f.filename)
        
        jd_text = request.form.get('jd', '').strip()  # Get the JD text from the form
        
        try:
            doc = Document(f.filename)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # Parse the resume using pyresparser
            data = ResumeParser(f.filename).get_extracted_data()

        except Exception as e:
            print(f"Error opening document: {e}")
            data = ResumeParser(f.filename).get_extracted_data()

        resume_skills = data.get('skills', [])
        skills_text = ' '.join(resume_skills)
        
        # Calculate BERT embeddings for the resume and the JD
        resume_embeddings = get_bert_embeddings([skills_text])
        jd_embeddings = get_bert_embeddings([jd_text])
        
        # Get BERT embeddings for job descriptions
        job_embeddings = get_bert_embeddings(df['Job_Description'].tolist())
        
        # Calculate the percentage match for each job based on cosine similarity
        nbrs = NearestNeighbors(n_neighbors=10, metric='cosine').fit(job_embeddings)
        distances, indices = nbrs.kneighbors(resume_embeddings)
        
        # Calculate similarity scores and convert them to percentage
        similarity_scores = 1 - distances[0]  # Since cosine distance is used, convert to similarity
        match_percentages = similarity_scores * 100
        
        # Create a DataFrame for the results
        matches = pd.DataFrame({
            'Position': df['Position'].iloc[indices[0]],
            'Company': df['Company'].iloc[indices[0]],
            'Location': df['Location'].iloc[indices[0]],
            'Match Percentage': match_percentages
        })
        
        # Clean location data
        matches['Location'] = matches['Location'].str.replace(r'[^\x00-\x7F]', '')
        matches['Location'] = matches['Location'].str.replace("â€“", "")
        
        # Create a sorted list of unique locations for the dropdown
        dropdown_locations = sorted(matches['Location'].unique())
        
        # Convert DataFrame to list of dictionaries
        job_list = matches.to_dict(orient='records')
        
        # Render the template with job list and dropdown locations
        return render_template('page.html', job_list=job_list, dropdown_locations=dropdown_locations)



if __name__ == "__main__":
    app.run(debug=True)
