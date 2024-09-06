import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate for redirection
import "./styles/login.css";

const Forgotpass = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const navigate = useNavigate(); // Initialize useNavigate

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/forgotpass', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          new_password: formData.password,
        }),
      });

      const result = await response.json();

      if (result.success) {
        // Password reset successful
        alert(result.message); // Show success message
        navigate('/login'); // Redirect to login page
      } else {
        // Handle failure
        alert(result.message);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div className="login-page">
      <div className="box-login">
        <h2>Create New Password</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-box">
            <span className="icon">
              <ion-icon name="person"></ion-icon>
            </span>
            <input
              type="text"
              required
              name="username"
              value={formData.username}
              onChange={handleInputChange}
            />
            <label>Username</label>
          </div>

          <div className="input-box">
            <span className="icon">
              <ion-icon name="eye-off"></ion-icon>
            </span>
            <input
              type="password"
              required
              name="password"
              value={formData.password}
              onChange={handleInputChange}
            />
            <label>New Password</label>
          </div>

          <button type="submit" className="btn">
            Ok
          </button>
        </form>
      </div>
    </div>
  );
};

export default Forgotpass;
