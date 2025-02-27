'use client'

import { useEffect, useState } from 'react';
import '../taskdetails/technicianviewtask.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useParams } from 'next/navigation';
import axios from 'axios';
import { getProfile } from "@/utils/auth";
import { useRouter } from "next/navigation";



export default function TechnicianIndexPage() {
    const { id } = useParams();

    const [RepairUpdate, setRepairUpdate] = useState(null);
    const [error, setError] = useState<string | null>(null);
    const [profile, setProfile] = useState<any>(null);
    const router = useRouter();
    const [formData, setFormData] = useState({

        id: "",
        repair_request: "",
        technician: [],
        status: "",
        remarks: "",
    });

    useEffect(() => {
        async function fetchProfile() {
            try {
                const data = await getProfile();
                setProfile(data);
                if (data?.technician_id) {
                    setFormData((prevFormData) => ({
                        ...prevFormData,
                        technician: [data.technician_id],  // เซ็ตเป็น array ตาม Django
                    }));
                }


            } catch (err) {
                setError("ไม่สามารถดึงข้อมูลโปรไฟล์ได้");
                console.error("Error fetching profile:", err);
                window.location.href = '/login';
            }
        }
        fetchProfile();
    }, []);

    const logout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("student_id");
        localStorage.removeItem("technician_id");
        window.location.href = '/login';
    };

    useEffect(() => {
        if (RepairUpdate) {
            setFormData((prevData) => ({
                ...prevData,
                remarks: RepairUpdate.repair_request.description,
                id: RepairUpdate.id,
                status: RepairUpdate.status,
            }));
        }
    }, [RepairUpdate]);

    useEffect(() => {
        if (id) {
            const fetchRepairUpdate = async () => {
                try {
                    const token = localStorage.getItem("accessToken");

                    if (!token) throw new Error("No token found");
                    const response = await axios.get(`http://localhost:8080/api/repair-requests-update-get/${id}/`,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`, // ส่ง JWT Token
                            }
                        }
                    );
                    setRepairUpdate(response.data);

                } catch (error) {
                    console.error('Error fetching repair request:', error);
                }
            };

            fetchRepairUpdate();
        }
    }, [id]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!profile?.technician_id) {
            alert("ไม่พบ technician_id");
            return;
        }

        const requestData = {
            ...formData,
            technician: [profile.technician_id],
        };

        try {
            const response = await fetch("http://localhost:8080/api/technician-repair-update/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestData),
            });

            if (response.ok) {
                router.push("/technician-trackstatus");
            } else {
                const errorData = await response.json();
                console.error("API error:", errorData);
                alert("เกิดข้อผิดพลาด กรุณาลองใหม่");
            }
        } catch (error) {
            console.error("Network error:", error);
            alert("เกิดข้อผิดพลาด กรุณาตรวจสอบการเชื่อมต่อ");
        }
    };


    useEffect(() => {
        require('bootstrap/dist/js/bootstrap.bundle.min.js');
    }, []);
    return (
        <>
            {/* ธรรมดา */}
            <div id="nav" className="d-none d-md-block">
                <header>
                    {profile ? (
                        <div>
                            <nav className="navroom d-flex justify-content-between align-items-center">
                                <span id="roompara">Technician ID : {profile.technician_id ?? "ไม่มีข้อมูล"}</span>

                                <div>
                                    <span id="roompara">
                                        {profile.first_name} {profile.last_name}&nbsp;
                                    </span>
                                    <button type="button" className="btn btn-danger" onClick={logout}>
                                        Logout
                                    </button>
                                </div>
                            </nav>
                        </div>
                    ) : (
                        <p>Loading...</p>
                    )}
                </header>
            </div>

            {/* responsive */}
            <div id="nav" className="d-block d-md-none">
                <header>
                    {profile ? (
                        <div>
                            <nav className="navroom d-flex justify-content-between align-items-center">
                                <span className=''>Technician ID : {profile.technician_id ?? "ไม่มีข้อมูล"}</span>

                                <div>
                                    <span >
                                        {profile.first_name} {profile.last_name}&nbsp;
                                    </span>
                                    <button type="button" className="btn btn-danger btn-sm" onClick={logout}>
                                        Logout
                                    </button>
                                </div>
                            </nav>
                        </div>
                    ) : (
                        <p>Loading...</p>
                    )}
                </header>
            </div>

            {/* responsive */}
            <nav className="d-block d-md-none navbar navbar-expand-lg bg-body-tertiary">
                <div className="container-fluid">
                    <div className="navbar-nav d-flex flex-row gap-3 w-100 justify-content-center">
                        <a className="nav-link active" id='navlinksidebar3' aria-current="page" href="/technician"><div className='row'>
                            <div className='col-3'>
                                <svg width="20" height="20" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M44 12C44 9.8 42.2 8 40 8H8C5.8 8 4 9.8 4 12M44 12V36C44 38.2 42.2 40 40 40H8C5.8 40 4 38.2 4 36V12M44 12L24 26L4 12" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </div>
                            <div className='col-9' >
                                <center id='sidebarlinkmenu2'>งานที่ได้รับ</center>
                            </div>

                        </div>
                        </a>
                        <a className="nav-link active" id='navlinksidebar3' aria-current="page" href="/technician-trackstatus"><div className='row'>
                            <div className='col-3'>
                                <svg width="20" height="20" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M44 12C44 9.8 42.2 8 40 8H8C5.8 8 4 9.8 4 12M44 12V36C44 38.2 42.2 40 40 40H8C5.8 40 4 38.2 4 36V12M44 12L24 26L4 12" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </div>
                            <div className='col-9' >
                                <center id='sidebarlinkmenu2'>อัพเดทสถานะ</center>
                            </div>

                        </div>
                        </a>
                    </div>
                </div>
            </nav>

            <div id="content">

                {/* ธรรมดา */}
                <div className="d-none d-lg-flex d-flex flex-column flex-shrink-0 p-3" id="sidebarbg" >
                    <span className="badge bg-white text-dark" id="sidebartitleout">
                        <div className="sidebartitlefont">
                            <span id='seereportspan'>รายละเอียดของงาน</span>
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

                {/* ธรรมดา */}
                <div className="container d-none d-md-block" id="pagecon">
                    <nav style={{ "--bs-breadcrumb-divider": "'>'" } as React.CSSProperties} aria-label="breadcrumb" id='breadcrumb'>
                        <ol className="breadcrumb">
                            <li className="breadcrumb-item">
                                <a href="/technician" id='breadcrumb-link'>งานที่ได้รับ</a>
                            </li>
                            <li className="breadcrumb-item active" aria-current="page" id='breadcrumb-link'>
                                รายละเอียดและสถานะ
                            </li>
                        </ol>
                    </nav>
                    <div id='taskdetailarea'>
                        <form onSubmit={handleSubmit}>
                            <div id='formshow'>
                                <div>
                                    <p id='remarkletter'>หมายเหตุ :</p>
                                </div>
                                <div>
                                    <input
                                        type="text"
                                        name="remarks"
                                        className="form-control"
                                        value={formData.remarks}
                                        onChange={handleChange}
                                        id='remarks-show'
                                        readOnly
                                        required>
                                    </input>
                                </div>
                            </div>
                            <div id='formshow'>
                                <div>
                                    <p id='remarkletter'>สถานะ :</p>
                                </div>
                                <div>

                                    <select
                                        name="status"
                                        className="form-select"
                                        value={formData.status}
                                        onChange={handleChange}
                                        id='selected-fonts'
                                    >

                                        <option value="assigned" >Assigned</option>
                                        <option value="in_progress" >In Progress</option>
                                        <option value="completed" >Completed</option>
                                    </select>
                                </div>
                            </div>
                            <div id='formbuttonsubmittask'>
                                <center>
                                    <button type="button" className="btn btn-warning" id='buttonforsubmittask' data-bs-toggle="modal" data-bs-target="#exampleModal">
                                        อัพเดต
                                    </button>
                                    <div className="modal fade" id="exampleModal" tabIndex={-1} aria-labelledby="exampleModalLabel" aria-hidden="true">
                                        <div className="modal-dialog">
                                            <div className="modal-content">
                                                <div className="modal-header">
                                                    <h1 className="modal-title fs-5" id="exampleModalLabel">คุณแน่ใจที่จะอัพเดตนี้แล้ว ใช่หรือไม่</h1>
                                                    <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                </div>
                                                <div id='footermodal'>
                                                    <div className='row'>
                                                        <div className='col'>
                                                            <button type="submit" className="btn btn-success" id='modalbuttonletter' data-bs-dismiss="modal">อัพเดต</button>
                                                        </div>
                                                        <div className='col'>
                                                            <button type="button" className="btn btn-danger" data-bs-dismiss="modal" id='modalbuttonletter'>ยกเลิก</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </center>
                            </div>
                        </form>
                    </div>
                </div>

                {/* Responsive */}
                <div className="container d-block d-md-none" id="pagecon">
                    <nav style={{ "--bs-breadcrumb-divider": "'>'" } as React.CSSProperties} aria-label="breadcrumb" id='breadcrumb'>
                        <ol className="breadcrumb ">
                            <li className="breadcrumb-item ">
                                <a href="/technician" id='breadcrumb-link' className="fs-6">งานที่ได้รับ</a>
                            </li>
                            <li className="breadcrumb-item active fs-6" aria-current="page" id='breadcrumb-link'>
                                รายละเอียดและสถานะ
                            </li>
                        </ol>
                    </nav>
                    <div id='taskdetailarea'>
                        <form onSubmit={handleSubmit}>
                            <div id='formshow'>
                                <div>
                                    <p id='remarkletter' className='fs-6'>หมายเหตุ :</p>
                                </div>
                                <div>
                                    <input
                                        type="text"
                                        name="remarks"
                                        className="form-control fs-6"
                                        value={formData.remarks}
                                        onChange={handleChange}
                                        id='remarks-show'
                                        readOnly
                                        required>
                                    </input>
                                </div>
                            </div>
                            <div id='formshow'>
                                <div>
                                    <p id='remarkletter' className='fs-6'>สถานะ :</p>
                                </div>
                                <div>
                                    <select
                                        name="status"
                                        className="form-select"
                                        value={formData.status}
                                        onChange={handleChange}
                                        id='selected-fonts'
                                    >
                                        <option value="assigned">Assigned</option>
                                        <option value="in_progress">In Progress</option>
                                        <option value="completed">Completed</option>
                                    </select>
                                </div>
                            </div>
                            <div id='formbuttonsubmittask'>
                                <center>
                                    <button type="button" className="btn btn-warning fs-6" id='buttonforsubmittask' data-bs-toggle="modal" data-bs-target="#exampleModal">
                                        อัพเดต
                                    </button>
                                    <div className="modal fade" id="exampleModal" tabIndex={-1} aria-labelledby="exampleModalLabel" aria-hidden="true">
                                        <div className="modal-dialog">
                                            <div className="modal-content">
                                                <div className="modal-header">
                                                    <h1 className="modal-title fs-5" id="exampleModalLabel">คุณแน่ใจที่จะอัพเดตนี้แล้ว ใช่หรือไม่</h1>
                                                    <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                </div>
                                                <div id='footermodal'>
                                                    <div className='row'>
                                                        <div className='col'>
                                                            <button type="submit" className="btn btn-success" id='modalbuttonletter' data-bs-dismiss="modal">อัพเดต</button>
                                                        </div>
                                                        <div className='col'>
                                                            <button type="button" className="btn btn-danger" data-bs-dismiss="modal" id='modalbuttonletter'>ยกเลิก</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </center>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </>
    );
}