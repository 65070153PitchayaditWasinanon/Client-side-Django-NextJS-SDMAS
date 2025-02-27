'use client'
import './studentreport.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { getProfile } from "@/utils/auth"; // Import ฟังก์ชัน getProfile

export default function StudentReportPage() {

    //สร้างตัวแปล Profile เก็บ ข้อมูล user setProfile คือตัวใส่ค่าเก็นใน profile
    const [profile, setProfile] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();
    //สร้างตัวแปรมาเก็บค่า และตั้งค่าเริ่มต้น
    const [formData, setFormData] = useState({
        student: 0,
        description: "",
        urgency: "",
        repair_appointment_time: "",
    });

    // useEffect คือ การกระทำที่เกิดขึ้นนอกเหนือจากการแสดงผลของ UI เช่น การดึงข้อมูลจาก API, การสมัคร listener สำหรับ events, การตั้งค่าหรือปรับปรุงค่าของ state ที่อาจมีผลต่อการ render ของคอมโพเนนต์
    useEffect(() => {
        async function fetchProfile() {
            try {
                // getProfile ดึงข้อมูลมาจาก django ใส่ data
                const data = await getProfile();
                //Profile ถูก set จาก setProfile ด้วยข้อมูล data ที่ได้มาจาก getProfile 
                setProfile(data);
                setFormData((prevFormData) => ({
                    ...prevFormData,
                    student: data.student_id || "",  // ตั้งค่า student_id เมื่อข้อมูลโปรไฟล์โหลดแล้ว
                }));
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

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    //ฟังก์ชัน handleSubmit สำหรับส่งข้อมูลไปที่ Django API
    const handleSubmit = async (e: React.FormEvent) => {
        // ป้องกันหน้าเว็บโหลดซ้ำ
        e.preventDefault();


        const response = await fetch("http://localhost:8080/api/repair-requests/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData),
        });
        if (response.ok) {
            alert("ส่งคำร้องขอซ่อมแล้ว!");
            router.push("/student");
        } else {
            alert("เกิดข้อผิดพลาด กรุณาลองใหม่");

        }
    };

    return (
        <>
            {/* ธรรมดา */}
            <div id="nav" className="d-none d-md-block">
                <header>
                    {profile ? (
                        <div>
                            <nav className="navroom">
                                <span id="roompara">Room: {profile.room}</span>

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
                        <div>
                            <nav className='navroom'>
                                <div className='row'>
                                    <div className='col-4'>
                                        <span id='roompara'>Room: Loading</span>
                                    </div>
                                    <div className='col-4'></div>
                                    <div className='col-4'>
                                        <span id='roompara'>Loading... &nbsp;</span>
                                        <button type="button" className="btn btn-danger" onClick={logout}>Logout</button>
                                    </div>
                                </div>
                            </nav>
                        </div>
                    )}
                </header>
            </div>

            {/* responsive */}
            <div id="nav" className="d-block d-md-none">
                <header>
                    {profile ? (
                        <div>
                            <nav className="navroom">
                                <span className=''>Room: {profile.room}</span>

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
                        <motion.a className="nav-link active" id='navlinksidebar3' aria-current="page" href="/student" whileTap={{ scale: 0.9 }} whileHover={{ backgroundColor: "rgba(0, 0, 0, 0.1)", borderRadius: "10px" }}><div className='row'>
                            <div className='col-3'>
                                <svg width="20" height="20" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M44 12C44 9.8 42.2 8 40 8H8C5.8 8 4 9.8 4 12M44 12V36C44 38.2 42.2 40 40 40H8C5.8 40 4 38.2 4 36V12M44 12L24 26L4 12" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </div>
                            <div className='col-9' >
                                <center id='sidebarlinkmenu2'>ปัญหาที่ส่ง</center>
                            </div>
                        </div>
                        </motion.a>
                        <motion.a className="nav-link active" id='navlinksidebar2' aria-current="page" href="/student/report" whileTap={{ scale: 0.9 }} whileHover={{ backgroundColor: "rgba(0, 0, 0, 0.1)", borderRadius: "10px" }}><div className='row'>
                            <div className='col-3'>
                                <svg width="20" height="20" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M25 19.125V27.625M25 36.125H25.0208M21.4375 8.20249L3.79165 38.25C3.42783 38.8926 3.23533 39.6213 3.23329 40.3633C3.23126 41.1054 3.41975 41.8351 3.78004 42.4799C4.14032 43.1246 4.65983 43.6618 5.28687 44.0382C5.91392 44.4145 6.62665 44.6168 7.35415 44.625H42.6458C43.3733 44.6168 44.086 44.4145 44.7131 44.0382C45.3401 43.6618 45.8596 43.1246 46.2199 42.4799C46.5802 41.8351 46.7687 41.1054 46.7667 40.3633C46.7646 39.6213 46.5721 38.8926 46.2083 38.25L28.5625 8.20249C28.1911 7.57797 27.6682 7.06162 27.0441 6.70327C26.4201 6.34492 25.7161 6.15666 25 6.15666C24.2839 6.15666 23.5798 6.34492 22.9558 6.70327C22.3318 7.06162 21.8089 7.57797 21.4375 8.20249Z" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </div>
                            <div className='col-9' >
                                <center id='sidebarlinkmenu2'>รายงานปัญหา</center>
                            </div>
                        </div></motion.a>
                        <motion.a className="nav-link active" id='navlinksidebar3' aria-current="page" href="/student-trackstatus" whileTap={{ scale: 0.9 }} whileHover={{ backgroundColor: "rgba(0, 0, 0, 0.1)", borderRadius: "10px" }}><div className='row'>
                            <div className='col-3'>
                                <svg width="20" height="20" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M25 19.125V27.625M25 36.125H25.0208M21.4375 8.20249L3.79165 38.25C3.42783 38.8926 3.23533 39.6213 3.23329 40.3633C3.23126 41.1054 3.41975 41.8351 3.78004 42.4799C4.14032 43.1246 4.65983 43.6618 5.28687 44.0382C5.91392 44.4145 6.62665 44.6168 7.35415 44.625H42.6458C43.3733 44.6168 44.086 44.4145 44.7131 44.0382C45.3401 43.6618 45.8596 43.1246 46.2199 42.4799C46.5802 41.8351 46.7687 41.1054 46.7667 40.3633C46.7646 39.6213 46.5721 38.8926 46.2083 38.25L28.5625 8.20249C28.1911 7.57797 27.6682 7.06162 27.0441 6.70327C26.4201 6.34492 25.7161 6.15666 25 6.15666C24.2839 6.15666 23.5798 6.34492 22.9558 6.70327C22.3318 7.06162 21.8089 7.57797 21.4375 8.20249Z" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </div>
                            <div className='col-9' >
                                <center id='sidebarlinkmenu2'>ติดตามสถานะ</center>
                            </div>
                        </div></motion.a>
                    </div>
                </div>
            </nav>

            <div id="content">

                {/* ธรรมดา */}
                <div className="d-none d-lg-flex d-flex flex-column flex-shrink-0 p-3" id="sidebarbg" >
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
                                        <center id='sidebarlinkmenu'>รายงานปัญหา</center>
                                    </div>
                                </div>
                            </a>
                        </li>
                        <li id='linavlink'>
                            <a href="/student-trackstatus" className="nav-link link-dark" id='navlinksidebar'>
                                <div className='row'>
                                    <div className='col-2'>
                                        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M25 19.125V27.625M25 36.125H25.0208M21.4375 8.20249L3.79165 38.25C3.42783 38.8926 3.23533 39.6213 3.23329 40.3633C3.23126 41.1054 3.41975 41.8351 3.78004 42.4799C4.14032 43.1246 4.65983 43.6618 5.28687 44.0382C5.91392 44.4145 6.62665 44.6168 7.35415 44.625H42.6458C43.3733 44.6168 44.086 44.4145 44.7131 44.0382C45.3401 43.6618 45.8596 43.1246 46.2199 42.4799C46.5802 41.8351 46.7687 41.1054 46.7667 40.3633C46.7646 39.6213 46.5721 38.8926 46.2083 38.25L28.5625 8.20249C28.1911 7.57797 27.6682 7.06162 27.0441 6.70327C26.4201 6.34492 25.7161 6.15666 25 6.15666C24.2839 6.15666 23.5798 6.34492 22.9558 6.70327C22.3318 7.06162 21.8089 7.57797 21.4375 8.20249Z" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                        </svg>
                                    </div>
                                    <div className='col-10' >
                                        <center id='sidebarlinkmenu'>ติดตามสถานะ</center>
                                    </div>
                                </div>
                            </a>
                        </li>
                    </ul>
                </div>


                <div className="container" id="pagecon">
                    <div className="emp-form-box">
                        <form onSubmit={handleSubmit} className="p-3 border rounded">
                            <div className="form-group mb-3">
                                <label htmlFor="description" id="student1label">
                                    อธิบายสาเหตุ :
                                </label>
                                <div className="student1textarea">
                                    <input
                                        type="text"
                                        name="description"
                                        className="form-control"
                                        value={formData.description} 
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                            </div>

                            <div className="form-group mb-3">
                                <label htmlFor="urgency" id="student1label">
                                    ความเร่งด่วน
                                </label>
                                <div id='student1urgencyselect'>
                                    <select
                                        name="urgency"
                                        className="form-select"
                                        value={formData.urgency}
                                        onChange={handleChange}
                                    >
                                        <option value="" id='optionletter'>กรุณาเลือก</option>
                                        <option value="low" id='optionletter'>น้อย</option>
                                        <option value="medium" id='optionletter'>ปานกลาง</option>
                                        <option value="high" id='optionletter'>สูง</option>
                                    </select>
                                </div>
                            </div>

                            <div className="form-group mb-3">
                                <label htmlFor="repairAppointmentTime" id="student1label">
                                    วันเวลาที่นัดหมาย
                                </label>
                                <div className="d-flex justify-content-around" id="repair_appointment_time_show">
                                    <input
                                        type="datetime-local"
                                        name="repair_appointment_time"
                                        className="form-control"
                                        value={formData.repair_appointment_time}
                                        onChange={handleChange}
                                        required
                                    />
                                </div>
                            </div>

                            <div className="row mt-4">
                                <div className="col">
                                    <center>
                                        <button type="submit" className="btn btn-success" id="student1button">
                                                เสร็จสิ้น
                                        </button>
                                    </center>
                                </div>
                                <div className="col">
                                    <center>
                                        <button type="button" className="btn btn-danger" id="student1button">
                                            <a href="/" id="studentdenybutton" style={{ color: "white", textDecoration: "none" }}>
                                                ยกเลิก
                                            </a>
                                        </button>
                                    </center>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </>
    );
}