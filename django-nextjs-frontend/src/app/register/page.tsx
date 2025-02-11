// pages/register.tsx
"use client";
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


    // useEffect(() => {
    //     // Check if the router is ready
    //     if (!router.isReady) return;
    // }, [router]);

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
        <div>
            <h2>ลงทะเบียน</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                />
                <input
                    type="text"
                    name="firstName"
                    placeholder="First Name"
                    value={formData.firstName}
                    onChange={handleChange}
                    required
                />
                <input
                    type="text"
                    name="lastName"
                    placeholder="Last Name"
                    value={formData.lastName}
                    onChange={handleChange}
                    required
                />
                <select
                    name="room_number"
                    className="form-select"
                    value={formData.room_number}
                    onChange={handleChange}
                >
                    <option value="">-- เลือกห้อง --</option> {/* ตัวเลือกเริ่มต้น */}
                    {RoomView.map((room) => (
                        <option key={room.room_number} value={room.room_number}>
                            {room.room_number}
                        </option>
                    ))}
                </select>
                {/* // <input
                //     type="text"
                //     name="room_number"
                //     placeholder="room_number"
                //     value={formData.room_number.RoomView.room_number}
                //     onChange={handleChange}
                //     required
                // /> */}
                
                <button type="submit">ลงทะเบียน</button>
            </form>
        </div>
    );
};

export default RegisterPage;
