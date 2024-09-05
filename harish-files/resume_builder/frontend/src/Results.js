import React from 'react';

function Results({ response }) {
  return (
    <div className="results">
      <h2>Overall Response</h2>
      <div dangerouslySetInnerHTML={{ __html: response }} />
    </div>
  );
}

export default Results;
