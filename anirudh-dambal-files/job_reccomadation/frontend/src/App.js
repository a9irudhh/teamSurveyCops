import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [file, setFile] = useState(null);
  const [jdText, setJdText] = useState('');
  const [results, setResults] = useState([]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleTextChange = (event) => {
    setJdText(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('userfile', file);
    formData.append('jd', jdText);

    const response = await fetch('http://localhost:5000/submit', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    setResults(data.job_list);
  };

  return (
    <div className="container">
      <h1>Job Matching Tool</h1>
      <form className="form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="resumeFile">Upload Resume:</label>
          <input 
            type="file" 
            id="resumeFile" 
            onChange={handleFileChange} 
            accept=".doc,.docx,.pdf" 
            className="input-file"
          />
        </div>
        <div className="form-group">
          <label htmlFor="jobDescription">Job Description:</label>
          <textarea 
            id="jobDescription" 
            value={jdText} 
            onChange={handleTextChange} 
            rows="4" 
            cols="50"
            className="input-textarea"
          />
        </div>
        <button className="submit-button" type="submit">Submit</button>
      </form>
      {results.length > 0 && (
        <table className="results-table">
          <thead>
            <tr>
              <th>Position</th>
              <th>Company</th>
              <th>Location</th>
              <th>Match Percentage</th>
              <th>Job URL</th> {/* New column for the URL */}
            </tr>
          </thead>
          <tbody>
            {results.map((job, index) => (
              <tr key={index}>
                <td>{job.Position}</td>
                <td>{job.Company}</td>
                <td>{job.Location}</td>
                <td>{job['Match Percentage'].toFixed(2)}%</td>
                <td><a href={job.URL} target="_blank" rel="noopener noreferrer">View Job</a></td> {/* New cell for the URL */}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default App;
