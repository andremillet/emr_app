// emr_app/emr-frontend/src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import PatientList from './components/PatientList';
import PatientForm from './components/PatientForm';
import PatientDetails from './components/PatientDetails';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [selectedPatientId, setSelectedPatientId] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('https://emr-app-4jan.onrender.com/login', {
        username,
        password,
      });
      const newToken = response.data.access_token;
      setToken(newToken);
      localStorage.setItem('token', newToken);
      setError('');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('token');
    setSelectedPatientId(null);
  };

  const handlePatientClick = (patientId) => {
    setSelectedPatientId(patientId);
  };

  const handleBack = () => {
    setSelectedPatientId(null);
  };

  const decodedToken = token ? jwtDecode(token) : null;
  const userRole = decodedToken ? decodedToken.role : null;

  return (
    <div className="App">
      <h1>EMR System</h1>
      {!token ? (
        <form onSubmit={handleLogin}>
          <div>
            <label>Username: </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div>
            <label>Password: </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button type="submit">Login</button>
          {error && <p style={{ color: 'red' }}>{error}</p>}
        </form>
      ) : (
        <>
          <p>Welcome, {username} ({userRole})</p>
          <button onClick={handleLogout}>Logout</button>
          {selectedPatientId ? (
            <PatientDetails token={token} patientId={selectedPatientId} onBack={handleBack} />
          ) : (
            <>
              <PatientList token={token} onPatientClick={handlePatientClick} />
              {userRole === 'admin' && <PatientForm token={token} />}
            </>
          )}
        </>
      )}
    </div>
  );
}

export default App;
