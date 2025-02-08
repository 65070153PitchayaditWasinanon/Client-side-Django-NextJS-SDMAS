"use client";
import { useState } from "react";
import axios, { AxiosError } from "axios";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
    const router = useRouter();
    const [formData, setFormData] = useState({ username: "", password: "" });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://localhost:8000/api/register/", formData);
            alert("ลงทะเบียนสำเร็จ! Student ID: " + response.data.student_id);
            router.push("/login"); // นำทางไปหน้า login
        } catch (error: unknown) {
            if (axios.isAxiosError(error)) {
                // ตรวจสอบว่า error เป็น AxiosError หรือไม่
                alert("เกิดข้อผิดพลาด: " + error.response?.data?.error || "ไม่สามารถลงทะเบียนได้");
            } else {
                alert("เกิดข้อผิดพลาดไม่ทราบสาเหตุ");
            }
        }
    };

    return (
        <div>
            <h2>ลงทะเบียน</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="username" placeholder="Username" onChange={handleChange} required />
                <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
                <button type="submit">ลงทะเบียน</button>
            </form>
        </div>
    );
}
