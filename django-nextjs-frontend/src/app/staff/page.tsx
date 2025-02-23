// app/nontakorn/page.tsx
'use client'
import '../staff/staffindex.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
// import { getProfile } from "@/utils/auth";
import { useState, useEffect } from "react";


export default function StaffIndexPage() {
    const [profile, setProfile] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    useEffect(() => {
        // 
        async function fetchProfile() {
            try {
                // getProfile ดึงข้อมูลมาจาก django ใส่ data
                const data = await getProfile();
                //Profile ถูก set จาก setProfile ด้วยข้อมูล data ที่ได้มาจาก getProfile 
                setProfile(data);

            } catch (err) {
                setError("ไม่สามารถดึงข้อมูลโปรไฟล์ได้");
            }
        }
        fetchProfile();
    }, []);

    const [RepairRequestView, setRepairRequest] = useState([]);

    useEffect(() => {
        const fetchRepairRequest = async () => {
            try {
                const token = localStorage.getItem("accessToken");
                console.log("Token ที่ใช้:", token); // ตรวจสอบ token

                if (!token) throw new Error("No token found");

                const response = await axios.get('http://localhost:8080/api/repair-requests-views-staff/',
                    {
                        headers: {
                            Authorization: `Bearer ${token}`, // ส่ง JWT Token
                        }
                    }
                );
                const sortedData = response.data.sort((a, b) => a.id - b.id);
                setRepairRequest(sortedData);
                console.log(sortedData);
            } catch (err) {
                console.error("Error fetching repair requests:", err);
            }
        };

        fetchRepairRequest();
    }, []);

    return (
        <>
            <div id="nav">
                <header>
                    {/* {profile ? (
                        <div>
                            <nav>
                                <span id='roompara'>Room:{profile.room}</span>
                            </nav>
                        </div>
                    ) : (
                        <div>
                            <nav>
                                <span id='roompara'>Room: Loading ...</span>
                            </nav>
                        </div>
                    )} */}
                    <div>
                        <nav>
                            <span id='roompara'>Staff Site</span>
                        </nav>
                    </div>
                </header>
            </div>
            <div id="content">
                <div className="d-flex flex-column flex-shrink-0 p-3" id="sidebarbg" >
                    <span className="badge bg-white text-dark" id="sidebartitleout">
                        <div className="sidebartitlefont">
                            <span id='seereportspan'>มอบหมายงาน</span>
                        </div>
                    </span>
                    <ul className="nav nav-pills flex-column mb-auto" id="sidebarselected">
                        <li id='linavlink'>
                            <a href="/staff" className="nav-link link-dark" id='navlinksidebar'>
                                <center id='sidebarlinkmenu'>มอบหมายงาน</center>
                            </a>
                        </li>
                        <li id='linavlink'>
                            <a href="/staff" className="nav-link link-dark" id='navlinksidebar'>
                                <center id='sidebarlinkmenu'>ประวัติการซ่อม</center>
                            </a>
                        </li>
                        <li id='linavlink'>
                            <a href="/staff" className="nav-link link-dark" id='navlinksidebar'>
                                <center id='sidebarlinkmenu'>จัดการช่าง</center>
                            </a>
                        </li>
                        <li id='linavlink'>
                            <a href="/staff" className="nav-link link-dark" id='navlinksidebar'>
                                <center id='sidebarlinkmenu'>จัดการนักศึกษา</center>
                            </a>
                        </li>
                    </ul>
                </div>
                <div className="container" id="pagecon">
                    <div className='row'>
                        {RepairRequestView.map((RepairRequestView) => (
                            <div className='col-6' key={RepairRequestView.id}>
                                <div className="card" id='card'>
                                    <div className="card-body">
                                        <div className='remark-bg' id='remark-bg'>
                                            <center>
                                                <p className="card-text" id='remark-text'>หมายเหตุ : {RepairRequestView.description}</p>
                                            </center>
                                        </div>
                                        <div className='remark-status-bg' id='remark-status-bg'>
                                            <center>
                                                <p className="card-text" id='remark-status-text'>สถานะ : {RepairRequestView.status.charAt(0).toUpperCase() + RepairRequestView.status.slice(1)}</p>
                                            </center>
                                        </div>
                                        <div className='row'>
                                            <div className='col-5'>
                                                <center>
                                                    <p className='card-text' id='room-number-text'>ห้อง : {RepairRequestView.student.room_id.room_number}</p>
                                                </center>
                                            </div>
                                            <div className='col-7'>
                                                <center>
                                                    <p className='card-text-small' id='urgency-level-text'>ความเร่งด่วน : {RepairRequestView.urgency.charAt(0).toUpperCase() + RepairRequestView.urgency.slice(1)}</p>
                                                </center>
                                            </div>
                                        </div>
                                        <div className='row' id='buttonframe'>
                                            <div className='col-6'>
                                                <center>
                                                    <a href={`staff/assignjob/${RepairRequestView.id}`} className="btn btn-success" id='buttonstudentviewreport'>
                                                        มอบหมายงาน
                                                    </a>
                                                </center>
                                            </div>
                                            <div className='col-6'>
                                                <center>
                                                    <button type="button" className="btn btn-warning" id='buttonstudentviewreport'>
                                                        แก้ไข
                                                    </button>
                                                </center>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
}