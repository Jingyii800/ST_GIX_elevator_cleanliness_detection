import React, { useState, useEffect } from "react";
import { Link , useParams} from "react-router-dom";
import API_BASE_URL from "../../config";
import { ActiveAlerts } from "../ActiveAlerts/ActiveAlerts";
import { Sidebar } from "../../components/sidebar";
import "./style.css";

export const DashboardElevator = () => {

  const [showAlert, setShowAlert] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [reportLogs, setReportLogs] = useState([]);
  const { stationName, elevatorId } = useParams(); // ✅ Extract URL parameters
  const decodedStationName = decodeURIComponent(stationName);

  // State to hold sensor data
  const [sensorData, setSensorData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  useEffect(() => {
    const socket = new WebSocket("wss://fastapi-websocket-app-fdh0bnc8ffgtdecu.westus-01.azurewebsites.net/ws");

    socket.onopen = () => {
      console.log("✅ WebSocket connection established!");
    };

    socket.onmessage = (event) => {
      console.log("🚨 Alert received:", event.data);
      const alertData = event.data;

      // Extract alert message dynamically
      setAlertMessage(alertData);
      setShowAlert(true);
      
      // Extract station name if available in the message
      const match = alertData.match(/at (.+?) Elevator/);
      if (match) setStationName(match[1]);

      // Auto-hide the alert after 5 seconds
      setTimeout(() => setShowAlert(false), 5000);
    };

    socket.onerror = (error) => {
      console.error("❌ WebSocket error:", error);
    };

    socket.onclose = () => {
      console.warn("⚠️ WebSocket connection closed! Reconnecting...");
      setTimeout(() => {
        socket = new WebSocket("wss://fastapi-websocket-app-fdh0bnc8ffgtdecu.westus-01.azurewebsites.net/ws");
      }, 5000); // Try to reconnect in 5 seconds
    };

    return () => socket.close(); // Cleanup on component unmount
  }, []);


  const fetchElevatorData = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/elevator_status?station=${encodeURIComponent(stationName)}&elevator_num=${elevatorId}`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      if (data.length === 0) {
        throw new Error("No data found for this elevator.");
      }

      setSensorData(data[0]); // Store first record in state
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchReportLogs = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/report_logs?time_filter=weekly&station=${encodeURIComponent(stationName)}&elevator_num=${elevatorId}`
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


  useEffect(() => {
    fetchElevatorData();
    fetchReportLogs();
  }, [stationName, elevatorId]);

  // ✅ Show loading or error messages before rendering UI
  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p className="loading-text">Fetching Elevator Data...</p>
      </div>
    );
  }
  

  if (error) {
    return <p>Error fetching data: {error}</p>;
  }

  return (
    <div className="dashboard-elevator">
      <div className="div-6">
        <div className="overlap-35">
          <div className="rectangle-19" />

          <div className="rectangle-20" />

          <img className="chart-3" alt="Chart" src="/img/chart.png" />

          <div className="high-line-3">
            <img className="line-5" alt="Line" src="/img/line-11.png" />

            <div className="text-wrapper-84">6</div>
          </div>

          <div className="high-line-4">
            <img className="line-6" alt="Line" src="/img/line-11-1.png" />

            <div className="text-wrapper-85">15</div>
          </div>

          <div className="navbar-3">
            <div className="text-wrapper-86">2</div>

            <div className="text-wrapper-87">3</div>

            <div className="text-wrapper-88">4</div>

            <div className="text-wrapper-89">5</div>

            <div className="text-wrapper-90">6</div>

            <div className="text-wrapper-91">8</div>

            <div className="text-wrapper-92">9</div>

            <div className="text-wrapper-93">10</div>

            <div className="text-wrapper-94">11</div>

            <div className="text-wrapper-95">12</div>

            <div className="text-wrapper-96">13</div>

            <div className="text-wrapper-97">7</div>
          </div>

          <div className="navbar-4">
            <div className="text-wrapper-87">2</div>

            <div className="text-wrapper-86">1</div>

            <div className="text-wrapper-98">3</div>

            <div className="text-wrapper-89">4</div>

            <div className="text-wrapper-99">5</div>

            <div className="text-wrapper-97">6</div>

            <div className="text-wrapper-100">9</div>

            <div className="text-wrapper-94">10</div>

            <div className="text-wrapper-95">11</div>

            <div className="text-wrapper-101">12</div>

            <div className="text-wrapper-102">13</div>

            <div className="text-wrapper-103">7</div>
          </div>

          <div className="label-4">Weekly Cleanliness Summary</div>

          <p className="cash-2">
            <span className="text-wrapper-104">32</span>

            <span className="text-wrapper-105">&nbsp;&nbsp;</span>

            <span className="text-wrapper-106">alerts</span>

            <span className="text-wrapper-107">&nbsp;</span>

            <span className="text-wrapper-106">in this week</span>
          </p>

          <div className="group-28">
            <div className="overlap-group-10">
              <div className="rectangle-21" />

              <div className="rectangle-22" />

              <div className="text-wrapper-108">Daily</div>

              <div className="text-wrapper-109">Weekly</div>

              <div className="text-wrapper-110">Monthly</div>

              <div className="text-wrapper-111">Yearly</div>
            </div>
          </div>

          <div className="group-29">
            <div className="overlap-36">
              <div className="rectangle-23" />

              <div className="text-wrapper-112">Cause Analysis Report</div>
            </div>
          </div>

          <div className="label-5">Daily Avg Resolution Time</div>

          <p className="cash-3">
            <span className="text-wrapper-104">15 </span>

            <span className="text-wrapper-106">mins</span>
          </p>

          <div className="chart-4">
            <div className="rectangle-24" />

            <div className="rectangle-25" />

            <div className="rectangle-26" />

            <div className="rectangle-27" />

            <div className="rectangle-28" />

            <div className="rectangle-29" />

            <div className="rectangle-30" />
          </div>

          <div className="medium-chart">
            <div className="overlap-37">
            <Link className="label-2" to="/report-logs">Elevators Status</Link>
            <div className="sensor-content">
              {/* Sensor List */}
              <div className="sensor-list">
              <div className="sensor-item">
              <div className="div-7">
                      <div className="noun-passenger">
                        <img
                          className="element-passanger"
                          alt="Element passanger"
                          src="/img/19-passanger-5.png"
                        />
                      </div>
                    </div>
                <div className="sensor-info">
                  <p className="sensor-name">Passenger Report</p>
                  <p className="sensor-value">Report : {sensorData.passenger_button ? "on" : "off"}</p>
                </div>     
                <div className={`sensor-status ${sensorData.passenger_button_status === "Good" ? "good" : "warning"}`}>
                  {sensorData.passenger_button_status === "Good" ? (
                    <div className="on-track-6">
                    <div className="done-instance-wrapper">
                      <img className="done done-2" alt="Done" src="/img/done-22.png" />
                    </div>
                  </div>
                  ) : (
                    <img src="/img/on-track.png" alt="Warning" className="status-icon" />
                  )}
                </div>  
                </div>       

                <div className="sensor-item">
              <div className="div-7">
                      <div className="noun-passenger">
                      <img
                        className="group-33"
                        alt="Group"
                        src="/img/group-632526-5.png"
                      />
                      </div>
                    </div>
                <div className="sensor-info">
                  <p className="sensor-name">Humidity Sensor</p>
                  <p className="sensor-value">Value : {sensorData.humidity}</p>
                </div>   
                <div className={`sensor-status ${sensorData.humidity_status === "Good" ? "good" : "warning"}`}>
                  {sensorData.humidity_status === "Good" ? (
                    <div className="on-track-6">
                    <div className="done-instance-wrapper">
                      <img className="done done-2" alt="Done" src="/img/done-22.png" />
                    </div>
                  </div>
                  ) : (
                    <img src="/img/on-track.png" alt="Warning" className="status-icon" />
                  )}
                </div>      
                </div>     

                <div className="sensor-item">
              <div className="div-7">
                      <div className="noun-passenger">
                      <img
                        className="group-33"
                        alt="Group"
                        src="/img/vector-51.png"
                      />
                      </div>
                    </div>
                <div className="sensor-info">
                  <p className="sensor-name">Air Quality Sensor</p>
                  <p className="sensor-value">Value : {sensorData.air_quality}</p>
                </div>   
                <div className={`sensor-status ${sensorData.air_quality_status === "Good" ? "good" : "warning"}`}>
                  {sensorData.air_quality_status === "Good" ? (
                    <div className="on-track-6">
                    <div className="done-instance-wrapper">
                      <img className="done done-2" alt="Done" src="/img/done-22.png" />
                    </div>
                  </div>
                  ) : (
                    <img src="/img/on-track.png" alt="Warning" className="status-icon" />
                  )}
                </div>      
                </div>   

              </div>
            </div>


              <img className="image" alt="Image" src="/img/image-1.png" />
            </div>
          </div>
        </div>

        <div className="text-wrapper-115">Hi Andrei,</div>

          {/* ✅ Dynamic Title Section */}
          <h1 className="text-wrapper-116">
            Elevator {elevatorId}, {decodedStationName} Station
          </h1>

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

        <img className="vector-31" alt="Vector" src="/img/vector-2.png" />

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

        <div className="frame-6">
          <div className="group-40" onClick={() => setModalOpen(true)}>
            <div className="overlap-group-15">
              <img className="vector-32" alt="Vector" src="/img/vector-3.png" />

              <div className="group-41" />

              <div className="text-wrapper-117">4</div>
            </div>
          </div>
        </div>

        <div className="group-42">
          <div className="overlap-46">
            <Sidebar activePage="Dashboard" 
            />
          </div>
        </div>
      </div>
    </div>
  );
};
