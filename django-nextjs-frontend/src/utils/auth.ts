import axios from "axios";


export async function login(username: string, password: string) {
    const response = await fetch("http://localhost:8080/auth/api/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
        throw new Error("Invalid credentials");
    }

    const data = await response.json();
    localStorage.setItem("accessToken", data.access);
    localStorage.setItem("refreshToken", data.refresh);
    localStorage.setItem("student_id", data.student_id); // บันทึก student_id ไว้

    return data;
}

//ดึงข้อมูลจาก django 
export async function getProfile() {
    //ต้องมีการ login ก่อน จะได้ token
    const token = localStorage.getItem("accessToken");
    if (!token) {
        throw new Error("No access token found");
    }
    //ดึงข้อมูลจาก ลิงค์นี้ที่ run มาจาก django
    const response = await fetch("http://localhost:8080/api/profile/", {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` },
    });

    if (!response.ok) {
        throw new Error("Failed to fetch profile");
    }

    return await response.json();
}

export function getAccessToken() {
    return localStorage.getItem("accessToken");
}


// export async function refreshToken() {
//     const refresh = localStorage.getItem("refreshToken");
//     if (!refresh) {
//         throw new Error("No refresh token found");
//     }

//     const response = await fetch("http://localhost:8080/auth/api/token/refresh/", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ refresh }),
//     });

//     if (!response.ok) {
//         throw new Error("Failed to refresh token");
//     }

//     const data = await response.json();
//     localStorage.setItem("accessToken", data.access);
//     return data.access;
// }

