import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Dashboard from './Dashboard';
import ChatInterface from './Chat';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Dashboard />} />
        <Route path='/chat/:docId' element={<ChatInterface />} />
      </Routes>
    </Router>
  );
}

export default App;
