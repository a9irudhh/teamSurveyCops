from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


db = SQLAlchemy()

# Create the Flask app
app = Flask(__name__)

# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# Initialize the app with the extension
db.init_app(app)


#crating db models
class Topic(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(unique=False)
    topicID: Mapped[str]


#drop tables
with app.app_context():
    db.drop_all()
    db.create_all()

# creating tables
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        #ADD a new topic
        topic = Topic(
            title =request.form["title"],
            description =request.form["description"],
        )
        db.session.add(topic)
        db.session.commit()

    topics = db.session.execute(db.select(Topic)).scalars()

    # for tp in topics:
    #     print(tp.title, tp.description, tp.id)
       
    return render_template("index.html", topics=topics)


@app.route("/topic/<int:id>", methods=["GET", "POST"])
def topic(id):
   
    if request.method == "POST":
        #ADD a new comment to the topic
        comment = Comment(
            text =request.form["comment"],
            topicID = id,
        )
        db.session.add(comment)
        db.session.commit()

    #Pull the topic and its comments
    topic = db.get_or_404(Topic, id)
    comments = Comment.query.filter_by(topicID = id).all()

    # print(comments)
    # for comm in comments:
    #     print(comm)
    return render_template("topic.html", topic= topic, comments=comments)





# Run the app on port 5001
if __name__ == "__main__":
    app.run(debug=True, port=5001)
