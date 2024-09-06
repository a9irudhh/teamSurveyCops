from flask import Flask, jsonify, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import markdown2 
from flask_cors import CORS
import os, json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import PyPDF2
import pandas as pd
import re
from ftfy import fix_text
from nltk.corpus import stopwords
import nltk
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64



app = Flask(__name__)
CORS(app)
app.secret_key = '&%#$@56'  # Replace with a strong secret key
import google.generativeai as genai

GEMINI_KEY2 = "AIzaSyASllztebMejaExX-gVtCQj63TZWI4vXFI"

genai.configure(api_key=GEMINI_KEY2)


# model initialization
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config=genai.types.GenerationConfig(
        max_output_tokens=600,
        temperature=0.5,
        top_k=50,
        top_p=0.9,
    ),
)

# Flask-PyMongo configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/candidate_calculator"
mongo = PyMongo(app)

# Access MongoDB collection
users = mongo.db.users  # Collection for user credentials
topics_collection = mongo.db.topics
comments_collection = mongo.db.comments

@app.route('/')
def index():
    return "Welcome to the API!"

# Traditional Login Endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json  # Use JSON for communication with React frontend
    username = data['username']
    password = data['password']
    
    user = users.find_one({'username': username})
    if user and user['password'] == password:  # Plain text comparison
        session['username'] = username
        return jsonify({'message': 'Login successful', 'success': True})
    return jsonify({'message': 'Invalid username or password', 'success': False})

# Registration Endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if users.find_one({'username': username}):
        return jsonify({'message': 'Username already exists. Please choose a different one.', 'success': False})
    
    if users.find_one({'email': email}):
        return jsonify({'message': 'Email already registered. Please choose a different one.', 'success': False})
    
    users.insert_one({'username': username, 'email': email, 'password': password})  # Store plain text password
    return jsonify({'message': 'Account created successfully! You can now log in.', 'success': True})

# Forgot Password Endpoint
@app.route('/api/forgotpass', methods=['POST'])
def forgot_password():
    data = request.json
    username = data['username']
    new_password = data['new_password']
    
    user = users.find_one({'username': username})
    if not user:
        return jsonify({'message': 'Username not found. Please try again.', 'success': False})
    
    users.update_one({'username': username}, {'$set': {'password': new_password}})  # Update plain text password
    return jsonify({'message': 'Password reset successful! You can now log in with your new password.', 'success': True})

@app.route("/api/topics", methods=["GET", "POST"])
def topics():
    if request.method == "POST":
        # ADD a new topic
        topic = {
            "title": request.json.get("title"),
            "description": request.json.get("description"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
        }
        result = topics_collection.insert_one(topic)
        topic["_id"] = str(result.inserted_id)  # Convert ObjectId to string
        return jsonify(topic), 201

    topics = list(topics_collection.find())
    for topic in topics:
        topic["_id"] = str(topic["_id"])  # Convert ObjectId to string
    return jsonify({"topics": topics})

@app.route("/api/topic/<string:id>", methods=["GET", "POST"])
def topic(id):
    if request.method == "POST":
        # ADD a new comment to the topic
        comment = {
            "text": request.json.get("text"),
            "topicID": id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "like_count": 0  # Initialize like count to 0
        }
        result = comments_collection.insert_one(comment)
        comment["_id"] = str(result.inserted_id)  # Convert ObjectId to string
        return jsonify({"success": True, "message": "Comment added successfully", "comment": comment}), 201

    # GET the topic and its comments
    topic = topics_collection.find_one({"_id": ObjectId(id)})
    if not topic:
        return jsonify({"success": False, "message": "Topic not found"}), 404
    topic["_id"] = str(topic["_id"])  # Convert ObjectId to string

    comments = list(comments_collection.find({"topicID": id}))
    for comment in comments:
        comment["_id"] = str(comment["_id"])  # Convert ObjectId to string

    comments_count = comments_collection.count_documents({"topicID": id})  # Get the count of comments

    return jsonify({
        "success": True,
        "topic": topic,
        "comments": comments,
        "comments_count": comments_count
    })

@app.route("/api/topic/<string:id>/comments", methods=["POST"])
def add_comment(id):
    # ADD a new comment to the topic
    comment = {
        "text": request.json.get("text"),
        "topicID": id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "like_count": 0  # Initialize like count to 0
    }
    result = comments_collection.insert_one(comment)
    comment["_id"] = str(result.inserted_id)  # Convert ObjectId to string
    return jsonify(comment), 201

@app.route('/api/comment/<comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    # Convert the comment_id to ObjectId
    comment_object_id = ObjectId(comment_id)
    
    # Fetch the comment from the database
    comment = comments_collection.find_one({'_id': comment_object_id})
    
    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    
    # Increment the like count
    new_like_count = comment.get('like_count', 0) + 1
    comments_collection.update_one(
        {'_id': comment_object_id},
        {'$set': {'like_count': new_like_count}}
    )
    
    return jsonify({"like_count": new_like_count}), 200


QuestionAnswerWindow = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": "Please Genarate a Simple Coding Question for me based on a topic that I tell you",
        },
    ]
)


