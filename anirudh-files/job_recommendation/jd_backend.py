from flask import Flask, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import PyPDF2
import os
import pandas as pd
import re
from ftfy import fix_text
from nltk.corpus import stopwords
import nltk
from flask_cors import CORS
import google.generativeai as genai

nltk.download('stopwords')
stopw = set(stopwords.words('english'))

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
df['processed_text'] = df['Job_Description'].apply(lambda x: ' '.join([word for word in str(x).split() if len(word) > 2 and word not in (stopw)]))

def ngrams(string, n=3):
    string = fix_text(string)
    string = string.encode("ascii", errors="ignore").decode()
    string = string.lower()
    chars_to_remove = [")", "(", ".", "|", "[", "]", "{", "}", "'"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string)
    string = string.replace('&', 'and')
    string = string.replace(',', ' ')
    string = string.replace('-', ' ')
    string = string.title()
    string = re.sub(' +', ' ', string).strip()
    string = ' ' + string + ' '
    string = re.sub(r'[,-./]|\sBD', r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

# Initialize TF-IDF vectorizer and fit it on the job descriptions
vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase=False)
job_embeddings = vectorizer.fit_transform(df['processed_text'].values)

# Initialize the KNN classifier
knn = KNeighborsClassifier(n_neighbors=10, metric='cosine')
knn.fit(job_embeddings, df['Position'])

def get_skills_from_gemini(resume_text):
    try:
        prompt = f"Extract the skills from the following resume text and give them as a comma-separated list:\n\n{resume_text}"
        response = model.generate_content(prompt)
        print(f"Response from GEMINI: {response.text}")
        return response.text.split(',')
    except Exception as e:
        print(f"Error fetching skills from GEMINI: {e}")
        return []

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
   
    # print(f"Extracted text from PDF: {text}")
    return text

@app.route('/submit', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        f = request.files['userfile']
        f.save(f.filename)

        jd_text = request.form.get('jd', '').strip()

        try:
            # Extract resume text from the uploaded PDF
            resume_text = extract_text_from_pdf(f.filename)
            # Get the skills from the resume using GEMINI API
            skills_list = get_skills_from_gemini(resume_text)
            skills_text = ' '.join([skill.strip() for skill in skills_list])
        except Exception as e:
            print(f"Error processing resume: {e}")
            skills_text = ""

        # Generate embeddings for the resume text and JD text
        resume_embeddings = vectorizer.transform([skills_text])
        jd_embeddings = vectorizer.transform([jd_text])

        # Predict the most relevant job positions using KNN (based on JD)
        distances_jd, jd_indices = knn.kneighbors(jd_embeddings)

        # Predict the most relevant job positions using KNN (based on resume)
        distances_resume, resume_indices = knn.kneighbors(resume_embeddings)

        # Ensure both JD and resume are matching with the same jobs (top 10 neighbors for both)
        jd_top_matches = df.iloc[jd_indices[0]]
        resume_top_matches = df.iloc[resume_indices[0]]

        # Calculate combined distance by averaging the JD and resume distances
        aggregated_distances = distances_resume[0]

        # Convert aggregated distances into similarity scores (1 - distance)
        aggregated_similarity_scores = 1 - aggregated_distances

        # Calculate match percentages based on aggregated similarity scores
        match_percentages = aggregated_similarity_scores * 100

        # Create a DataFrame for the final matches
        matches = pd.DataFrame({
            'Position': jd_top_matches['Position'],
            'Company': jd_top_matches['Company'],
            'Location': jd_top_matches['Location'],
            'URL': jd_top_matches['url'],
            'Aggregated Match Percentage': match_percentages
        })

        # Clean up any unwanted characters in the location
        matches['Location'] = matches['Location'].str.replace(r'[^\x00-\x7F]', '', regex=True)
        matches['Location'] = matches['Location'].str.replace("â€“", "")

        # Extract unique values before modifying the DataFrame
        dropdown_locations = sorted(matches['Location'].unique())
        dropdown_position = sorted(matches['Position'].unique())
        
        # remove redundant values in the matches dataframe
        matches = matches.drop_duplicates(subset=['Position', 'Company', 'Location', "URL"])
        job_list = matches.to_dict(orient='records')

        # Remove the uploaded file after processing
        os.remove(f.filename)

        # Return the response
        return jsonify({
            "job_list": job_list,
            "dropdown_position": dropdown_position,
            "dropdown_locations": dropdown_locations
        })


if __name__ == "__main__":
    app.run(debug=True)
