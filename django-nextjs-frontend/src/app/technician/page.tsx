// app/nontakorn/page.tsx
'use client'

import '../technician/technicianindex.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import { useEffect, useState } from 'react';
import { getProfile } from "@/utils/auth";
import axios from 'axios';

export default function TechnicianIndexPage() {
    const [RepairAssignmentView, setRepairRepairAssignment] = useState([]);
    const [profile, setProfile] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    const fetchRepairAssignment = async (technician_id: string) => {
        try {
            const token = localStorage.getItem("accessToken");
            console.log("Token ที่ใช้:", token); // ตรวจสอบ token

            if (!token) throw new Error("No token found");

            const response = await axios.get(
                `http://localhost:8080/api/requests-asignment-views/?technician_id=${technician_id}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`, // ส่ง JWT Token
                    }
                }
            );
            // กำหนดว่าต้องเป็น Reported เท่านั้น
            // const filteredData = response.data.filter((request: any) => request.status === "Reported"); // กรองเฉพาะ status = "reported"
            // setRepairRequest(filteredData);
            setRepairRepairAssignment(response.data);
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

                if (data?.technician_id) {
                    fetchRepairAssignment(data.technician_id); // เรียก API ด้วย student_id
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

    // useEffect(() => {
    //     if (profile && profile.technician_id) {
    //         const fetchRepairAssignments = async () => {
    //             try {
    //                 const response = await axios.get(`http://localhost:8080/api/repair-assignment-filter/${profile.technician_id}/`);
    //                 setRepairAssignment(response.data);  // ถ้ามีข้อมูล จะใส่ใน array
    //                 console.log("Repair Assignments:", response.data);
    //             } catch (error) {
    //                 console.error("Error fetching repair assignments:", error);
    //             }
    //         };
    //         fetchRepairAssignments();
    //     }
    // }, [profile]);

    return (
        <>
            <div id="nav">
                <header>
                    {profile ? (
                        <div>
                            <nav className='navroom'>
                                <div className='row'>
                                    <div className='col-4'>
                                        <span id='roompara'>Technician ID : {profile.technician_id ?? "ไม่มีข้อมูล"}</span>
                                    </div>
                                    <div className='col-4'></div>
                                    <div className='col-4'>
                                        <span id='roompara'>{profile.first_name}  {profile.last_name}&nbsp;</span>
                                        <button type="button" className="btn btn-danger" onClick={logout}>Logout</button>
                                    </div>
                                </div>
                            </nav>
                        </div>
                    ) : (
                        <div>
                            <nav className='navroom'>
                                <div className='row'>
                                    <div className='col-4'>
                                        <span id='roompara'>Technician ID : No Data</span>
                                    </div>
                                    <div className='col-4'></div>
                                    <div className='col-4'>
                                        <span id='roompara'>No Data</span>
                                        <button type="button" className="btn btn-danger" onClick={logout}>Logout</button>
                                    </div>
                                </div>
                            </nav>
                        </div>
                    )}
                </header>
            </div>
            <div id="content">
                <div className="d-flex flex-column flex-shrink-0 p-3" id="sidebarbg" >
                    <span className="badge bg-white text-dark" id="sidebartitleout">
                        <div className="sidebartitlefont">
                            <span id='seereportspan'>งานที่ได้รับ</span>
                        </div>
                    </span>
                    <ul className="nav nav-pills flex-column mb-auto" id="sidebarselected">
                        <li id='linavlink'>
                            <a href="/technician" className="nav-link link-dark" id='navlinksidebar'>
                                <div className='row'>
                                    <div className='col-2'>
                                        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M29.4 12.6C29.0336 12.9739 28.8283 13.4765 28.8283 14C28.8283 14.5235 29.0336 15.0262 29.4 15.4L32.6 18.6C32.9739 18.9665 33.4765 19.1717 34 19.1717C34.5235 19.1717 35.0262 18.9665 35.4 18.6L42.94 11.06C43.9457 13.2824 44.2502 15.7585 43.8129 18.1583C43.3757 20.5581 42.2174 22.7677 40.4926 24.4926C38.7677 26.2174 36.5581 27.3757 34.1583 27.8129C31.7585 28.2502 29.2824 27.9457 27.06 26.94L13.24 40.76C12.4444 41.5557 11.3652 42.0027 10.24 42.0027C9.1148 42.0027 8.03567 41.5557 7.24002 40.76C6.44437 39.9644 5.99738 38.8852 5.99738 37.76C5.99738 36.6348 6.44437 35.5557 7.24002 34.76L21.06 20.94C20.0543 18.7176 19.7498 16.2416 20.1871 13.8417C20.6244 11.4419 21.7826 9.23233 23.5075 7.50746C25.2323 5.7826 27.4419 4.62436 29.8417 4.18711C32.2415 3.74985 34.7176 4.05435 36.94 5.06002L29.4 12.6Z" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                        </svg>
                                    </div>
                                    <div className='col-10' >
                                        <center id='sidebarlinkmenu'>งานที่ได้รับ</center>
                                    </div>
                                </div>
                            </a>
                        </li>
                    </ul>
                </div>
                <div className="container" id="pagecon">
                    <div className='taskarea'>
                        <center>
                            {RepairAssignmentView.map((RepairAssignmentView) => (
                                <div className='card' id='cardtask' key={RepairAssignmentView.repair_request.id}>
                                    <div className='row'>
                                        <div className='col-6' id='technicianreport'>
                                            <div className='row'>
                                                <div>
                                                    <div className='row' id='taskrowinfo'>
                                                        <div className='col-2'>
                                                            <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                                <path d="M18 44V24H30V44M6 18L24 4L42 18V40C42 41.0609 41.5786 42.0783 40.8284 42.8284C40.0783 43.5786 39.0609 44 38 44H10C8.93913 44 7.92172 43.5786 7.17157 42.8284C6.42143 42.0783 6 41.0609 6 40V18Z" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                                            </svg>
                                                        </div>
                                                        <div className='col-10'>
                                                            <p id='roompara' key={RepairAssignmentView.repair_request.student.room_id.room_number}>{RepairAssignmentView.repair_request.student.room_id.room_number}</p>
                                                        </div>
                                                    </div>
                                                    <div className='row' id='taskrowinfo'>
                                                        <div className='col-2'>
                                                            <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                                <path d="M24 4L38 42L24 34L10 42L24 4Z" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                                            </svg>
                                                        </div>
                                                        <div className='col-10'>
                                                            <p id='floorpara' key={RepairAssignmentView.repair_request.student.room_id.floor}>ชั้น {RepairAssignmentView.repair_request.student.room_id.floor}</p>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div className='col-3' id='linktodetails'>
                                            <a href={`technician/${RepairAssignmentView.repair_request.id}/taskdetails`}>
                                                <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                    <path d="M24 32V24M24 16H24.02M44 24C44 35.0457 35.0457 44 24 44C12.9543 44 4 35.0457 4 24C4 12.9543 12.9543 4 24 4C35.0457 4 44 12.9543 44 24Z" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                                </svg>
                                            </a>
                                        </div>
                                        <div className='col-3' id='clickfordetailsarea'>
                                            <button type="button" className="btn btn-success w-100 h-100" data-bs-toggle="modal" data-bs-target="#exampleModal" id='clickforaccepttaskmodalbutton'>
                                                รับงาน
                                            </button>
                                            <div className="modal fade" id="exampleModal" tabIndex={-1} aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div className="modal-dialog">
                                                    <div className="modal-content">
                                                        <div className="modal-header">
                                                            <h1 className="modal-title fs-5" id="modaltitletter">คุณแน่ใจที่จะรับงานนี้หรือไม่?</h1>
                                                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                        </div>
                                                        <div className="modal-footer" id='modalfooterbutton'>
                                                            <center>
                                                                <button type="button" className="btn btn-success w-100" id='buttoninmodalletter'>รับงาน</button>
                                                            </center>
                                                        </div>
                                                    </div>
                                                </div>
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