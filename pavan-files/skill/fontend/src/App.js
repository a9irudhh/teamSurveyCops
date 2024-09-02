import React, { useState } from "react";
import "./App.css";

function App() {
  const [response, setResponse] = useState("");
  const [answer, setAnswer] = useState("");
  const [question, setQuestion] = useState("");
  const [questionType, setQuestionType] = useState("");

  const handleRefreshQuestion = async () => {
    console.log(questionType);
    try {
      const res = await fetch("http://127.0.0.1:5000/ai_generate_question", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ type: questionType }),
      });
      const data = await res.json();
      console.log(res);
      console.log(data);
      setQuestion(data.question);
      setResponse("");
      setQuestionType("");
      setAnswer("");
    } catch (error) {
      console.error("Error fetching new question:", error);
    }
  };

  const handleSubmit = async () => {
    console.log(questionType);
    try {
      const res = await fetch("http://127.0.0.1:5000/ai_generate_answer", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ answer: answer }),
      });
      const data = await res.json();
      console.log(res);
      console.log(data);
      setResponse(data.response);
    } catch (error) {
      console.error("Error fetching new question:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Coding Challenge</h1>
        <p>Solve the problem below and submit your solution.</p>
      </header>
      <div className="Input-header">
        <input
          type="text"
          placeholder="Enter question type (eg, string/array/etc..)"
          value={questionType}
          onChange={(e) => setQuestionType(e.target.value)}
          className="question-type-input"
        />
        <button className="refresh-button" onClick={handleRefreshQuestion}>
          Refresh Question
        </button>
      </div>
      <div className="container">
        <section className="coding-question">
          <h2>Question:</h2>
          <p dangerouslySetInnerHTML={{ __html: question }}></p>
        </section>
        <section className="solution-input">
          <h2>Your Solution:</h2>
          <textarea
            rows="30"
            cols="80"
            placeholder="Write your code here..."
            onChange={(e) => setAnswer(e.target.value)}
          ></textarea>
          <button className="submit-button" onClick={handleSubmit}>
            Submit
          </button>
        </section>
        {response && (
          <section className="response">
            <h2>Response:</h2>
            <p dangerouslySetInnerHTML={{ __html: response }}></p>
          </section>
        )}
      </div>
    </div>
  );
}

export default App;
