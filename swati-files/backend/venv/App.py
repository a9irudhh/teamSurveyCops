from flask import Flask, jsonify, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.secret_key = '&%#$@56'  # Replace with a strong secret key

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

if __name__ == '__main__':
    app.run(debug=True)
