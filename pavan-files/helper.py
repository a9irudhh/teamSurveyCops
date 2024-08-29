from flask import Flask, request, jsonify
import google.generativeai as genai

# PLEASE DONT USE THIS KEY, CREATE YOUR OWN KEY
# ANDH MANDH KA TOLA DUSRA JOH YEH KEY USE KAREGA WOH BKL
GEMINI_KEY = "AIzaSyCVC519rZi_VHferma_hIaAd29ww_NjFhE"

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


# Chat initialization
chat = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": "Hello! I’m reaching out for assistance with analyzing and improving my skills to help me secure a fulfilling and successful job. I’m interested in leveraging your expertise to gain a clearer understanding of my current strengths and pinpoint areas where I could enhance my abilities. My ultimate goal is to either advance in my current career or make a smooth transition into a new field that aligns with my interests and aspirations. I would greatly appreciate it if you could assess my existing skill set, offer insights into where I might need to focus my efforts, and recommend relevant resources or training opportunities that can help me strengthen my qualifications. I’m enthusiastic about collaborating with you to develop the skills necessary to achieve my career objectives and unlock new opportunities for professional growth!",
        },
    ]
)


def send_chat_to_AI(message, type="question"):
    """

    This function sends a message to the AI model and returns the response. The message can be a question or a prompt, and the type parameter specifies the type of message. The function then sends the message to the AI model and returns the response. If the response is empty, the function returns an error message. If the response is not empty, the function returns the response text.

    """

    if not message:
        return

    else:

        # TODO: Add a check for the type of message and prompt accordingly
        # TODO: Write Good prompt for the message

        if type == "question":
            prompt = (
                "Give me a consise answer to the following question in such a way : "
                + message
            )
        else:
            prompt = message

        # Send the prompt to the AI model
        response = chat.send_message(prompt)

        return response.text


@app.route("/introudce_user", methods=["POST"])
def introudce_user():

    if request.method == "POST":

        """
        Description:
        This endpoint is used to introduce the user to the AI. The user provides their skills, the role they are seeking, their experience, and their current occupation. The AI then generates a message that the user can use to introduce themselves to potential employers or network contacts. The message includes information about the user's skills, experience, and career goals, and asks for guidance on how to navigate the job search process and prepare for interviews.

        """

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
            return jsonify({"response": response_text})


@app.route("/chat_with_ai", methods=["POST"])
def chat_with_ai():
    """
    Description:
    This endpoint is used to chat with the AI. The user provides a question, and the AI responds with an answer. The question can be on any topic, and the AI will generate a response based on the input. If the question is not provided, the endpoint returns an error message. If the AI does not generate a response, the endpoint returns an error message. If the AI generates a response, the endpoint returns the response text.

    """

    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Please provide a question"}), 400

    response_text = send_chat_to_AI(question)

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

    return jsonify({"answer": response_text})
