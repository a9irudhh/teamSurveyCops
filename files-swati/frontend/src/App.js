import React from "react";

import Login from "./components/login";
import Register from "./components/register";
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom'; 
import Home from "./components/home";
import Layout from "./components/layout";
import Forgotpass from "./components/forgotpass";
import Forum from "./components/forum";
import Comments from "./components/comments";
import Skill from "./components/skill";
import Resume from "./components/resume";
import Jobcom from "./components/job_recom";
import UserInfo from "./components/chatbox";
import Chatai from "./components/chat_ai";
import Dashboard from "./components/job_dash";
import Problems from "./components/problemlist";

const AppContent = () => {
  const location = useLocation();
  const isAuthPage = location.pathname === '/login' || location.pathname === '/register' || location.pathname === '/forgotpass' || location.pathname === '/forum' ||  location.pathname === '/skill' ||  location.pathname === '/resume' || location.pathname === '/job_recom' || location.pathname === '/chatbox' || location.pathname === '/job_dash' ||  location.pathname === '/problemlist' ;
  return (
    <>
      {isAuthPage ? (
        <Layout>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgotpass" element={<Forgotpass />} />
            <Route path="/forum" element={<Forum />} />
            <Route path="/skill" element={<Skill />} />
            <Route path="/resume" element={<Resume />} />
            <Route path="/job_recom" element={<Jobcom />} />
            <Route path="/chatbox" element={<UserInfo />} />
            <Route path="/job_dash" element={<Dashboard />} />
            <Route path="/problemlist" element={<Problems />} />
            
          </Routes>
        </Layout>
      ) : (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/comments/:id" element={<Comments />} />
            <Route path="/chat_ai" element={<Chatai />} />
            
        </Routes>
      )}
    </>
  );
};

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
