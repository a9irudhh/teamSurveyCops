import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom"; // Import useNavigate for navigation
import "./login.css"; // Import your CSS file

const Register = () => {
  // State to handle form inputs
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    termsAccepted: false,
  });

  const navigate = useNavigate(); // Initialize useNavigate

  // Handler to update form data state
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      if (result.success) {
        navigate('/login'); // Redirect to login page on success
      } else {
        alert(result.message); // Display error message
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="login-page">
      <div className="box-login">
        <h2>Create Account</h2>
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
              <ion-icon name="mail"></ion-icon>
            </span>
            <input
              type="email"
              required
              name="email"
              value={formData.email}
              onChange={handleInputChange}
            />
            <label>Email</label>
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
            <label>Password</label>
          </div>
          <div className="remember-forgot">
            <label>
              <input
                type="checkbox"
                name="termsAccepted"
                checked={formData.termsAccepted}
                onChange={handleInputChange}
              />
              I agree to all terms & policies
            </label>
          </div>
          <button type="submit" className="btn">
            Register
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;
