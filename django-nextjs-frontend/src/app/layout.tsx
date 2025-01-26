// app/layout.tsx
import './styles.css';
import 'bootstrap/dist/css/bootstrap.min.css';

interface LayoutProps {
  children: React.ReactNode;
  nav: React.ReactNode;
  head: React.ReactNode;
  sidebarTitle: React.ReactNode;
  sidebarContent: React.ReactNode;
  content: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({
  nav,
  head,
  sidebarTitle,
  sidebarContent,
  content,
  children,
}) => {
  return (
    <html lang="en">
      <body>
        <div id="nav">
          <header>
            <nav>{nav}</nav>
          </header>
        </div>
        <div id="head">{head}</div>
        <div id="content">
          <div
            className="d-flex flex-column flex-shrink-0 p-3"
            style={{ width: '400px' }}
            id="sidebarbg"
          >
            <span className="badge bg-white text-dark" id="sidebartitleout">
              <div className="sidebartitlefont">{sidebarTitle}</div>
            </span>
            <ul className="nav nav-pills flex-column mb-auto" id="sidebarselected">
              {sidebarContent}
            </ul>
          </div>
          <div className="container" id="pagecon">
            {children || content}
          </div>
        </div>
      </body>
    </html>
  );
};

export default Layout;