// app/nontakorn/page.tsx
import '../styles.css';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function NontakornPage() {
    return (
        <html lang="en">

            <body>
                <div id="nav">
                    <header>
                        <nav>ROOM:</nav>
                    </header>
                </div>

                <div id="content">
                    <div
                        className="d-flex flex-column flex-shrink-0 p-3"
                        style={{ width: '400px' }}
                        id="sidebarbg"
                    >
                        <span className="badge bg-white text-dark" id="sidebartitleout">
                            <div className="sidebartitlefont">รายงานปัญหา</div>
                        </span>
                        <ul className="nav nav-pills flex-column mb-auto" id="sidebarselected">
                            <li><a href="" className="nav-link link-dark">
                                <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M44 12C44 9.8 42.2 8 40 8H8C5.8 8 4 9.8 4 12M44 12V36C44 38.2 42.2 40 40 40H8C5.8 40 4 38.2 4 36V12M44 12L24 26L4 12" stroke="#1E1E1E" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />
                                </svg>
                                ปัญหาที่ส่ง
                            </a></li>
                        </ul>
                    </div>
                    <div className="container" id="pagecon">

                    </div>
                </div>
            </body>
        </html>
    );
}