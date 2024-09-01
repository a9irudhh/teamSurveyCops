from flask import Flask, render_template, redirect, request
import pandas as pd
import re
from transformers import BertTokenizer, BertModel
import torch
from sklearn.neighbors import NearestNeighbors
from pyresparser import ResumeParser
from docx import Document

# Initialize the Flask app
app = Flask(__name__)

# Load the job data
df = pd.read_csv('job_final.csv')
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
        # print(f"Saved file: {f.filename}")
        
        try:
            doc = Document(f.filename)
            # print("Document opened successfully.")
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

            # Parse the resume using pyresparser
            data = ResumeParser(f.filename).get_extracted_data()
            # print(f"Extracted data: {data}")

        except Exception as e:
            print(f"Error opening document: {e}")
            data = ResumeParser(f.filename).get_extracted_data()


        resume_skills = data.get('skills', [])
        # print(f"Extracted skills: {resume_skills}")

        skills_text = ' '.join(resume_skills)
        
        resume_embeddings = get_bert_embeddings([skills_text])
        # print("Resume BERT embeddings calculated.")

        # Get BERT embeddings for job descriptions
        job_embeddings = get_bert_embeddings(df['Job_Description'].tolist())
        # print("Job descriptions BERT embeddings calculated.")



        # Find the nearest neighbors using BERT embeddings
        nbrs = NearestNeighbors(n_neighbors=10, metric='cosine').fit(job_embeddings)
        distances, indices = nbrs.kneighbors(resume_embeddings)


        # Create a list of matching jobs with their distances
        matches = pd.DataFrame({
            'Position': df['Position'].iloc[indices[0]],
            'Company': df['Company'].iloc[indices[0]],
            'Location': df['Location'].iloc[indices[0]],
            'Match Confidence': distances[0]
        })
        
        # Clean location data
        matches['Location'] = matches['Location'].str.replace(r'[^\x00-\x7F]', '')
        matches['Location'] = matches['Location'].str.replace("â€“", "")
        
        # Create a sorted list of unique locations for the dropdown
        dropdown_locations = sorted(matches['Location'].unique())
        
        # Create a list of dictionaries for job positions
        job_list = matches.to_dict(orient='records')
        print(f"Job list created with {len(job_list)} entries.")

        # Render the template with job list and dropdown locations
        return render_template('page.html', job_list=job_list, dropdown_locations=dropdown_locations)

if __name__ == "__main__":
    app.run(debug=True)
