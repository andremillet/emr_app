// src/components/PatientList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function PatientList({ token }) {
  const [patients, setPatients] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await axios.get('https://emr-app-4jan.onrender.com/patients', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setPatients(response.data.patients);
        setError('');
      } catch (err) {
        setError('Failed to fetch patients');
      }
    };
    fetchPatients();
    // Optional: Poll every 5 seconds (remove if real-time not needed)
    const interval = setInterval(fetchPatients, 5000);
    return () => clearInterval(interval); // Cleanup
  }, [token]);

  return (
    <div>
      <h2>Patients</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {patients.map((patient) => (
          <li key={patient.patient_id}>
            {patient.full_name} - CPF: {patient.cpf}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PatientList;
