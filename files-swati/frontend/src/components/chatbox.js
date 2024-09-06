import React, { useState } from "react";
import "./styles/InfoStyle.css"; // Import your CSS
import { useNavigate } from "react-router-dom"; // Import useNavigate hook

const UserInfo = () => {
  const navigate = useNavigate(); // Initialize the navigate function
  const [formData, setFormData] = useState({
    presentSkills: "",
    roleSeeking: "",
    experience: "",
    currentOccupation: "",
  });

  const [aiResponse, setAiResponse] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      skills: formData.presentSkills,
      roleSeeking: formData.roleSeeking,
      experience: formData.experience,
      currentOccupation: formData.currentOccupation,
    };

    fetch("http://127.0.0.1:5000/introduce_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setAiResponse(data.response);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleChatRedirect = () => {
    navigate("/chat_ai"); // Use navigate to redirect to the /chat_ai page
  };

  return (
    <div className="main-intro-container">
      <div className="user-info">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="presentSkills">Present Skills</label>
            <input
              type="text"
              id="presentSkills"
              name="presentSkills"
              placeholder="Enter your current skills"
              value={formData.presentSkills}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="roleSeeking">Role Seeking</label>
            <input
              type="text"
              id="roleSeeking"
              name="roleSeeking"
              placeholder="Enter the role you are seeking"
              value={formData.roleSeeking}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="experience">Experience</label>
            <input
              type="text"
              id="experience"
              name="experience"
              placeholder="Enter your experience"
              value={formData.experience}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="currentOccupation">Current Occupation</label>
            <input
              type="text"
              id="currentOccupation"
              name="currentOccupation"
              placeholder="Enter your current occupation"
              value={formData.currentOccupation}
              onChange={handleChange}
            />
          </div>
          <button type="submit">Submit</button>
        </form>
      </div>
      <div>
        {aiResponse && (
          <div>
            <div
              className="ai-response"
              dangerouslySetInnerHTML={{ __html: aiResponse }}
            ></div>
            <button
              className="chat-ai-button"
              onClick={handleChatRedirect}
              style={{
                position: "fixed",
                bottom: "20px",
                left: "20px",
              }}
            >
              Chat with AI
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserInfo;