def AI_genrate(type, promptType="question"):

    # Send the prompt to the AI model

    if promptType == "question":
        prompt = f"please generate one coding Question of {type} topic and it should be simple and easy to understand and for me to solve the question must be language independent"
    else:
        prompt = f"Please check the answer to the following question write by me : {type} is correct or not please check and tell me and also tell me the correct answer to the question and also tell me the reason why the answer is correct or not and tell me the changes that I need to make in the answer and why I need to make those changes in the answer and resources that I can use to learn more about the topic please be confident about your and dont ask me to check the answer by myself"

    response = QuestionAnswerWindow.send_message(prompt)
    return response.text


@app.route("/ai_generate_question", methods=["POST"])
def ai_generate_question():

    data = request.json
    type = data.get("type")

    response_text = AI_genrate(type, "question")

    if not response_text:
        return (
            jsonify(
                {
                    "error": "No response from AI",
                    "message": "Something went wrong, please try again later",
                }
            ),
            500,
        )
    text = response_text
    text = markdown2.markdown(response_text)
    return jsonify({"question": text})


@app.route("/ai_generate_answer", methods=["POST"])
def generate_answer():

    data = request.json
    answer = data.get("answer")

    response_text = AI_genrate(answer, "answer")

    if not response_text:
        return (
            jsonify(
                {
                    "error": "No response from AI",
                    "message": "Something went wrong, please try again later",
                }
            ),
            500,
        )
    text = response_text
    text = markdown2.markdown(response_text)
    return jsonify({"responnse": text})




# Set up your API key securely
API_KEY2 = 'AIzaSyC_iJ_seRtx_OtEJO6rKYuuyOv8HrcQmvo'

# Configure the Generative AI client
genai.configure(api_key=API_KEY2)

# Initialize the Generative Model
config = {
    'temperature': 0,
    'top_k': 20,
    'top_p': 0.9,
    'max_output_tokens': 500
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=config,
    safety_settings=safety_settings
)

def format_prompt(prompt, prompt_type):
    """Format the prompt based on the type of input to ensure professional responses."""
    prompt_engineering = {
    'overall': "Please read the input carefully and format the following text professionally for a resume. Extract the main contents, keep the formatting simple, and structure the response as a clean text. Ensure that the response does not include 'json' or any additional labels or escape sequences. If you find null objects then dont generate them in the response. ",
    
    'name_contact': "Dont add unnecessary details. Please format the following name and contact details professionally for a resume. Structure it clearly as a clean JSON object with the following keys: email, linkedin, name, phone and other cpntact details that you find. Exclude 'json' and any additional labels or escape sequences:",
    
    'schooling_marks': "Dont add unnecessary details. Calculate overall grade .Please organize the following education details level-wise, starting with school and then college. Include CGPAs and percentiles where applicable in new fields, and format them professionally for a resume. Structure the response as a clean JSON object with the following keys: Education. Exclude 'json' and any additional labels or escape sequences:",
    
    'experience': "Dont add unnecessary details. Present the following experience details in a polished and professional manner suitable for a resume. Structure it as a clean JSON object with the following keys: experience. Exclude 'json' and any additional labels or escape sequences:",
    
    'projects': "Dont add unnecessary details. Include techstack that has been used in the projects, if tehy are less in number think and add what are the pre requisites for it also. Please structure the following project details in a professional and easy-to-read format appropriate for a resume. Return the response as a clean JSON object with the following keys: projects. Exclude 'json' and any additional labels or escape sequences:",
    
    'publications': "Dont add unnecessary details. Please organize and format the following publication details in a professional manner suitable for a resume. Structure the response as a clean JSON object with the following keys: publications. Exclude 'json' and any additional labels or escape sequences:",
    
    'certificates': "Dont add unnecessary details. Please structure the following certificate details in a professional and polished format suitable for a resume. Ensure clarity and return the response as a clean JSON object with the following keys: certificates. Exclude 'json' and any additional labels or escape sequences:",
    
    'description': "Dont add unnecessary details. Creatively express the individual's name and summarize their professional persona using the available data. Make it engaging and suitable for a personal description section in a resume. Structure the response as a clean JSON object with the following keys: description. Exclude 'json' and any additional labels or escape sequences:",
    }

    overall_prompt = prompt_engineering.get('overall', '')
    specific_prompt = prompt_engineering.get(prompt_type, '')
    formatted_prompt = overall_prompt + specific_prompt + prompt

    return formatted_prompt

