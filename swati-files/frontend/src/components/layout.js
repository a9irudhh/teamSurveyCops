import React from "react";
import { Link } from "react-router-dom";
import './layout.css'; 

const Layout = ({ children }) => {
  return (
  
    <div className="Layout-body">
      <nav className="navigation">
        <div id="image-body">
          <Link to="/" className="L1">Home</Link> 
          <Link to="/about" className="L1">About</Link>
          <Link to="/forum"className="L1">Discussion Forum</Link>
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
