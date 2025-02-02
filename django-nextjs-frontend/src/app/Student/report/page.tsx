// app/nontakorn/page.tsx
'use client'
import '../report/studentreport.css';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function StudentReportPage() {
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
                            <span id='reportproblemspan'>รายงานปัญหา</span>
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
                                        <svg width="50" height="51" viewBox="0 0 50 51" fill="none" xmlns="http://www.w3.org/2000/svg">
                                            <path d="M25 19.125V27.625M25 36.125H25.0208M21.4375 8.20249L3.79165 38.25C3.42783 38.8926 3.23533 39.6213 3.23329 40.3633C3.23126 41.1054 3.41975 41.8351 3.78004 42.4799C4.14032 43.1246 4.65983 43.6618 5.28687 44.0382C5.91392 44.4145 6.62665 44.6168 7.35415 44.625H42.6458C43.3733 44.6168 44.086 44.4145 44.7131 44.0382C45.3401 43.6618 45.8596 43.1246 46.2199 42.4799C46.5802 41.8351 46.7687 41.1054 46.7667 40.3633C46.7646 39.6213 46.5721 38.8926 46.2083 38.25L28.5625 8.20249C28.1911 7.57797 27.6682 7.06162 27.0441 6.70327C26.4201 6.34492 25.7161 6.15666 25 6.15666C24.2839 6.15666 23.5798 6.34492 22.9558 6.70327C22.3318 7.06162 21.8089 7.57797 21.4375 8.20249Z" stroke="#1E1E1E" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
                                        </svg>
                                    </div>
                                    <div className='col-10' >
                                        <center id='sidebarlinkmenu'>รายงานปัญหา</center>
                                    </div>
                                </div>
                            </a>
                        </li>
                    </ul>
                </div>
                <div className="container" id="pagecon">
                    <div className="emp-form-box">
                        <form>
                            <div className="form-group mb-3">
                                <label htmlFor="description" id="student1label">
                                    อธิบายสาเหตุ :
                                </label>
                                <div className="student1textarea">
                                    <textarea
                                        id="description"
                                        // value="{description}"
                                        // onChange={(e) => setDescription(e.target.value)}
                                        className="form-control"
                                        placeholder="กรุณาอธิบาย..."
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
                                        id="urgency"
                                        // onChange={(e) => setUrgency(e.target.value)}
                                        className="form-select"
                                        required
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
                                        id="repairAppointmentTime"
                                        // onChange={(e) => setRepairAppointmentTime(e.target.value)}
                                        onFocus={(e) => e.target.showPicker()}
                                        className="form-control"
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