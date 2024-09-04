import React from "react";
import './App.css';
import Login from "./components/login";
import Register from "./components/register";
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom'; 
import Home from "./components/home";
import Layout from "./components/layout";
import Forgotpass from "./components/forgotpass";
import Forum from "./components/forum";
import Comments from "./components/comments";

const AppContent = () => {
  const location = useLocation();
  const isAuthPage = location.pathname === '/login' || location.pathname === '/register' || location.pathname === '/forgotpass' || location.pathname === '/forum'  ;
  return (
    <>
      {isAuthPage ? (
        <Layout>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgotpass" element={<Forgotpass />} />
            <Route path="/forum" element={<Forum />} />
            
          </Routes>
        </Layout>
      ) : (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/comments/:id" element={<Comments />} />
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
