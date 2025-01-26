// app/nontakorn/page.tsx
import Layout from '../layout';  // Import Layout
import '../styles.css';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function NontakornPage() {
  return (
    <Layout
      nav={<span>Room:</span>}
      head={<h1></h1>}
      sidebarTitle={<span>รายงานปัญหา</span>}
      sidebarContent={<li><a href="" className="nav-link link-dark">
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M44 12C44 9.8 42.2 8 40 8H8C5.8 8 4 9.8 4 12M44 12V36C44 38.2 42.2 40 40 40H8C5.8 40 4 38.2 4 36V12M44 12L24 26L4 12" stroke="#1E1E1E" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        ปัญหาที่ส่ง
      </a></li>}
      content={<div><p>This is the main content of Nontakorn Page.</p></div>}
    >
      <div>
        <h2>This is additional content passed through children in NontakornPage.</h2>
      </div>
    </Layout>
  );
}