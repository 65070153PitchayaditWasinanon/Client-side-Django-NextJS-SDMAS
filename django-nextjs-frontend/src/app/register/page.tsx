// pages/register.tsx
"use client";

import '../register/register.css';
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
        room_number: '',
    });
    const [RoomView, setRoom] = useState([]);

    useEffect(() => {
        const fetchRoom = async () => {
            const response = await axios.get('http://localhost:8080/api/room/');
            setRoom(response.data);
            console.log(response.data);
        };

        fetchRoom();
    }, []);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            // ส่งข้อมูลไปยัง Django backend สำหรับการลงทะเบียน
            const response = await axios.post('http://localhost:8080/auth/api/register/', formData);
            console.log('Register success:', response.data);
            router.push('/login'); // หลังจากลงทะเบียนเสร็จให้ไปที่หน้า login
        } catch (error) {
            console.error('Register error:', error);
            alert('การลงทะเบียนล้มเหลว');
        }
    };

    return (
        <div id='content'>
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
                                <select
                                    name="room_number"
                                    className="form-select"
                                    value={formData.room_number}
                                    onChange={handleChange}
                                    id='input-text'
                                >
                                    <option value="" id='option-text-area'>-- เลือกห้อง --</option> {/* ตัวเลือกเริ่มต้น */}
                                    {RoomView.map((room) => (
                                        <option id='option-text-area' key={room.room_number} value={room.room_number}>
                                            {room.room_number}
                                        </option>
                                    ))}
                                </select>
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
