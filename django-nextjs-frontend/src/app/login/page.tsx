// "use client";
// import { useState } from "react";
// import axios from "axios";
// import { useRouter } from "next/navigation";

// export default function LoginPage() {
//     const router = useRouter();
//     const [formData, setFormData] = useState({ username: "", password: "" });
//     const [studentId, setStudentId] = useState<number | null>(null);

//     const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//         setFormData({ ...formData, [e.target.name]: e.target.value });
//     };

//     const handleSubmit = async (e: React.FormEvent) => {
//         e.preventDefault();
//         try {
//             const response = await axios.post("http://localhost:8000/auth/api/login/", formData);
//             setStudentId(response.data.student_id);
//             localStorage.setItem("student_id", response.data.student_id); // เก็บ student_id ใน localStorage
//             alert("เข้าสู่ระบบสำเร็จ! Student ID: " + response.data.student_id);
//             router.push("/dashboard"); // นำทางไปหน้า Dashboard หรือหน้าอื่น
//         } catch (error: unknown) {
//             if (axios.isAxiosError(error)) {
//                 // ตรวจสอบว่า error เป็น AxiosError หรือไม่
//                 alert("เกิดข้อผิดพลาด: " + error.response?.data?.error || "ไม่สามารถลงทะเบียนได้");
//             } else {
//                 alert("เกิดข้อผิดพลาดไม่ทราบสาเหตุ");
//             }
//         }
//     };

//     return (
//         <div>
//             <h2>เข้าสู่ระบบ</h2>
//             <form onSubmit={handleSubmit}>
//                 <input type="text" name="username" placeholder="Username" onChange={handleChange} required />
//                 <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
//                 <button type="submit">เข้าสู่ระบบ</button>
//             </form>
//             {studentId && <p>Student ID: {studentId}</p>}
//         </div>
//     );
// }
"use client";
import '../login/login.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/utils/auth"; // Import ฟังก์ชัน login ที่สร้างไว้
import axios from "axios";

export default function LoginPage() {
    const router = useRouter();
    const [formData, setFormData] = useState({ username: "", password: "" });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const data = await login(formData.username, formData.password);
            // console.log(data); // ✅ ตรวจสอบค่าที่ได้จาก API

            const studentId = data.student_id;
            const technicianId = data.technician_id;
            const role = data.user.role;

            if (studentId) {
                localStorage.setItem("student_id", studentId);
            }
            if (technicianId) {
                localStorage.setItem("technician_id", technicianId);
            }

            alert(`เข้าสู่ระบบสำเร็จ! Role: ${role} ${studentId ? "Student ID: " + studentId : ""} ${technicianId ? "Technician ID: " + technicianId : ""}`);
            // alert("เข้าสู่ระบบสำเร็จ! Student ID: " + data.student_id);
            if (studentId) {
                // localStorage.setItem("student_id", studentId);
                router.push("/student");
            }
            if (technicianId) {
                // localStorage.setItem("technician_id", technicianId);
                router.push("/technician");
            }
            // router.push("/dashboard"); // นำทางไปหน้า Dashboard
        } catch (error: unknown) {
            if (axios.isAxiosError(error)) {
                // ตรวจสอบว่า error เป็น AxiosError หรือไม่
                alert("เกิดข้อผิดพลาด: " + error.response?.data?.error || "ไม่สามารถลงทะเบียนได้");
            } else {
                alert("เกิดข้อผิดพลาดไม่ทราบสาเหตุ");
            }
        }
    };

    return (
        <div id='content'>
            <div className="container" id="pagecon">
                <center>
                    <div className="card" id='login-menu'>
                        <div id='login-title-area'>
                            <p id='login-title'>เข้าสู่ระบบ</p>
                        </div>

                        <form onSubmit={handleSubmit}>
                            <center>
                                <div id='input-area'>
                                    <input type="text" name="username" id='input-text' placeholder="Username" onChange={handleChange} required />
                                </div>
                            </center>
                            <center>
                                <div id='input-area'>
                                    <input type="password" name="password" id='input-text' placeholder="Password" onChange={handleChange} required />
                                </div>
                            </center>
                            <div id='button-area'>
                                <button type="submit" id='login-button-submit' className="btn btn-primary">เข้าสู่ระบบ</button>
                            </div>

                        </form>
                    </div>
                </center>
            </div>
        </div>

    );
}

