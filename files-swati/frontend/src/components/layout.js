import React from "react";
import { Link } from "react-router-dom";
import './styles/layout.css'; 

const Layout = ({ children }) => {
  return (
  
    <div className="Layout-body">
      <nav className="navigation">
        <div id="image-body">
          <Link to="/" className="L1">Home</Link> 
          <Link to="/about" className="L1">About</Link>
          <Link to="/forum" className="L1">Discussion Forum</Link>
          <Link to="/skill" className="L1">Skill</Link>
          <Link to="/resume" className="L1">Resume Wizard</Link>
          <Link to="/job_recom" className="L1">Job Recommendation</Link>
          <Link to="/chatbox" className="L1">Chat Box</Link>
          <Link to="/job_dash" className="L1">Job Analytics</Link>
          <Link to="/problemlist" className="L1">Practise Problems</Link>
          <Link to="/login">
          <button className="btnlogin1" onClick={() => window.location.href='login'}>Login</button>
          </Link>
        </div>
        </nav>
     
      
      {/* Page Content */}
      <main>
        {children}
        
      </main>
      </div>
      
  );
};

export default Layout;
