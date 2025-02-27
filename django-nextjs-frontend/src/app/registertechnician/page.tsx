"use client";

import '../registertechnician/registertechnician.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';


const RegisterPage = () => {
    const router = useRouter();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        firstName: '',
        lastName: '',
        technician_id: '',
        expertise: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            // ส่งข้อมูลไปยัง Django backend สำหรับการลงทะเบียน
            const response = await axios.post('http://localhost:8080/auth/api/register/technician/', formData);
            router.push('/login'); // หลังจากลงทะเบียนเสร็จให้ไปที่หน้า login
        } catch (error) {
            console.error('Register error:', error);
            alert('การลงทะเบียนล้มเหลว');
        }
    };

    return (
        <div className='content'>
            <div className='container' id='pagecon'>
                <div className='card' id='registerarea'>
                    <div id='register-title-area'>
                        <center>
                            <p id='register-title'>ลงทะเบียน</p>
                        </center>
                    </div>
                    <div>
                        <form onSubmit={handleSubmit}>
                            <div id='input-area'>
                                <input
                                    type="text"
                                    name="username"
                                    placeholder="Username"
                                    value={formData.username}
                                    onChange={handleChange}
                                    required
                                    id='input-text'
                                />
                            </div>
                            <div id='input-area'>
                                <input
                                    type="password"
                                    name="password"
                                    placeholder="Password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    required
                                    id='input-text'
                                />
                            </div>
                            <div id='input-area'>
                                <input
                                    type="text"
                                    name="firstName"
                                    placeholder="First Name"
                                    value={formData.firstName}
                                    onChange={handleChange}
                                    required
                                    id='input-text'
                                />
                            </div>
                            <div id='input-area'>
                                <input
                                    type="text"
                                    name="lastName"
                                    placeholder="Last Name"
                                    value={formData.lastName}
                                    onChange={handleChange}
                                    required
                                    id='input-text'
                                />
                            </div>
                            <div id='input-area'>
                                <input
                                    type="text"
                                    name="technician_id"
                                    placeholder="Technician ID"
                                    value={formData.technician_id}
                                    onChange={handleChange}
                                    required
                                    id='input-text'
                                />
                            </div>
                            <div id='input-area'>
                                <input
                                    type="text"
                                    name="expertise"
                                    placeholder="Expertise"
                                    value={formData.expertise}
                                    onChange={handleChange}
                                    required
                                    id='input-text'
                                />
                            </div>
                            <div id='button-area'>
                                <button className='btn btn-success' type="submit" id='register-button'>ลงทะเบียน</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;
