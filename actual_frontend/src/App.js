import React, { useState, useEffect } from 'react';
import './App.css';

const App = () => {
  const [file, setFile] = useState(null);
  const [jdText, setJdText] = useState('');
  const [location, setLocation] = useState(''); // For the dropdown
  const [results, setResults] = useState([]);
  const [dropdownLocations, setDropdownLocations] = useState([]); // Dropdown options for locations

  // Handle file change
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Handle job description text change
  const handleTextChange = (event) => {
    setJdText(event.target.value);
  };

  // Handle location selection change
  const handleLocationChange = (event) => {
    setLocation(event.target.value);
  };

  // Handle form submission
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
    setDropdownLocations(data.dropdown_locations); // Populate dropdown with locations from backend
  };

  // Filter jobs by location if a location is selected
  const filteredResults = location
    ? results.filter((job) => job.Location === location)
    : results;

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

      {/* Location Dropdown */}
      {dropdownLocations.length > 0 && (
        <div className="form-group">
          <label htmlFor="locationDropdown">Filter by Location:</label>
          <select 
            id="locationDropdown" 
            value={location} 
            onChange={handleLocationChange} 
            className="input-select"
          >
            <option value="">All Locations</option>
            {dropdownLocations.map((loc, index) => (
              <option key={index} value={loc}>
                {loc}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Display filtered job results */}
      {filteredResults.length > 0 && (
        <table className="results-table">
          <thead>
            <tr>
              <th>Position</th>
              <th>Company</th>
              <th>Location</th>
              <th>Match Percentage</th>
              <th>Job URL</th>
            </tr>
          </thead>
          <tbody>
            {filteredResults.map((job, index) => (
              <tr key={index}>
                <td>{job.Position}</td>
                <td>{job.Company}</td>
                <td>{job.Location}</td>
                <td>{job['Match Percentage'].toFixed(2)}%</td>
                <td>
                  <a href={job.URL} target="_blank" rel="noopener noreferrer">
                    View Job
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default App;

