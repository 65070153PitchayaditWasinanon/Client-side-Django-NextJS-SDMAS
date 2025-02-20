// app/nontakorn/page.tsx
'use client'
import './studentindex.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { getProfile } from "@/utils/auth";
import { useState, useEffect } from "react";
import axios from 'axios';

export default function StudentIndexPage() {
    const [RepairRequestView, setRepairRequest] = useState([]);
    const [profile, setProfile] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    const fetchRepairRequest = async (student_id: string) => {
        try {
            const token = localStorage.getItem("accessToken");
            console.log("Token ที่ใช้:", token); // ตรวจสอบ token

            if (!token) throw new Error("No token found");

            const response = await axios.get(
                `http://localhost:8080/api/repair-requests-views/?student_id=${student_id}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`, // ส่ง JWT Token
                    }
                }
            );
            // กำหนดว่าต้องเป็น Reported เท่านั้น
            const filteredData = response.data.filter((request: any) => request.status === "Reported"); // กรองเฉพาะ status = "reported"
            setRepairRequest(filteredData);
        } catch (err) {
            console.error("Error fetching repair requests:", err);
        }
    };

    useEffect(() => {
        // 
        async function fetchProfile() {
            try {
                // getProfile ดึงข้อมูลมาจาก django ใส่ data
                const data = await getProfile();
                //Profile ถูก set จาก setProfile ด้วยข้อมูล data ที่ได้มาจาก getProfile 
                setProfile(data);

                if (data?.student_id) {
                    fetchRepairRequest(data.student_id); // เรียก API ด้วย student_id
                }

            } catch (err) {
                setError("ไม่สามารถดึงข้อมูลโปรไฟล์ได้");
                window.location.href = '/login';
            }
        }
        fetchProfile();
    }, []);
    const logout = () => {
        // ลบ JWT จาก localStorage
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("student_id");
        localStorage.removeItem("technician_id");

        // Redirect ไปยังหน้า login
        window.location.href = '/login';  // หรือหน้าอื่นๆ ตามต้องการ
    };

    const handleDelete = async (repairRequestId: number) => {
        try {
            const token = localStorage.getItem("accessToken");
            if (!token) throw new Error("No token found");

            const response = await axios.delete(
                `http://localhost:8080/api/repair-requests-views/${repairRequestId}/`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            if (response.status === 204) {
                alert("ลบข้อมูลสำเร็จ!");
                setRepairRequest((prev) => prev.filter((item) => item.id !== repairRequestId));
            }
        } catch (err) {
            console.error("Error deleting repair request:", err);
        }
    };

    return (
        <>
            <div id="nav">
                <header>
                    {profile ? (
                        <div>
                            <nav className='navroom'>
                                <span id='roompara'>Room:{profile.room}</span>

                                <div>
                                    <span id='roompara'>{profile.first_name}  {profile.last_name}&nbsp;</span>
                                    <button type="button" className="btn btn-danger" onClick={logout}>Logout</button>
                                </div>
                            </nav>
                        </div>
                    ) : (
                        <p>Loading...</p>
                    )}
                </header>
            </div>
            <div id="content">
                <div className="d-flex flex-column flex-shrink-0 p-3" id="sidebarbg" >
                    <span className="badge bg-white text-dark" id="sidebartitleout">
                        <div className="sidebartitlefont">
                            <span id='seereportspan'>ปัญหาที่ส่ง</span>
                        </div>
                    </span>
                    <ul className="nav nav-pills flex-column mb-auto" id="sidebarselected">
                        <li id='linavlink'>
                            <a href="/student" className="nav-link link-dark" id='navlinksidebar'>
                                <div className='row'>
                                    <div className='col-2'>
                                        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M44 12C44 9.8 42.2 8 40 8H8C5.8 8 4 9.8 4 12M44 12V36C44 38.2 42.2 40 40 40H8C5.8 40 4 38.2 4 36V12M44 12L24 26L4 12" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                        </svg>
                                    </div>
                                    <div className='col-10' >
                                        <center id='sidebarlinkmenu'>ปัญหาที่ส่ง</center>
                                    </div>
                                </div>
                            </a>
                        </li>
                        <li id='linavlink'>
                            <a href="/student/report" className="nav-link link-dark" id='navlinksidebar'>
                                <div className='row'>
                                    <div className='col-2'>
                                        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M25 19.125V27.625M25 36.125H25.0208M21.4375 8.20249L3.79165 38.25C3.42783 38.8926 3.23533 39.6213 3.23329 40.3633C3.23126 41.1054 3.41975 41.8351 3.78004 42.4799C4.14032 43.1246 4.65983 43.6618 5.28687 44.0382C5.91392 44.4145 6.62665 44.6168 7.35415 44.625H42.6458C43.3733 44.6168 44.086 44.4145 44.7131 44.0382C45.3401 43.6618 45.8596 43.1246 46.2199 42.4799C46.5802 41.8351 46.7687 41.1054 46.7667 40.3633C46.7646 39.6213 46.5721 38.8926 46.2083 38.25L28.5625 8.20249C28.1911 7.57797 27.6682 7.06162 27.0441 6.70327C26.4201 6.34492 25.7161 6.15666 25 6.15666C24.2839 6.15666 23.5798 6.34492 22.9558 6.70327C22.3318 7.06162 21.8089 7.57797 21.4375 8.20249Z" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                        </svg>
                                    </div>
                                    <div className='col-10' >
                                        {/* <a href=""></a> */}

                                        <center id='sidebarlinkmenu'>รายงานปัญหา</center>
                                    </div>
                                </div>
                            </a>
                        </li>
                    </ul>
                </div>
                <div className="container" id="pagecon">
                    <div>
                        <center>
                            {RepairRequestView.map((request) => (
                                <div className="card" id='card' key={request.id}>
                                    <div className="card-body">
                                        <div className='remark-bg' id='remark-bg'>
                                            <p className="card-text" id='remark-text'>หมายเหตุ : {request.description}</p>
                                        </div>
                                        <div className='remark-status-bg' id='remark-status-bg'>
                                            <p className="card-text" id='remark-status-text'>สถานะ : {request.status}</p>
                                        </div>
                                        <div className='row' id='buttonframe'>
                                            <div className='col' key={request.id}>
                                                <a href={`student/${request.id}/taskdetails`}>
                                                    {/* <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                        <path d="M24 32V24M24 16H24.02M44 24C44 35.0457 35.0457 44 24 44C12.9543 44 4 35.0457 4 24C4 12.9543 12.9543 4 24 4C35.0457 4 44 12.9543 44 24Z" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                                    </svg> */}
                                                    <button type="button" className="btn btn-warning" id='buttonstudentviewreport'>
                                                        แก้ไข
                                                    </button>
                                                </a>

                                            </div>
                                            <div className='col'>
                                                <button type="button" className="btn btn-danger" id='buttonstudentviewreport' onClick={() => handleDelete(request.id)}>
                                                    ลบ
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </center>
                    </div>
                </div>
            </div>
        </>
    );
}