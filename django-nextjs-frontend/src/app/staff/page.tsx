'use client'
import '../staff/staffindex.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import { getProfile } from "@/utils/auth";
import { useState, useEffect } from "react";


export default function StaffIndexPage() {
    const [profile, setProfile] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    useEffect(() => {
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

                if (!token) throw new Error("No token found");

                const response = await axios.get('http://localhost:8080/api/repair-requests-views-staff/',
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        }
                    }
                );
                const sortedData = response.data.sort((a, b) => a.id - b.id);
                const filteredData = sortedData.filter((request: any) => request.status === "Reported"); // กรองเฉพาะ status = "reported"
                setRepairRequest(filteredData);
            } catch (err) {
                console.error("Error fetching repair requests:", err);
            }
        };

        fetchRepairRequest();
    }, []);

    const logout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("student_id");
        localStorage.removeItem("technician_id");
        window.location.href = '/login';
    };

    return (
        <>
            <div id="nav">
                <header>
                    <div>
                        <nav>
                            <div className='row'>
                                <div className='col-6 float-start'>
                                    <span id='roompara'>Staff Site</span>
                                </div>
                                <div className='col-6'>
                                    <button type="button" className="btn btn-danger float-end" onClick={logout}>
                                        Logout
                                    </button>
                                </div>
                            </div>
                        </nav>
                    </div>
                </header>
            </div>

            {/* responsive */}
            <nav className="d-block d-md-none navbar navbar-expand-lg bg-body-tertiary">
                <div className="container-fluid">
                    <div className="row d-flex w-100 justify-content-center">
                        <div className='col-12'>
                            <a href="/staff" className="nav-link link-dark" id='response-navlinksidebar'>
                                <center id='sidebarlinkmenu'>มอบหมายงาน</center>
                            </a>
                        </div>
                    </div>
                </div>
            </nav>

            <div id="content">
                <div className="d-none d-lg-flex d-flex flex-column flex-shrink-0 p-3" id="sidebarbg" >
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
                    </ul>
                </div>

                {/* ธรรมดา */}
                <div className="container d-none d-md-block" id="pagecon">
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
                                                    <a href={`staff/edit-job/${RepairRequestView.id}`} className="btn btn-warning" id='buttonstudentviewreport'>
                                                        แก้ไข
                                                    </a>
                                                </center>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* responsive */}
                <div className="container d-block d-md-none" id="pagecon">
                    <div>
                        {RepairRequestView.map((RepairRequestView) => (
                            <div className='col-12' key={RepairRequestView.id}>
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
                                            <div className='col-12'>
                                                <center>
                                                    <p className='card-text' id='room-number-text'>ห้อง : {RepairRequestView.student.room_id.room_number}</p>
                                                </center>
                                            </div>
                                            <div className='col-12'>
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
                                                    <a href={`staff/edit-job/${RepairRequestView.id}`} className="btn btn-warning" id='buttonstudentviewreport'>
                                                        แก้ไข
                                                    </a>
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