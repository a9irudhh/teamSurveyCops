import React from "react";
import './styles/home.css';


function Home() {
  return (
    <div className="home-body">
    <header>
      <nav className="navigation1">
        <div id="image-body">
          <a href="/">Home</a>
          <a href="#">About</a>
            <a href="/forum">Discussion Forum</a>
            <a href="/skill">Skill</a>
            <a href="/resume">Resume wizard</a>
            <a href="/job_recom">Job Recommendation</a>
            <a href="/chatbox">Chat Box</a>
            <a href="/job_dash">Job Analytics</a>
            <a href="/problemlist">Practice Problems</a>
          <button className="btnlogin1" onClick={() => window.location.href='login'}>Login</button>
        </div>
      </nav>
      
      </header>
      <div className="home-main">
        <h1> Comprehensive Employment<br></br>Platform!!</h1>
        <p className="par">Discover your strengths and improve your skills!<br></br>Take our diagnostic test to assess your competencies. <br></br>Based on your results, get personalized job recommendations and<br></br>training courses to bridge your skill gaps and advance your career.</p>
        </div>
      </div>
  );
}

export default Home;