def preprocess(response_text):
    print(type(response_text))
    try:
        response_json = json.loads(response_text)
        return response_json
    except json.JSONDecodeError:
        print("Error decoding JSON. The input text might be improperly formatted.")
        return None

def convert_to_markdown(json_data):
    """Convert JSON data into a Markdown formatted string."""
    prompt = json.dumps(json_data) + '''The attached details before this prompt are needed to be retrieved with html tags alone such that i can download the images from the html directly, use all the necessary heading, sub headings tags, br tags for new lines and properly give the output '''
    response_from_ai = model.generate_content(prompt)
    return response_from_ai.text



def generate_response(prompt, prompt_type):
    """Generate a response from the model with additional formatting instructions."""
    formatted_prompt = format_prompt(prompt, prompt_type)
    response = model.generate_content(formatted_prompt)
    return response.text

@app.route('/process_name_contact', methods=['POST'])
def process_name_contact():
    print("Entered backend")
    data = request.json
    print(data)
    prompt = data.get('name/contact')
    if not prompt:
        return jsonify({"error": "Missing 'name_contact' field"}), 400

    response_text = generate_response(prompt, 'name_contact')
    response_json = preprocess(response_text)
    if response_json:
        markdown_response = convert_to_markdown(response_json)
        return jsonify({"response": markdown_response})
    return jsonify({"error": "Failed to process response"}), 500

@app.route('/process_schooling_marks', methods=['POST'])
def process_schooling_marks():
    print("sjsdf")
    data = request.json
    prompt = data.get('schooling_marks')
    if not prompt:
        return jsonify({"error": "Missing 'schooling_marks' field"}), 400

    response_text = generate_response(prompt, 'schooling_marks')
    response_json = preprocess(response_text)
    if response_json:
        markdown_response = convert_to_markdown(response_json)
        return jsonify({"response": markdown_response})
    return jsonify({"error": "Failed to process response"}), 500

@app.route('/process_experience', methods=['POST'])
def process_experience():
    data = request.json
    prompt = data.get('experience')
    if not prompt:
        return jsonify({"error": "Missing 'experience' field"}), 400

    response_text = generate_response(prompt, 'experience')
    response_json = preprocess(response_text)
    if response_json:
        markdown_response = convert_to_markdown(response_json)
        return jsonify({"response": markdown_response})
    return jsonify({"error": "Failed to process response"}), 500

@app.route('/process_projects', methods=['POST'])
def process_projects():
    data = request.json
    print(data)
    prompt = data.get('projects')
    if not prompt:
        return jsonify({"error": "Missing 'projects' field"}), 400

    response_text = generate_response(prompt, 'projects')
    print(response_text)
    response_json = preprocess(response_text)
    if response_json:
        markdown_response = convert_to_markdown(response_json)
        return jsonify({"response": markdown_response})
    return jsonify({"error": "Failed to process response"}), 500

#--------------------------------------------------------------------------

nltk.download('stopwords')
stopw = set(stopwords.words('english'))


