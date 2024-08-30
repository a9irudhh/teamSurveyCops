from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from datetime import datetime  # Import datetime to get the current date


# Create the Flask app
app = Flask(__name__)

# Configure the MongoDB database
app.config["MONGO_URI"] = "mongodb://localhost:27017/projectDB"

# Initialize the app with the MongoDB extension
mongo = PyMongo(app)

# Creating collections
topics_collection = mongo.db.topics
comments_collection = mongo.db.comments

# Uncomment the following block if you want to drop the collections on startup
# ----------------------------------------------------------
def drop_collections():
    topics_collection.drop()
    comments_collection.drop()
    print("Dropped 'topics' and 'comments' collections.")

# drop_collections()
# --



@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # ADD a new topic
        topic = {
            "title": request.form["title"],
            "description": request.form["description"],
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
        }
        topics_collection.insert_one(topic)

    topics = topics_collection.find()

    return render_template("index.html", topics=topics)


@app.route("/topic/<string:id>", methods=["GET", "POST"])
def topic(id):
    if request.method == "POST":
        # ADD a new comment to the topic
        comment = {
            "text": request.form["comment"],
            "topicID": id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
        }
        comments_collection.insert_one(comment)

    # Pull the topic and its comments
    topic = topics_collection.find_one({"_id": ObjectId(id)})
    comments_count = comments_collection.count_documents({"topicID": id})  # Get the count of comments
    comments = list(comments_collection.find({"topicID": id}))  # Fetch the comments

    return render_template("topic.html", topic=topic, comments=comments, comments_count=comments_count)


# Run the app on port 5001
if __name__ == "__main__":
    app.run(debug=True, port=5001)
