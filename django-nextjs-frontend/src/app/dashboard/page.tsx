"use client";
import { useEffect, useState } from "react";
import { getProfile, getAccessToken } from "@/utils/auth"; // Import ฟังก์ชัน getProfile

// const logout = () => {
//     // ลบ JWT จาก localStorage
//     localStorage.removeItem('access_token');
//     localStorage.removeItem('refresh_token');

//     // Redirect ไปยังหน้า login
//     window.location.href = '/login';  // หรือหน้าอื่นๆ ตามต้องการ
// };

export default function DashboardPage() {
    const [profile, setProfile] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchProfile() {
            const token = getAccessToken();
            try {
                const data = await getProfile();
                setProfile(data);
            } catch (err) {
                setError("ไม่สามารถดึงข้อมูลโปรไฟล์ได้");
                // window.location.href = '/login'; 
            }
        }
        fetchProfile();
    }, []);

    if (error) return <p>{error}</p>;

    const logout = () => {
        // ลบ JWT จาก localStorage
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("student_id");
        localStorage.removeItem("technician_id");

        // Redirect ไปยังหน้า login
        window.location.href = '/login';  // หรือหน้าอื่นๆ ตามต้องการ
    };

    return (
        <div>
            <h2>Dashboard</h2>
            {profile ? (
                <div>
                    <p>Welcome, {profile.username}!</p>
                    <p>Welcome, {profile.student_id}!</p>
                    <p>Welcome, {profile.room}!</p>
                    <button onClick={logout}>Logout</button> {/* ปุ่ม logout */}
                </div>

            ) : (
                <p>Loading...</p>
            )}


        </div>
    );
}
