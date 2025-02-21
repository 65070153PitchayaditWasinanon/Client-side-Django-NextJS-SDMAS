// app/nontakorn/page.tsx
'use client'
import '../[id]/staffassignjob.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
// import { getProfile } from "@/utils/auth";
import { useState, useEffect } from "react";
import { useParams } from 'next/navigation';


export default function StaffAssignJobPage() {
    const { id } = useParams();
    // const [profile, setProfile] = useState<any>(null);
    // const [error, setError] = useState<string | null>(null);
    // useEffect(() => {
    //     // 
    //     async function fetchProfile() {
    //         try {
    //             // getProfile ดึงข้อมูลมาจาก django ใส่ data
    //             const data = await getProfile();
    //             //Profile ถูก set จาก setProfile ด้วยข้อมูล data ที่ได้มาจาก getProfile 
    //             setProfile(data);

    //         } catch (err) {
    //             setError("ไม่สามารถดึงข้อมูลโปรไฟล์ได้");
    //         }
    //     }
    //     fetchProfile();
    // }, []);

    const [technicians, setTechnicians] = useState<{ id: number, name: string }[]>([]);

    useEffect(() => {
        const fetchTechnicians = async () => {
            try {
                const response = await axios.get('http://localhost:8080/api/staff/technician/');
                // // , {
                //     headers: {
                //         Authorization: `Bearer ${localStorage.getItem("access_token")}` // ใส่ Token ด้วย
                //     }
                // });
                setTechnicians(response.data);
            } catch (error) {
                console.error("Error fetching technicians", error);
            }
        };

        fetchTechnicians();
    }, []);

    const [repairRequest, setRepairRequest] = useState(null);

    useEffect(() => {
        if (id) {
            const fetchRepairRequest = async () => {
                try {
                    const response = await axios.get(`http://localhost:8080/api/repair-requests-staff/${id}/`);
                    setRepairRequest(response.data);
                    console.log(response.data);
                } catch (error) {
                    console.error('Error fetching repair request:', error);
                }
            };

            fetchRepairRequest();
        }
    }, [id]);

    const [formData, setFormData] = useState({
        repair_request: "",
        technician: [],
        status: "assigned",
    });

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
                    <form onSubmit={handleSubmit}>
                        <div className='row'>
                            <div className='col-3' id='remark-letter'>
                                หมายเหตุ :
                            </div>
                            <div className='col-6'>

                            </div>
                            <div className='col-3' id='room-letter'>
                                ห้อง {repairRequest?.student.room_id.room_number || "Loading ..."}
                            </div>
                        </div>
                        <div id='remark-show-area'>
                            <input
                                type="text"
                                name="remarks"
                                className="form-control"
                                value={formData?.remarks}
                                // value={repairRequest?.description || "Loading ..."}
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
                                        // value={formData.remarks}
                                        value={repairRequest?.status || "Loading ..."}
                                        // onChange={handleChange}
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
                                        // value={formData.remarks}
                                        value={repairRequest?.urgency || "Loading ..."}
                                        // onChange={handleChange}
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
                                    <select className="form-control" id='select-letter'>
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
                                            <a href="" className="btn btn-success" id='assignjobbutton'>
                                                มอบหมายงาน
                                            </a>
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