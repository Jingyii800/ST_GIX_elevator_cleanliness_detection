/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const Sidebar = ({ activePage }) => {
  const menuItems = [
    { name: "Dashboard", icon: "/img/icon-12.png", path: "/dashboard-station" },
    { name: "Report Logs", icon: "/img/icon-1.png", path: "/report-logs" },
    { name: "Elevator Status", icon: "/img/group-632545.png", path: "/elevator-status" },
    { name: "Settings", icon: "/img/icon-6.png", path: "/settings" },
  ];

  return (
    <aside className="sidebar">
      {/* ✅ Logo Section (No Stretching) */}
      <div className="sidebar-logo">
        <img src="/img/web-brand-logo-horizontal-blue-rgb-1.png" alt="SoundTransit Logo" />
      </div>

      {/* ✅ Sidebar Menu */}
      <nav className="sidebar-menu">
        {menuItems.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className={`sidebar-item ${activePage === item.name ? "active" : ""}`}
          >
            <img src={item.icon} alt={item.name} className="sidebar-icon" />
            <span className="sidebar-text">{item.name}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
};

Sidebar.propTypes = {
  activePage: PropTypes.string.isRequired, // Current active page for highlighting
};


// import PropTypes from "prop-types";
// import React from "react";
// import { Link } from "react-router-dom";
// import { Dashboard } from "../Dashboard";
// import { LocalLibrary } from "../LocalLibrary";
// import { Login } from "../Login";
// import { Security } from "../Security";
// import { Settings } from "../Settings";
// import { ShowChart } from "../ShowChart";
// import "./style.css";

// export const Sidebar = ({
//   className,
//   frameClassName,
//   text = "Activity",
//   hasFrame = true,
//   text1 = "Security",
//   visible = true,
//   hasDiv = true,
//   hasFrame1 = true,
//   loginLoginClassName,
//   loginLogin = "/img/icon-7.png",
//   hasLogo = true,
//   divClassName,
//   dashboardDashboard = "/img/icon.png",
//   frameClassNameOverride,
//   divClassNameOverride,
//   to,
//   to1,
//   to2,
// }) => {
//   return (
//     <div className={`sidebar ${className}`}>
//       <img className="line" alt="Line" src="/img/line-16.png" />

//       <div className="frame">
//         <Link className={`div ${frameClassName}`} to={to2}>
//           <div className={`text-wrapper ${divClassName}`}>Dashboard</div>

//           <Dashboard className="icon" dashboard={dashboardDashboard} />
//         </Link>

//         <Link className="frame-2" to={to}>
//           <div className="text-wrapper-2">{text}</div>

//           <ShowChart className="icon" showChart="/img/icon-1.png" />
//         </Link>

//         {hasFrame && (
//           <div className="frame-3">
//             <div className="text-wrapper-2">Library</div>

//             <LocalLibrary className="icon" localLibrary="/img/icon-2.png" />
//           </div>
//         )}

//         <Link className={`frame-2 ${frameClassNameOverride}`} to={to1}>
//           <div className={`text-wrapper-2 ${divClassNameOverride}`}>
//             {text1}
//           </div>

//           {visible && <Security className="icon" security="/img/icon-3.png" />}
//         </Link>

//         <div className="frame-3">
//           <div className="text-wrapper-2">Settings</div>

//           <Settings className="icon" settings="/img/icon-6.png" />
//         </div>
//       </div>

//       <div className="frame-4">
//         <div className="text-wrapper-2">Log Out</div>

//         <Login className={loginLoginClassName} login={loginLogin} />
//       </div>

//       {hasLogo && (
//         <div className="logo">
//           <div className="text">
//             <div className="text-wrapper-3">DASHBOARD</div>

//             <div className="text-wrapper-4">VENUS</div>
//           </div>

//           <div className="group-wrapper">
//             <img className="group" alt="Group" src="/img/group-51.png" />
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// Sidebar.propTypes = {
//   text: PropTypes.string,
//   hasFrame: PropTypes.bool,
//   text1: PropTypes.string,
//   visible: PropTypes.bool,
//   hasDiv: PropTypes.bool,
//   hasFrame1: PropTypes.bool,
//   loginLogin: PropTypes.string,
//   hasLogo: PropTypes.bool,
//   dashboardDashboard: PropTypes.string,
//   to: PropTypes.string,
//   to1: PropTypes.string,
//   to2: PropTypes.string,
// };