# Configure Generative AI client
API_KEY4 = 'AIzaSyC_iJ_seRtx_OtEJO6rKYuuyOv8HrcQmvo'
genai.configure(api_key=API_KEY4)

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
df = pd.read_csv('./venv/job_final.csv')
print(df.columns)
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
knn = KNeighborsClassifier(n_neighbors=5, metric='cosine')
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
   
    print(f"Extracted text from PDF: {text}")
    return text

@app.route('/submit', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        f = request.files['userfile']
        f.save(f.filename)

        jd_text = request.form.get('jd', '').strip()

        try:
            resume_text = extract_text_from_pdf(f.filename)
            skills_list = get_skills_from_gemini(resume_text)
            skills_text = ' '.join([skill.strip() for skill in skills_list])
        except Exception as e:
            print(f"Error processing resume: {e}")
            skills_text = ""

        resume_embeddings = vectorizer.transform([skills_text])
        jd_embeddings = vectorizer.transform([jd_text])

        # Predict the most relevant job positions using KNN
        predicted_position = knn.predict(jd_embeddings)

        # Retrieve the top 5 matches based on the Job Description
        distances, jd_indices = knn.kneighbors(jd_embeddings)

        # Extract the matched jobs
        classified_jobs = df.iloc[jd_indices[0]]

        similarity_scores = 1 - distances[0]
        match_percentages = similarity_scores * 100

        matches = pd.DataFrame({
            'Position': classified_jobs['Position'],
            'Company': classified_jobs['Company'],
            'Location': classified_jobs['Location'],
            'URL': classified_jobs['url'],
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


# --------------------------------------------------------------------

# PLEASE DONT USE THIS KEY, CREATE YOUR OWN KEY
GEMINI_KEY = "AIzaSyASllztebMejaExX-gVtCQj63TZWI4vXFI"


# model initialization
AIChatModel = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config=genai.types.GenerationConfig(
        max_output_tokens=500,
        temperature=0.5,
        top_k=50,
        top_p=0.9,
    ),
)

All_chats = []


def preprocess(response_text):
    # print(response_text)
    try:
        response_json = json.loads(response_text)
        return response_json
    except json.JSONDecodeError:
        print("Error decoding JSON. The input text might be improperly formatted.")
        return None


# Chat initialization
chat = AIChatModel.start_chat(
    history=[
        {
            "role": "user",
            "parts": "Hello! I’m reaching out for assistance with analyzing and improving my skills to help me secure a fulfilling and successful job. I’m interested in leveraging your expertise to gain a clearer understanding of my current strengths and pinpoint areas where I could enhance my abilities. My ultimate goal is to either advance in my current career or make a smooth transition into a new field that aligns with my interests and aspirations. I would greatly appreciate it if you could assess my existing skill set, offer insights into where I might need to focus my efforts, and recommend relevant resources or training opportunities that can help me strengthen my qualifications. I’m enthusiastic about collaborating with you to develop the skills necessary to achieve my career objectives and unlock new opportunities for professional growth!. note - Do not respond to anything other than the prompts related to carrer building, job hunting and skill development. if any other prompt is given, please ask the user to provide a prompt related to carrer building, job hunting and skill development.",
        },
    ]
)


def send_chat_to_AI(message, type="prompt"):

    if not message:
        return

    else:

        # TODO: Add a check for the type of message and prompt accordingly
        # TODO: Write Good prompt for the message

        if type == "question":
            prompt = (
                "Please provide a concise, 200-word verbal response to the following question"
                + message
            )
        else:
            prompt = "give a consise answer to this within 500 words: " + message

        # Send the prompt to the AI model
        response = chat.send_message(prompt)

        return response.text


@app.route("/introduce_user", methods=["POST", "GET"])
def introduce_user():

    if request.method == "POST":

        data = request.json

        presentSkills = data.get("skills")
        roleSeeking = data.get("roleSeeking")
        experience = data.get("experience")
        currentOccupation = data.get("currentOccupation")

        if not presentSkills:
            return jsonify({"error": "Please provide your skills"}), 400
        if not roleSeeking:
            return jsonify({"error": "Please provide the role you are seeking"}), 400
        if not experience:
            return jsonify({"error": "Please provide your experience"}), 400
        if not currentOccupation:
            return jsonify({"error": "Please provide your current occupation"}), 400

        message = f"I am currently working as a {currentOccupation} with {experience} years of experience in {presentSkills}. I am now looking to advance my career by transitioning into a role in {roleSeeking}. I am eager to apply my skills and knowledge in this new field, and I would greatly appreciate any guidance on how to navigate the job search process, network effectively, and prepare for interviews to position myself as a strong candidate."

        response_text = send_chat_to_AI(message)

        if not response_text:
            return (
                jsonify(
                    {
                        "error": "No response from AI",
                        "message": "Something went wrong, please try again later",
                    }
                ),
                500,
            )
        else:
            text = markdown2.markdown(response_text)
            return jsonify({"response": text})



@app.route("/chat_with_ai", methods=["POST", "GET"])
def chat_with_ai():

    if request.method == "POST":
        data = request.json
        question = data.get("question")

        if not question:
            return jsonify({"error": "Please provide a question"}), 400

        response_text = send_chat_to_AI(question, type="question")

        if not response_text:
            return (
                jsonify(
                    {
                        "error": "No response from AI",
                        "message": "Something went wrong, please try again later",
                    }
                ),
                500,
            )

        All_chats.append({"question": question, "answer": response_text})
        text = markdown2.markdown(response_text)
        return jsonify({"answer": text})



@app.route("/get_all_chats", methods=["GET"])
def get_all_chats():
    return jsonify(All_chats)

# --------------------------------------------------------------------




# Load and preprocess data
def load_and_preprocess_data(filepath):
    df = pd.read_csv(filepath)
    df['salary_in_usd'] = pd.to_numeric(df['salary_in_usd'], errors='coerce')
    df = df.dropna()
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    categorical_cols = ['experience_level', 'employment_type', 'job_title', 'employee_residence', 'work_setting', 'company_location', 'company_size', 'job_category']
    df[categorical_cols] = df[categorical_cols].astype('category')
    experience_order = ['Entry-level', 'Mid-level', 'Senior', 'Executive']
    df['experience_level'] = pd.Categorical(df['experience_level'], categories=experience_order, ordered=True)
    return df



# Load your data

df = load_and_preprocess_data('./venv/dash_data.csv')

# Utility function to encode plots as base64
def encode_plot(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

@app.route('/basic_statistics', methods=['GET'])
def basic_statistics():
    stats = df.describe(include='all').to_dict()
    return jsonify(stats)

@app.route('/job_counts_by_experience_level', methods=['GET'])
def job_counts_by_experience_level():
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='experience_level')
    plt.title('Job Counts by Experience Level')
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})

