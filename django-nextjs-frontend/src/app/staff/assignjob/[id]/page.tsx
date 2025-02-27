// app/nontakorn/page.tsx
'use client'
import '../[id]/staffassignjob.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import { getProfile } from "@/utils/auth";
import { useState, useEffect } from "react";
import { useParams, useRouter } from 'next/navigation';


export default function StaffAssignJobPage() {
    const { id } = useParams(); //การดึง id มาจาก URL
    const router = useRouter();

    const [profile, setProfile] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    useEffect(() => {
        async function fetchProfile() {
            try {
                // getProfile ดึงข้อมูลมาจาก Django ใส่ Data
                const data = await getProfile();
                //Profile ถูก set จาก setProfile ด้วยข้อมูล Data ที่ได้มาจาก getProfile 
                setProfile(data);

            } catch (err) {
                setError("ไม่สามารถดึงข้อมูลโปรไฟล์ได้"); //ถ้า error จะขึ้นเตือน
            }
        }
        fetchProfile();
    }, []);

    const [technicians, setTechnicians] = useState<any>([]); //ของ Technician

    useEffect(() => {
        const fetchTechnicians = async () => {
            try {
                const token = localStorage.getItem("accessToken"); // Get Token มาเพื่อส่งคำขอ

                if (!token) throw new Error("No token found");
                const response = await axios.get('http://localhost:8080/api/staff/technician/'
                    , {
                        headers: {
                            Authorization: `Bearer ${token}` // ใส่ Token ด้วย
                        }
                    });
                setTechnicians(response.data); // Set ค่าในตัวแปร technicians
            } catch (error) {
                console.error("Error fetching technicians", error);
            }
        };

        fetchTechnicians();
    }, []);

    const [repairRequest, setRepairRequest] = useState(null); //ของ RepairRequest

    useEffect(() => {
        if (id) {
            const fetchRepairRequest = async () => {
                try {
                    const token = localStorage.getItem("accessToken"); // Get Token มาเพื่อส่งคำขอ

                    if (!token) throw new Error("No token found");
                    const response = await axios.get(`http://localhost:8080/api/repair-requests-staff/${id}/`
                    , {
                        headers: {
                            Authorization: `Bearer ${token}` // ใส่ Token ด้วย
                        }
                    });
                    setRepairRequest(response.data);
                } catch (error) {
                    console.error('Error fetching repair request:', error);
                }
            };

            fetchRepairRequest();
        }
    }, [id]);

    const [formData, setFormData] = useState({
        repair_request: null,
        technician: [],
        status: "assigned",
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    //ฟังก์ชัน handleSubmit สำหรับส่งข้อมูลไปที่ Django API
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const token = localStorage.getItem("accessToken");
        if (!token) {
            alert("ไม่พบ Token กรุณาเข้าสู่ระบบใหม่");
            return;
        }

        const response = await fetch("http://localhost:8080/api/staff-create-repairassignment/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": token ? `Bearer ${token}` : ""
            },
            body: JSON.stringify(formData),
        });

        if (response.ok) {
            // alert("ส่งคำร้องขอซ่อมแล้ว!");
            router.push("/staff");
        } else {
            const errorData = await response.json();
            console.error("API error:", errorData);
            alert("เกิดข้อผิดพลาด กรุณาลองใหม่");
        }

        const responseData = await response.json();
    };

    useEffect(() => {
        if (repairRequest) {
            setFormData((prevData) => ({
                ...prevData,
                repair_request: repairRequest.id,
            }));
        }
    }, [repairRequest]);

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
                    <form onSubmit={handleSubmit}>
                        <div className='row'>
                            <div className='col-3' id='remark-letter'>
                                หมายเหตุ :
                            </div>
                            <div className='col-6'>

                            </div>
                            <div className='col-3' id='room-letter'>
                                ห้อง {repairRequest?.student.room_id.room_number
                                    ? repairRequest.student.room_id.room_number.charAt(0).toUpperCase() + repairRequest.student.room_id.room_number.slice(1)
                                    : "Loading ..."}
                            </div>
                        </div>
                        <div id='remark-show-area'>
                            <input
                                type="text"
                                name="remarks"
                                className="form-control"
                                value={repairRequest?.description || "Loading ..."}
                                onChange={handleChange}
                                id='remarks-show'
                                readOnly
                                required>
                            </input>
                        </div>
                        <div className='row' id='status-and-urgency'>
                            <div className='col-6' id='status-area'>
                                <div id='status-letter'>
                                    สถานะหมายเหตุ :
                                </div>
                                <div id='status-input'>
                                    <input
                                        type="text"
                                        name="status"
                                        className="form-control"
                                        value={repairRequest?.status
                                            ? repairRequest.status.charAt(0).toUpperCase() + repairRequest.status.slice(1)
                                            : "Loading ..."}
                                        id='status-show'
                                        readOnly
                                        required>
                                    </input>
                                </div>
                            </div>
                            <div className='col-6'>
                                <div id='urgency-letter'>
                                    ความเร่งด่วน
                                </div>
                                <div id='urgency-input'>
                                    <input
                                        type="text"
                                        name="status"
                                        className="form-control"
                                        value={repairRequest?.urgency
                                            ? repairRequest.urgency.charAt(0).toUpperCase() + repairRequest.urgency.slice(1)
                                            : "Loading ..."}
                                        id='urgency-show'
                                        readOnly
                                        required>
                                    </input>
                                </div>
                            </div>
                        </div>
                        <div id='technician-assign-area'>
                            <div id='technician-assign-letter'>
                                มอบหมายงาน
                            </div>
                            <div className='row'>
                                <div className='col-8'>
                                    <select className="form-control"
                                        id='select-letter'
                                        name="technician"
                                        value={formData.technician[0] || ""}
                                        onChange={(e) => {
                                            const selectedTechnicianId = Number(e.target.value);
                                            setFormData((prevData) => ({
                                                ...prevData,
                                                technician: [selectedTechnicianId],
                                            }));
                                        }}
                                        required
                                    >
                                        <option value="" id='option-letter'>-- เลือกช่าง --</option>
                                        {technicians.map((tech) => (
                                            <option key={tech.id} value={tech.id} id='option-letter'>
                                                {tech.user.first_name} {tech.user.last_name}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <div className='col-4'>
                                    <div>
                                        <center>
                                            <button type="submit" className="btn btn-success" id='assignjobbutton'>
                                                มอบหมายงาน
                                            </button>
                                        </center>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>

                {/* responsive */}
                <div className="container d-block d-md-none" id="pagecon">
                    <form onSubmit={handleSubmit}>
                        <div className='row'>
                            <div className='col-12' id='room-letter'>
                                <center>
                                    ห้อง {repairRequest?.student.room_id.room_number
                                        ? repairRequest.student.room_id.room_number.charAt(0).toUpperCase() + repairRequest.student.room_id.room_number.slice(1)
                                        : "Loading ..."}
                                </center>
                            </div>
                        </div>

                        <div className='row'>
                            <div className='col-12' id='remark-letter'>
                                หมายเหตุ :
                            </div>
                        </div>
                        <div id='remark-show-area'>
                            <input
                                type="text"
                                name="remarks"
                                className="form-control"
                                value={repairRequest?.description || "Loading ..."}
                                onChange={handleChange}
                                id='remarks-show'
                                readOnly
                                required>
                            </input>
                        </div>
                        <div className='row' id='status-and-urgency'>
                            <div className='col-12' id='status-area'>
                                <div id='status-letter'>
                                    สถานะหมายเหตุ :
                                </div>
                                <div id='status-input'>
                                    <input
                                        type="text"
                                        name="status"
                                        className="form-control"
                                        value={repairRequest?.status
                                            ? repairRequest.status.charAt(0).toUpperCase() + repairRequest.status.slice(1)
                                            : "Loading ..."}
                                        id='status-show'
                                        readOnly
                                        required>
                                    </input>
                                </div>
                            </div>
                        </div>
                        <div className='row' id='status-and-urgency'>
                            <div className='col-12' id='status-area'>
                                <div id='urgency-letter'>
                                    ความเร่งด่วน
                                </div>
                                <div id='urgency-input'>
                                    <input
                                        type="text"
                                        name="status"
                                        className="form-control"
                                        value={repairRequest?.urgency
                                            ? repairRequest.urgency.charAt(0).toUpperCase() + repairRequest.urgency.slice(1)
                                            : "Loading ..."}
                                        id='urgency-show'
                                        readOnly
                                        required>
                                    </input>
                                </div>
                            </div>
                        </div>
                        <div id='technician-assign-area'>
                            <div id='technician-assign-letter'>
                                มอบหมายงาน
                            </div>
                            <div className='row'>
                                <div className='col-12'>
                                    <select className="form-control"
                                        id='select-letter'
                                        name="technician"
                                        value={formData.technician[0] || ""}
                                        onChange={(e) => {
                                            const selectedTechnicianId = Number(e.target.value);
                                            setFormData((prevData) => ({
                                                ...prevData,
                                                technician: [selectedTechnicianId],
                                            }));
                                        }}
                                        required
                                    >
                                        <option value="" id='option-letter'>-- เลือกช่าง --</option>
                                        {technicians.map((tech) => (
                                            <option key={tech.id} value={tech.id} id='option-letter'>
                                                {tech.user.first_name} {tech.user.last_name}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <div className='col-12' id='responsive-button-area'>
                                    <div>
                                        <center>
                                            <button type="submit" className="btn btn-success" id='assignjobbutton'>
                                                มอบหมายงาน
                                            </button>
                                        </center>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div >
        </>
    );
}