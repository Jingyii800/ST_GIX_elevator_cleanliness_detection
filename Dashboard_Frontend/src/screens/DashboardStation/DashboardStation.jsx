import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { Sidebar } from "../../components/sidebar";
import API_BASE_URL from "../../config";
import { ActiveAlerts } from "../ActiveAlerts/ActiveAlerts";
import "./style.css";


export const DashboardStation = () => {
  const socketRef = useRef(null);
  const [stationName, setStationName] = useState("University of Washington"); // Default Station
  const [elevators, setElevators] = useState([]); // Store fetched elevator data
  const [reportLogs, setReportLogs] = useState([]);
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState("")
  const [modalOpen, setModalOpen] = useState(false);

  const stationOptions = [
    "University of Washington",
    "Seattle Central",
    "Pioneer Square",
    "Westlake",
    "Columbia City",
    "Bellevue Station",
  ];

  const fetchElevatorStatus = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/elevator_status?station=${encodeURIComponent(stationName)}`
      );

      if (!response.ok) throw new Error("Failed to fetch elevator status");

      const data = await response.json();

      const updatedElevators = data
      .map((elevator) => ({
        id: elevator.elevator_num,
        status: elevator.alert_status, // Use Alert_Status from database
      }))
      .sort((a, b) => a.id - b.id);

      setElevators(() => updatedElevators);
    } catch (error) {
      console.error("Error fetching elevator status:", error);
    }
  };

  const fetchReportLogs = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/report_logs?time_filter=weekly&station=${encodeURIComponent(stationName)}`
      );

      if (!response.ok) throw new Error("Failed to fetch report logs");

      const data = await response.json();

      // 🔹 Store only the latest 5 logs
      const latestLogs = data.slice(0, 5);

      setReportLogs(latestLogs);
      console.log("Fetched Report Logs:", data);
    } catch (error) {
      console.error("Error fetching report logs:", error);
    }
  };

  // 🔹 Fetch elevator status & report logs from the backend
  useEffect(() => {
    fetchElevatorStatus();
    fetchReportLogs();
  }, [stationName]);


  useEffect(() => {
    const connectWebSocket = () => {
      if (socketRef.current) {
        socketRef.current.close(); // ✅ Close previous instance before reconnecting
      }

      const ws = new WebSocket("wss://fastapi-websocket-app-fdh0bnc8ffgtdecu.westus-01.azurewebsites.net/ws");
      socketRef.current = ws; // ✅ Store WebSocket instance

      ws.onopen = () => {
        console.log("✅ WebSocket connection established!");
      };

      ws.onmessage = (event) => {
        console.log("🚨 Alert received:", event.data);
        setAlertMessage(event.data);
        setShowAlert(true);

        // Extract station name if available in the message
        const match = event.data.match(/at (.+?) Elevator/);
        if (match) setStationName(match[1]);

        // Auto-hide alert after 5 seconds
        setTimeout(() => setShowAlert(false), 5000);
      };

      ws.onerror = (error) => {
        console.error("❌ WebSocket error:", error);
      };

      ws.onclose = () => {
        console.warn("⚠️ WebSocket connection closed! Reconnecting...");
        socketRef.current = null; // ✅ Prevents old WebSocket instance reuse
        setTimeout(() => connectWebSocket(), 5000); // ✅ Correct reconnection logic
      };
    };

    connectWebSocket(); // ✅ Initial connection

    return () => {
      if (socketRef.current) {
        socketRef.current.close(); // ✅ Cleanup WebSocket on component unmount
      }
    };
  }, []); // ✅ Runs only once at mount

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
                      className={`depth-frame ${elevator.status === "Normal" ? "good-status" : "warning-status"}`}
                    >
                      <div className="depth-frame-2">
                        <div className="text-wrapper-47">{elevator.status === "Normal" ? "Good" : "Warning"}</div>
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

        <div className="dropdown-container">
          <select 
            className="text-wrapper-50"
            value={stationName} Station
            onChange={(e) => setStationName(e.target.value)}
          >
            {stationOptions.map((station) => (
              <option key={station} value={station}>
                {station}
              </option>
            ))}
          </select>
          <span className="text-wrapper-50"> Station</span> {/* Added station text */}
        </div>

        <div className="overlap-9">
          <Link className="label-2"  to="/report-logs">Report Logs</Link>

          <div className="report-logs-content">
            {reportLogs.length > 0 ? (
              reportLogs.map((log, index) => (
                <div key={index} className="report-log-item">
                    {/* 🚀 Elevator Location at the Top */}
                    <p className="log-location">
                      <strong>{log.station}, Elevator {log.elevatorNumber}</strong>
                    </p>

                    {/* 🔹 Alert Icon & Status Progress in Flexbox */}
                    <div className="log-details">
                      <div className="log-icon">
                        <img
                          src={log.resolved ? "/img/checkmark.png" : "/img/on-track.png"}
                          alt={log.resolved ? "Resolved" : "Warning"}
                          className={log.resolved ? "resolved-icon" : "warning-icon"}
                        />
                      </div>
                      <div className="log-status-text">
                        <p className={`status-text ${log.resolved ? "status-resolved" : "status-warning"}`}>
                          {log.resolved ? "Resolved" : "Warning"}
                        </p>
                      </div>
                    </div>

                    {/* ⏳ Timestamp at the Bottom */}
                    <p className="log-time">{new Date(log.timeStamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })} {new Date(log.timeStamp).toLocaleDateString()}</p>
                    
                  </div>
              ))
            ) : (
              <p className="no-logs">No reports available.</p>
            )}
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
              {alertMessage}
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
