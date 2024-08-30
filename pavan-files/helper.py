import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import markdown2

# PLEASE DONT USE THIS KEY, CREATE YOUR OWN KEY
GEMINI_KEY = "AIzaSyDIxd85HNb1VXMTTLK5u0rVcZi5hJZiWfw"

genai.configure(api_key=GEMINI_KEY)

app = Flask(__name__)

# model initialization
model = genai.GenerativeModel(
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
chat = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": "Hello! I’m reaching out for assistance with analyzing and improving my skills to help me secure a fulfilling and successful job. I’m interested in leveraging your expertise to gain a clearer understanding of my current strengths and pinpoint areas where I could enhance my abilities. My ultimate goal is to either advance in my current career or make a smooth transition into a new field that aligns with my interests and aspirations. I would greatly appreciate it if you could assess my existing skill set, offer insights into where I might need to focus my efforts, and recommend relevant resources or training opportunities that can help me strengthen my qualifications. I’m enthusiastic about collaborating with you to develop the skills necessary to achieve my career objectives and unlock new opportunities for professional growth!",
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
            prompt = "give a consise answer to this in 500 words: " + message

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

    return render_template("information.html")


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

    return render_template("chat.html")


@app.route("/get_all_chats", methods=["GET"])
def get_all_chats():
    return jsonify(All_chats)


if __name__ == "__main__":
    app.run(debug=True)
