import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { GoogleOAuthProvider } from '@react-oauth/google';

const clientId = '860619162417-lht7l4cj48nct169gai8jfvctbbvc621.apps.googleusercontent.com'; // Replace with your actual client ID

// Create a root for React rendering
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component wrapped with GoogleOAuthProvider
root.render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={clientId}>
      <App />
    </GoogleOAuthProvider>
  </React.StrictMode>
);

// Optional: Measure performance in your app
reportWebVitals();
