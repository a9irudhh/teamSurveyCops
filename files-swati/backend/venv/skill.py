
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


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)
