import React, { useState } from 'react';
import axios from 'axios';

function Section({ sectionName, apiEndpoint, onResponse }) {
  const [input, setInput] = useState('');
  const [error, setError] = useState('');

  const handleInputChange = (event) => {
    setInput(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      const postData = {};
      postData[sectionName.toLowerCase().replace(' ', '_')] = input;
      console.log(`Sending data to ${apiEndpoint}:`, postData);

      const response = await axios.post(`http://127.0.0.1:5001/${apiEndpoint}`, postData);

      console.log("Response received:", response.data);

      onResponse(response.data.response);
    } catch (error) {
      setError(`Failed to process ${sectionName}.`);
      console.error("Error:", error);
    }
  };

  return (
    <div className="section">
      <h2>{sectionName}</h2>
      <textarea
        placeholder={`Enter ${sectionName} details...`}
        value={input}
        onChange={handleInputChange}
      />
      <button onClick={handleSubmit}>Submit</button>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Section;
