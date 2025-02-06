// app/nontakorn/page.tsx
'use client'

import { useEffect } from 'react';
import '../taskdetails/technicianviewtask.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from "react";

export default function TechnicianIndexPage() {

    //สร้างตัวแปรมาเก็บค่า และตั้งค่าเริ่มต้น
    const [formData, setFormData] = useState({
        // student: 1,
        // description: "",
        // urgency: "",
        // repair_appointment_time: "",

        //ข้อมูลแบบ many to many ต้องใส่เป็น list
        repair_request:12,
        technician:[5],
        status:"assigned",
        // update_time:"",
        remarks:"",

        // repair_request: 12,
        // technician: 5,
        // // assigned_at = models.DateTimeField(auto_now_add=True) 
        // status: "Assigned",
    });

    // ใช้กับ <input> และ <select> ดึงค่า name และ value จากช่องที่ผู้ใช้กรอก อัปเดต formData ให้มีค่าตามที่ผู้ใช้พิมพ์
    // ดึงค่าและ อัพเดทค่า
    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    //ฟังก์ชัน handleSubmit สำหรับส่งข้อมูลไปที่ Django API
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
    
        console.log(formData);  // ตรวจสอบข้อมูลที่ส่งไปให้แน่ใจว่าถูกต้อง
    
        const response = await fetch("http://localhost:8080/api/technician-requests/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData),
        });
    
        if (response.ok) {
            alert("ส่งคำร้องขอซ่อมแล้ว!");
        } else {
            const errorData = await response.json();
            console.error("API error:", errorData);
            alert("เกิดข้อผิดพลาด กรุณาลองใหม่");
        }
    };

    useEffect(() => {
        require('bootstrap/dist/js/bootstrap.bundle.min.js'); //required อันที่ต้องใช้ bundle + Popper.js มาให้แล้ว เพื่อให้ฝั่ง client ใช้ได้ (ปล. อันทำเพื่อให้ใช้ modal ได้)
    }, []);
    return (
        <>
            <div id="nav">
                <header>
                    <nav>
                        <span id='roompara'>Room:</span>
                    </nav>
                </header>
            </div>
            <div id="content">
                <div className="d-flex flex-column flex-shrink-0 p-3" id="sidebarbg" >
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
                <div className="container" id="pagecon">
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
                                        required>
                                    </input>
                                </div>
                            </div>
                            <div id='formshow'>
                                <div>
                                    <p id='remarkletter'>สถานะ :</p>
                                </div>
                                <div>
                                    <input
                                        readOnly
                                        type="text"
                                        name="status"
                                        className="form-control"
                                        value={formData.status}
                                        onChange={handleChange}
                                        required>
                                    </input>
                                </div>
                            </div>
                            <div id='formbuttonsubmittask'>
                                <center>
                                    <button type="button" className="btn btn-warning" id='buttonforsubmittask' data-bs-toggle="modal" data-bs-target="#exampleModal">
                                        รับงาน
                                    </button>
                                    <div className="modal fade" id="exampleModal" tabIndex={-1} aria-labelledby="exampleModalLabel" aria-hidden="true">
                                        <div className="modal-dialog">
                                            <div className="modal-content">
                                                <div className="modal-header">
                                                    <h1 className="modal-title fs-5" id="exampleModalLabel">คุณแน่ใจที่จะรับงานนี้จริงๆ ใช่หรือไม่</h1>
                                                    <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                </div>
                                                <div id='footermodal'>
                                                    <div className='row'>
                                                        <div className='col'>
                                                            <button type="submit" className="btn btn-success" id='modalbuttonletter'>รับงาน</button>
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