@app.route('/average_salary_by_experience_level', methods=['GET'])
def average_salary_by_experience_level():
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='experience_level', y='salary_in_usd', estimator='mean')
    plt.title('Average Salary by Experience Level')
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})



@app.route('/average_salary_by_work_setting', methods=['GET'])
def average_salary_by_work_setting():
    avg_salary_by_setting = df.groupby('work_setting')['salary_in_usd'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=avg_salary_by_setting.index, y=avg_salary_by_setting.values)
    plt.title('Average Salary by Work Setting')
    plt.xticks(rotation=45)
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})

@app.route('/salary_distribution_by_job_category', methods=['GET'])
def salary_distribution_by_job_category():
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df, x='job_category', y='salary_in_usd')
    plt.xticks(rotation=90)
    plt.title('Salary Distribution by Job Category')
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})

@app.route('/pie_chart_experience_level', methods=['GET'])
def pie_chart_experience_level():
    experience_counts = df['experience_level'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(experience_counts, labels=experience_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    plt.title('Job Distribution by Experience Level')
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})

@app.route('/heatmap_salary_by_job_category', methods=['GET'])
def heatmap_salary_by_job_category():
    pivot_table = df.pivot_table(values='salary_in_usd', index='job_category', columns='experience_level', aggfunc='mean')
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, cmap='coolwarm', fmt='.0f')
    plt.title('Heatmap of Average Salary by Job Category and Experience Level')
    plot_base64 = encode_plot(plt.gcf())
    plt.close()
    return jsonify({'plot': plot_base64})



if __name__ == '__main__':
    app.run(debug=True)
