import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Sidebar } from "../../components/Sidebar";
import { ActiveAlerts } from "../ActiveAlerts/ActiveAlerts";
import "./style.css";


export const DashboardStation = () => {

  const stationName = "University of Washington"; // Example station name

  // Elevator status data
  const elevators = [
    { id: 1, status: "Good" },
    { id: 2, status: "Warning" },
    { id: 3, status: "Warning" },
    { id: 4, status: "Good" },
    { id: 5, status: "Good" },
    { id: 6, status: "Warning" },
    { id: 7, status: "Good" },
    { id: 8, status: "Good" },
  ];

  const [showAlert, setShowAlert] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    // Auto-hide the alert after 10 seconds
    const timer = setTimeout(() => setShowAlert(false), 100000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="dashboard-station">
      <div className="div-4">
        <div className="overlap-7">
          <div className="rectangle-3" />

          <div className="rectangle-4" />

          <img className="chart" alt="Chart" src="/img/chart.png" />

          <div className="high-line">
            <img className="line-2" alt="Line" src="/img/line-11.png" />

            <div className="text-wrapper-12">6</div>
          </div>

          <div className="high-line-2">
            <img className="line-3" alt="Line" src="/img/line-11-1.png" />

            <div className="text-wrapper-13">15</div>
          </div>

          <div className="navbar">
            <div className="text-wrapper-14">2</div>

            <div className="text-wrapper-15">3</div>

            <div className="text-wrapper-16">4</div>

            <div className="text-wrapper-17">5</div>

            <div className="text-wrapper-18">6</div>

            <div className="text-wrapper-19">8</div>

            <div className="text-wrapper-20">9</div>

            <div className="text-wrapper-21">10</div>

            <div className="text-wrapper-22">11</div>

            <div className="text-wrapper-23">12</div>

            <div className="text-wrapper-24">13</div>

            <div className="text-wrapper-25">7</div>
          </div>

          <div className="navbar-2">
            <div className="text-wrapper-15">2</div>

            <div className="text-wrapper-14">1</div>

            <div className="text-wrapper-26">3</div>

            <div className="text-wrapper-17">4</div>

            <div className="text-wrapper-27">5</div>

            <div className="text-wrapper-25">6</div>

            <div className="text-wrapper-28">9</div>

            <div className="text-wrapper-22">10</div>

            <div className="text-wrapper-23">11</div>

            <div className="text-wrapper-29">12</div>

            <div className="text-wrapper-30">13</div>

            <div className="text-wrapper-31">7</div>
          </div>

          <div className="label">Weekly Cleanliness Summary</div>

          <p className="cash">
            <span className="span">32</span>

            <span className="text-wrapper-32">&nbsp;&nbsp;</span>

            <span className="text-wrapper-33">alerts</span>

            <span className="text-wrapper-34">&nbsp;</span>

            <span className="text-wrapper-33">in this week</span>
          </p>

          <div className="group-6">
            <div className="overlap-group-6">
              <div className="rectangle-5" />

              <div className="rectangle-6" />

              <div className="text-wrapper-35">Daily</div>

              <div className="text-wrapper-36">Weekly</div>

              <div className="text-wrapper-37">Monthly</div>

              <div className="text-wrapper-38">Yearly</div>
            </div>
          </div>

          <div className="group-7">
            <div className="overlap-8">
              <div className="rectangle-7" />

              <div className="text-wrapper-39">Cause Analysis Report</div>
            </div>
          </div>

          {/* Elevator Status Section */}
          <div className="medium-chart">
            <div className="label-wrapper">
              <Link className="label-2" to="/elevator-status">Elevators Status</Link>
            {/* Elevator Status Section */}
            <div className="elevator-status-section">
              <div className="elevator-grid">
                {elevators.map((elevator) => (
                  <div key={elevator.id} className="elevator-item">
                    {/* Elevator Name */}
                    <div className="text-wrapper-40">Elevator {elevator.id}</div>

                    {/* Clickable Status Box */}
                    <Link
                      to={`/elevator-status/${encodeURIComponent(stationName)}/${elevator.id}`}
                      className={`depth-frame ${elevator.status.toLowerCase()}`}
                    >
                      <div className="depth-frame-2">
                        <div className="text-wrapper-47">{elevator.status}</div>
                      </div>
                    </Link>
                  </div>
                ))}
              </div>
            </div>
            </div>
          </div>

          <div className="label-3">Daily Avg Resolution Time</div>

          <p className="p">
            <span className="span">15 </span>

            <span className="text-wrapper-33">mins</span>
          </p>

          <div className="chart-2">
            <div className="rectangle-9" />

            <div className="rectangle-10" />

            <div className="rectangle-11" />

            <div className="rectangle-12" />

            <div className="rectangle-13" />

            <div className="rectangle-14" />

            <div className="rectangle-15" />
          </div>
        </div>

        <div className="text-wrapper-49">Hi Andrei,</div>

        <div className="text-wrapper-50">University of Washington Station</div>

        <div className="overlap-9">
          <Link className="medium-chart-2" to="/report-logs">
            <div className="overlap-10">
              <div className="medium-chart-3">
                <div className="label-2">Report Logs</div>
              </div>

              <div className="name-2">UW Station, Elevator 2</div>

              <div className="date-2">12:00pm&nbsp;&nbsp;2024/12/07</div>

              <img
                className="vector-9"
                alt="Vector"
                src="/img/vector-2-3.png"
              />

              <div className="rectangle-16" />
            </div>
          </Link>

          <div className="name-3">UW Station, Elevator 7</div>

          <div className="group-8">
            <div className="overlap-11">
              <img
                className="group-9"
                alt="Group"
                src="/img/group-632523.png"
              />

              <img
                className="on-track-3"
                alt="On track"
                src="/img/on-track.png"
              />
            </div>
          </div>

          <div className="group-10">
            <img className="group-11" alt="Group" src="/img/group-632523.png" />
          </div>

          <div className="name-4">Warning</div>

          <div className="name-5">Warning</div>

          <div className="date-3">Resolution in progress</div>

          <div className="date-4">Resolution in progress</div>

          <div className="group-10">
            <div className="overlap-11">
              <img
                className="group-9"
                alt="Group"
                src="/img/group-632523.png"
              />

              <img
                className="on-track-3"
                alt="On track"
                src="/img/on-track.png"
              />
            </div>
          </div>
        </div>

        <div className="overlap-12">
          <img className="vector-10" alt="Vector" src="/img/vector-2.png" />

          <div className="group-12">
            <div className="overlap-13">
              <Sidebar activePage="Dashboard" />
            </div>
          </div>
        </div>

          {/* 🚨 Updated Notification Alert (Same Structure & Classes) */}
          {showAlert && (
            <div className="overlap-14" onClick={() => setModalOpen(true)}>
            <div className="rectangle-17" />
            <p className="new-cleanliness">
              New Cleanliness Alert at {stationName} Elevator 3: Liquid Waste!
            </p>
            <img
              className="group-14"
              alt="Group"
              src="https://cdn.animaapp.com/projects/679b2ae904e702c3d5b68b5e/releases/679bf0db758798aa49c71be6/img/group-4@2x.png"
            />
            <button className="close-alert" onClick={(e) => { 
              e.stopPropagation();  // ✅ Prevents clicking from opening the modal
              setShowAlert(false);
            }}>✖</button>
          </div>
          )}
          <ActiveAlerts isOpen={modalOpen} onClose={() => setModalOpen(false)} />
          
        {/* 🚨 Active Alerts */}
        <div className="frame-5">
          <div className="group-15" onClick={() => setModalOpen(true)}>
            <div className="overlap-group-7">
              <img className="vector-11" alt="Vector" src="/img/vector-3.png" />

              <div className="group-16" />

              <div className="text-wrapper-51">4</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
