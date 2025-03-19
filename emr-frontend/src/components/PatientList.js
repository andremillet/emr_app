// emr_app/emr-frontend/src/components/PatientList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function PatientList({ token, onPatientClick }) {
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
    const interval = setInterval(fetchPatients, 5000);
    return () => clearInterval(interval);
  }, [token]);

  return (
    <div>
      <h2>Patients</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {patients.map((patient) => (
          <li key={patient.patient_id} onClick={() => onPatientClick(patient.patient_id)} style={{ cursor: 'pointer' }}>
            {patient.full_name} - CPF: {patient.cpf}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PatientList;
