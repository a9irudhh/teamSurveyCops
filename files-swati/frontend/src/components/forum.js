import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './styles/forum.css'; // Import the forum CSS

const Forum = () => {
  const [topics, setTopics] = useState([]);
  const [filteredTopics, setFilteredTopics] = useState([]);
  const [newTopic, setNewTopic] = useState({ title: '', description: '' });
  const [searchQuery, setSearchQuery] = useState('');
 

  useEffect(() => {
    fetch('/api/topics')
      .then(response => response.json())
      .then(data => {
        setTopics(data.topics);
        setFilteredTopics(data.topics); // Initialize filtered topics
      })
      .catch(error => console.error('Error fetching topics:', error));
  }, []);

  useEffect(() => {
    // Filter and sort topics based on search query
    const filtered = topics
      .filter(topic => topic.title.toLowerCase().includes(searchQuery.toLowerCase()))
      .sort((a, b) => a.title.localeCompare(b.title));
    setFilteredTopics(filtered);
  }, [searchQuery, topics]);

  const handleTopicChange = (e) => {
    setNewTopic({ ...newTopic, [e.target.name]: e.target.value });
  };

  const handleTopicSubmit = (e) => {
    e.preventDefault();
    fetch('/api/topics', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newTopic),
    })
      .then(response => response.json())
      .then(data => {
        setTopics([...topics, data]);
        setNewTopic({ title: '', description: '' }); // Clear form
      })
      .catch(error => console.error('Error adding topic:', error));
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };


  return (
    <div>
      <div className="forum-container">  
        <div className="add-topic-form">
          <h1>Add a Topic</h1>
          <form onSubmit={handleTopicSubmit}>
            <div>
              <label htmlFor="title" className='title-1'>Title</label>
              <input
               
                type="text"
                name="title"
                id="title"
                value={newTopic.title}
                onChange={handleTopicChange}
                required
              />
            </div>
            <div>
              <label htmlFor="description" className='des-1'>Description</label>
              <input
                
                type="text"
                name="description"
                id="description"
                value={newTopic.description}
                onChange={handleTopicChange}
                required
              />
            </div>
            <button type="submit" className="btn">Submit</button>
          </form>
        </div>
      </div>

      <div className="search-container">
        <input
          type="text"
          placeholder="Search topics..."
          value={searchQuery}
          onChange={handleSearchChange}
          className="search-input"
        />
      </div>

      <div className="topics-list">
        <h2>Added Topics</h2>
        {filteredTopics.map((item, index) => (
          <div className="topic-item" key={item._id}>
            <div>
            <strong>
  <Link to={`/comments/${item._id}`}>{item.title}</Link>
</strong>

             
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Forum;
