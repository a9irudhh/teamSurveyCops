import React, { useEffect, useState } from 'react';
import './login.css'; // Import your CSS file for styles
import { Link, useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const script = document.createElement('script');
    script.src = "https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js";
    script.type = "module";
    document.body.appendChild(script);

    const scriptNoModule = document.createElement('script');
    scriptNoModule.src = "https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js";
    scriptNoModule.noModule = true;
    document.body.appendChild(scriptNoModule);

    // Clean up script elements on component unmount
    return () => {
      document.body.removeChild(script);
      document.body.removeChild(scriptNoModule);
    };
  }, []);

  const handleLoginSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // If login is successful, redirect to the home page
        navigate('/');
      } else {
        // Display error message
        setError(data.message);
      }
    } catch (err) {
      console.error('Login Error:', err);
      setError('An error occurred. Please try again.');
    }
  };

  return (
    <div className="login-page">
      <div className="box-login">
        <h2>Login</h2>
        <form onSubmit={handleLoginSubmit}>
          <div className="input-box">
            <span className="icon"><ion-icon name="person"></ion-icon></span>
            <input
              type="text"
              required
              name="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <label>Username</label>
          </div>
          <div className="input-box">
            <span className="icon"><ion-icon name="eye-off"></ion-icon></span>
            <input
              type="password"
              required
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <label>Password</label>
          </div>
          <div className="remember-forgot">
            <label><input type="checkbox" />Remember me</label>
            <p><Link to="/forgotpass" className="register-link">Forgot Password?</Link></p>
          </div>
          <button type="submit" className="btn">Login</button>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <div className="login-register">
            <p>Don't have an account? <Link to="/register" className="register-link">Create Account</Link></p>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;
