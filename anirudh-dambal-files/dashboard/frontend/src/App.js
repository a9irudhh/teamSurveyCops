import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [selectedInput, setSelectedInput] = useState(''); // To handle dropdown selection in mobile view

  const fetchData = async (endpoint) => {
    try {
      const response = await axios.get(`http://localhost:5000/${endpoint}`);
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Error fetching data');
      setData(null);
    }
  };

  const handleDropdownChange = (event) => {
    const selectedOption = event.target.value;
    setSelectedInput(selectedOption);
    fetchData(selectedOption);
  };

  const renderChart = () => {
    if (!data || !data.plot) return null;

    return (
      <div>
        <h2>{data.title}</h2>
        <img src={`data:image/png;base64,${data.plot}`} alt={data.title} />
      </div>
    );
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Data Analysis Dashboard</h1>
      </header>

      <div className="dashboard-container">
        {/* Dropdown for mobile view */}
        <div className="dashboard-dropdown">
          <select onChange={handleDropdownChange} value={selectedInput}>
            <option value="">Select Analysis</option>
            <option value="job_counts_by_experience_level">Job Counts by Experience Level</option>
            <option value="average_salary_by_experience_level">Average Salary by Experience Level</option>
            <option value="average_salary_by_work_setting">Average Salary by Work Setting</option>
            <option value="salary_distribution_by_job_category">Salary Distribution by Job Category</option>
            <option value="pie_chart_experience_level">Pie Chart - Experience Level</option>
            <option value="heatmap_salary_by_job_category">Heatmap - Salary by Job Category</option>
          </select>
        </div>

        {/* Card input for desktop view */}
        <nav className="dashboard-nav">
          <div className="card" onClick={() => fetchData('job_counts_by_experience_level')}>
            <h3>Job Counts by Experience Level</h3>
          </div>
          <div className="card" onClick={() => fetchData('average_salary_by_experience_level')}>
            <h3>Average Salary by Experience Level</h3>
          </div>
          <div className="card" onClick={() => fetchData('average_salary_by_work_setting')}>
            <h3>Average Salary by Work Setting</h3>
          </div>
          <div className="card" onClick={() => fetchData('salary_distribution_by_job_category')}>
            <h3>Salary Distribution by Job Category</h3>
          </div>
          <div className="card" onClick={() => fetchData('pie_chart_experience_level')}>
            <h3>Pie Chart - Experience Level</h3>
          </div>
          <div className="card" onClick={() => fetchData('heatmap_salary_by_job_category')}>
            <h3>Heatmap - Salary by Job Category</h3>
          </div>
        </nav>

        <main className="dashboard-content">
          {error && <div className="error">{error}</div>}
          {renderChart()}
        </main>
      </div>
    </div>
  );
}

export default Dashboard;

