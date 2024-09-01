import React, { useState } from 'react';
import Section from './Section';
import Results from './Results';
import './App.css';

function App() {
  // State to store responses for each section
  const [responses, setResponses] = useState({
    name_contact: '',
    schooling_marks: '',
    experience: '',
    projects: '',
  });

  // State to store the overall combined response
  const [overallResponse, setOverallResponse] = useState('');

  // Handle individual section responses
  const handleResponse = (section, response) => {
    setResponses(prevState => ({
      ...prevState,
      [section]: response
    }));
  };

  // Generate combined response from all sections
  const handleOverallResponse = () => {
    const combinedResponse = `
      <h2>Name/Contact</h2>
      <p>${responses.name_contact}</p>
      <h2>Schooling Marks</h2>
      <p>${responses.schooling_marks}</p>
      <h2>Experience</h2>
      <p>${responses.experience}</p>
      <h2>Projects</h2>
      <p>${responses.projects}</p>
    `;
    setOverallResponse(combinedResponse);
  };

  return (
    <div className="App">
      <h1>Resume Builder</h1>
      <div className="container">
        <div className="input-sections">
          {/* Render Section components for each part of the resume */}
          <Section
            sectionName="Name/Contact"
            apiEndpoint="/process_name_contact"
            onResponse={response => handleResponse('name_contact', response)}
          />
          <Section
            sectionName="Schooling Marks"
            apiEndpoint="/process_schooling_marks"
            onResponse={response => handleResponse('schooling_marks', response)}
          />
          <Section
            sectionName="Experience"
            apiEndpoint="/process_experience"
            onResponse={response => handleResponse('experience', response)}
          />
          <Section
            sectionName="Projects"
            apiEndpoint="/process_projects"
            onResponse={response => handleResponse('projects', response)}
          />
          {/* Button to generate the overall response */}
          <button onClick={handleOverallResponse}>Generate Overall Response</button>
        </div>

        {/* Display overall response if it exists */}
        <div className="overall-response">
          <Results response={overallResponse} />
        </div>
      </div>
    </div>
  );
}

export default App;
