// emr_app/emr-frontend/src/components/PatientDetails.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

function PatientDetails({ token, patientId, onBack }) {
  const [patient, setPatient] = useState(null);
  const [formData, setFormData] = useState({
    full_name: '',
    dob: '',
    gender: '',
    address: '',
    phone: '',
    email: '',
    cpf: '',
  });
  const [message, setMessage] = useState('');
  const decoded = jwtDecode(token);
  const isAdmin = decoded.role === 'admin';

  useEffect(() => {
    const fetchPatient = async () => {
      try {
        const response = await axios.get(`https://emr-app-4jan.onrender.com/patients/${patientId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setPatient(response.data);
        setFormData(response.data);
        setMessage('');
      } catch (err) {
        setMessage('Error: ' + (err.response?.data?.error || 'Failed to fetch patient'));
      }
    };
    fetchPatient();
  }, [patientId, token]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.put(`https://emr-app-4jan.onrender.com/patients/${patientId}`, formData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setPatient(response.data.patient);
      setMessage('Patient updated successfully');
    } catch (err) {
      setMessage('Error: ' + (err.response?.data?.error || 'Failed to update patient'));
    }
  };

  if (!patient) return <div>Loading...</div>;

  return (
    <div>
      <h2>Patient Details</h2>
      <button onClick={onBack}>Back to List</button>
      <p>Full Name: {patient.full_name}</p>
      <p>Date of Birth: {patient.dob}</p>
      <p>Gender: {patient.gender}</p>
      <p>Address: {patient.address}</p>
      <p>Phone: {patient.phone}</p>
      <p>Email: {patient.email}</p>
      <p>CPF: {patient.cpf}</p>

      {isAdmin && (
        <div>
          <h3>Edit Patient</h3>
          <form onSubmit={handleSubmit}>
            <div>
              <label>Full Name: </label>
              <input name="full_name" value={formData.full_name} onChange={handleChange} required />
            </div>
            <div>
              <label>Date of Birth (YYYY-MM-DD): </label>
              <input name="dob" value={formData.dob} onChange={handleChange} required />
            </div>
            <div>
              <label>Gender (M/F): </label>
              <input name="gender" value={formData.gender} onChange={handleChange} required />
            </div>
            <div>
              <label>Address: </label>
              <input name="address" value={formData.address} onChange={handleChange} required />
            </div>
            <div>
              <label>Phone: </label>
              <input name="phone" value={formData.phone} onChange={handleChange} required />
            </div>
            <div>
              <label>Email: </label>
              <input name="email" value={formData.email} onChange={handleChange} required />
            </div>
            <div>
              <label>CPF: </label>
              <input name="cpf" value={formData.cpf} onChange={handleChange} required />
            </div>
            <button type="submit">Update</button>
          </form>
          {message && <p className={message.startsWith('Error') ? 'error' : ''}>{message}</p>}
        </div>
      )}
    </div>
  );
}

export default PatientDetails;
