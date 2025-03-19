// src/components/PatientForm.js
import React, { useState } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

function PatientForm({ token }) {
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

  if (decoded.role !== 'admin') return null;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('https://emr-app-4jan.onrender.com/patients/new', formData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMessage('Patient created successfully');
      setFormData({ full_name: '', dob: '', gender: '', address: '', phone: '', email: '', cpf: '' });
    } catch (err) {
      setMessage('Error: ' + (err.response?.data?.error || 'Unknown'));
    }
  };

  return (
    <div>
      <h2>Create Patient</h2>
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
        <button type="submit">Create</button>
      </form>
      {message && (
        <p className={message.startsWith('Error') ? 'error' : ''}>{message}</p>
      )}
    </div>
  );
}

export default PatientForm;
