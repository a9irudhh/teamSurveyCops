import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import "./styles/comments.css"

const Comments = () => {
  const { id } = useParams(); // Get topic ID from URL
  const [topic, setTopic] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [likedComments, setLikedComments] = useState(new Set()); // Track liked comments using a Set
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch the topic details and comments when component mounts
    console.log("Fetching data for topic ID:", id); // Debugging line
    fetch(`/api/topic/${id}`)  // Ensure this endpoint is correct
      .then(response => response.json())
      .then(data => {
        if (data.topic) {
          setTopic(data.topic); // Set the topic data
        } else {
          console.error('Error: Topic not found in response:', data);
        }
        if (data.comments) {
          setComments(data.comments); // Set the comments data with like counts from the database
        } else {
          console.error('Error: Comments not found in response:', data);
        }
      })
      .catch(error => console.error('Error fetching topic details:', error));
  }, [id]);

  const handleCommentChange = (e) => {
    setNewComment(e.target.value);
  };

  const handleCommentSubmit = (e) => {
    e.preventDefault();
    
    // Ensure we are submitting a valid comment
    if (newComment.trim() === '') return;

    // Send POST request to add a new comment
    fetch(`/api/topic/${id}/comments`, {  // Ensure this endpoint is correct
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: newComment }),
    })
      .then(response => response.json())
      .then(data => {
        setComments([...comments, data]); // Add new comment to state
        setNewComment(''); // Clear the input field
      })
      .catch(error => console.error('Error adding comment:', error));
  };

  const handleLikeComment = (commentId) => {
    const isLiked = likedComments.has(commentId); // Check if the comment is already liked

    fetch(`/api/comment/${commentId}/${isLiked ? 'unlike' : 'like'}`, { // Toggle like/unlike endpoint
      method: 'POST',
    })
      .then(response => response.json())
      .then(data => {
        // Update the comment with the new like count from the response
        setComments(comments.map(comment => 
          comment._id === commentId ? { ...comment, like_count: data.like_count } : comment
        ));

        // Update the liked comments set based on whether the comment was already liked
        setLikedComments(prevLikedComments => {
          const updatedLikedComments = new Set(prevLikedComments);
          if (isLiked) {
            updatedLikedComments.delete(commentId); // Remove from liked if already liked
          } else {
            updatedLikedComments.add(commentId); // Add to liked if not already liked
          }
          return updatedLikedComments;
        });
      })
      .catch(error => console.error('Error toggling like for comment:', error));
  };

  if (!topic) {
    return <p>Loading topic...</p>; // Show loading message while fetching data
  }

  return (
    <>
      <div className="topic-container">
        {/* Back to Discussion Forum Button */}
        <button onClick={() => navigate('/forum')} style={{ marginBottom: '20px' }}>
          Back to Discussion Forum
        </button>

        {/* Topic Details */}
        <div className="topic-details">
          <h1>{topic.title}</h1>
          <p>{topic.description}</p>
          <div className="topic-meta">
            <small>Date: {topic.date} Time: {topic.time}</small>
          </div>
        </div>
      </div>

      {/* Comments Section */}
      <div className="comments-section">
        <h2>Comments ({comments.length})</h2>
        {comments.map((comm) => (
          <div className="comment-item" key={comm._id}>
            <p>
              <strong>User</strong>
              <small>Date: {comm.date} Time: {comm.time}</small>
              <span>{comm.text}</span>
            </p>
            <button
              className="like-button"
              onClick={() => handleLikeComment(comm._id)}
            >
              <svg width="24" height="24" xmlns="http://www.w3.org/2000/svg">
                <title>Like</title>
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill={likedComments.has(comm._id) ? 'red' : 'gray'}/>
              </svg>
              <span>{comm.like_count || 0}</span> {/* Display the actual like count */}
            </button>
          </div>
        ))}
      </div>

      {/* Add Comment Form */}
      <form onSubmit={handleCommentSubmit} className="add-comment-form">
      <h2 className='SelfMadeTitle'>Add a Comment</h2>
        <div>
          <label htmlFor="comment">Comment</label>
          <input
            type="text"
            name="comment"
            id="comment"
            value={newComment}
            onChange={handleCommentChange}
            required
          />
        </div>
        <button className='SelfMadeButton' type="submit">Submit</button>
      </form>
    </>
  );
};

export default Comments;
