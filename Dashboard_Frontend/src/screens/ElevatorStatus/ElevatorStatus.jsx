import React, { useState, useEffect } from "react";
import { LargeInput } from "../../components/LargeInput";
import { Sidebar } from "../../components/sidebar";
import API_BASE_URL from "../../config";
import { ActiveAlerts } from "../ActiveAlerts/ActiveAlerts";
import "./style.css";

export const ElevatorStatus = () => {
  const [station, setStation] = useState(""); // Selected station
  const [elevator, setElevator] = useState(""); // Selected elevator number
  const [logs, setLogs] = useState([]); // Logs from API
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error handling
  const [modalOpen, setModalOpen] = useState(false);

  const [currentTime, setCurrentTime] = useState("");

  useEffect(() => {
    const updateCurrentTime = () => {
      const now = new Date();
      
      // Format Time (HH:MM:SS AM/PM)
      const formattedTime = now.toLocaleTimeString([], { 
        hour: "2-digit", 
        minute: "2-digit", 
        second: "2-digit",
        hour12: true 
      });
  
      // Format Date (Jan 01 2025)
      const formattedDate = now.toLocaleDateString("en-US", { 
        month: "short", 
        day: "2-digit", 
        year: "numeric" 
      });
  
      setCurrentTime(`${formattedTime} ${formattedDate}`);
    };
  
    updateCurrentTime(); // Set initial time
    const interval = setInterval(updateCurrentTime, 1000); // Update every second
  
    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  // 🔹 Fetch report logs based on filters
  const fetchElevatorData = async () => {
    setLoading(true);
    setError(null);

    let url = `${API_BASE_URL}/elevator_status?`;
    console.log(station, elevator)
    if (station) url += `&station=${encodeURIComponent(station)}`;
    if (elevator) url += `&elevator_num=${elevator}`;

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Failed to fetch data. Status: ${response.status}`);

      const data = await response.json();
      // ✅ Sort by ID (ascending order)
      const sortedData = data.sort((a, b) => a.elevator_num - b.elevator_num);
      setLogs(sortedData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // 🔹 Fetch logs when filters change
  useEffect(() => {
    fetchElevatorData();
  }, [station, elevator]);

  return (
    <div className="report-logs">
      <div className="div-2">
        <img className="vector" alt="Vector" src="/img/vector-2-1.png" />

        <div className="div-3">
          <div className="div-3">
            <LargeInput
              className="large-input-instance"
              overlapClassName="design-component-instance-node"
              state="default"
              type="search-icon"
            />
            <div className="text-wrapper-6">Hi Andrei,</div>

            <div className="text-wrapper-7">Elevator Status</div>

            <div className="overlap-2">
              <div className="side-bar">
                <Sidebar activePage="Elevator Status" 
                />
              </div>
            </div>

            {/* 🔹 Time Filters */}
            <div className="group-6">
              <div className="overlap-10">
                <div className="overlap-group-4">
                  <div className = "text-wrapper-26">Current Time: {currentTime}</div>
                </div>
          </div>
            </div>

            {/* 🔹 Station & Elevator Filters */}
            <div className="group-7">
              <div className="UW-station-wrapper">
                <select className="station-dropdown" value={station} onChange={(e) => setStation(e.target.value)}>
                <option value="">All</option>
                  <option value="University Of Washington">University of Washington</option>
                  <option value="Seattle Central">Seattle Central</option>
                  <option value="Bellevue Station">Bellevue Station</option>
                </select>
              </div>

              <div className="elevator-wrapper">
                <select className="elevator-dropdown" value={elevator} onChange={(e) => setElevator(e.target.value)}>
                  <option value="">All</option>
                  <option value="1">Elevator 1</option>
                  <option value="2">Elevator 2</option>
                  <option value="3">Elevator 3</option>
                  <option value="4">Elevator 4</option>
                  <option value="5">Elevator 5</option>
                  <option value="5">Elevator 6</option>
                  <option value="7">Elevator 7</option>
                  <option value="8">Elevator 8</option>
                </select>
              </div>
            </div>

            <div className="overlap-3">
            <div className="report-logs-container elevator-status">
                  {/* 🔹 Logs Table */}
                  <div className="logs-table">
                    <table>
                      <thead>
                        <tr>
                          <th>Location</th>
                          <th>Humidity Status</th>
                          <th>Air Quailty Status</th>
                          <th>Passenger Report</th>
                          <th>Alert</th>
                        </tr>
                      </thead>
                      <tbody>
                        {logs.map((log, index) => (
                          <tr key={index}>
                            <td>{log.station} ,Elevator {log.elevator_num}</td>
                            <td>{log.humidity}, {log.humidity_status}</td>
                            <td>{log.air_quality}, {log.air_quality_status}</td>
                            <td>{log.passenger_button_status}</td>
                            <td>
                              <span className={`status-badge ${log.alert_status == "Normal" ? "resolved" : "in-progress"}`}>
                                {log.resolved ? "Resolved" : log.alert_status == "Normal" ? "Normal" : "Active"}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            <ActiveAlerts isOpen={modalOpen} onClose={() => setModalOpen(false)} />
            <div className="group-4" onClick={() => setModalOpen(true)}>
              <div className="overlap-9">
                <img className="vector-4" alt="Vector" src="/img/vector-3.png" />

                <div className="group-5" />

                <div className="text-wrapper-25">4</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
