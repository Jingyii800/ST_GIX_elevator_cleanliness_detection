import React, { useState, useEffect } from "react";
import { LargeInput } from "../../components/LargeInput";
import API_BASE_URL from "../../config";
import { Sidebar } from "../../components/sidebar";
import { ActiveAlerts } from "../ActiveAlerts/ActiveAlerts";
import "./style.css";

export const ReportLogs = () => {
  const [timeFilter, setTimeFilter] = useState("daily"); // Default to daily
  const [station, setStation] = useState(""); // Selected station
  const [alertNum, setAlertNum] = useState(0);
  const [elevator, setElevator] = useState(""); // Selected elevator number
  const [logs, setLogs] = useState([]); // Logs from API
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error handling
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const [modalOpen, setModalOpen] = useState(false);

  // 🔹 Fetch alerts counts
  const fetchAlerts = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/alerts`);
      if (!response.ok) throw new Error("Failed to fetch alerts");
      
      const data = await response.json();
      setAlertNum(data.length)
    } catch (err) {
      console.error("Error getting alerts count:", err);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  // 🔹 Fetch report logs based on filters
  const fetchReportLogs = async () => {
    setLoading(true);
    setError(null);

    let url = `${API_BASE_URL}/report_logs?time_filter=${timeFilter}`;
    console.log(station, elevator)
    if (station) url += `&station=${encodeURIComponent(station)}`;
    if (elevator) url += `&elevator_num=${elevator}`;

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Failed to fetch data. Status: ${response.status}`);

      const data = await response.json();
      setLogs(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // 🔹 Fetch logs when filters change
  useEffect(() => {
    fetchReportLogs();
  }, [timeFilter, station, elevator]);

  // 🔹 Calculate start & end dates based on timeFilter
  useEffect(() => {
    const now = new Date();
    setEndDate(now.toISOString().split("T")[0]); // Today’s date (YYYY-MM-DD)

    let calculatedStartDate;
    switch (timeFilter.toLowerCase()) {
      case "daily":
        calculatedStartDate = new Date(now);
        calculatedStartDate.setDate(now.getDate() - 1);
        break;
      case "weekly":
        calculatedStartDate = new Date(now);
        calculatedStartDate.setDate(now.getDate() - 7);
        break;
      case "monthly":
        calculatedStartDate = new Date(now);
        calculatedStartDate.setMonth(now.getMonth() - 1);
        break;
      case "yearly":
        calculatedStartDate = new Date(now);
        calculatedStartDate.setFullYear(now.getFullYear() - 1);
        break;
      default:
        calculatedStartDate = new Date(now);
    }

    setStartDate(calculatedStartDate.toISOString().split("T")[0]); // Format YYYY-MM-DD
  }, [timeFilter]);

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

            <div className="text-wrapper-7">Report Logs</div>

            <div className="overlap-2">
              <div className="side-bar">
                <Sidebar activePage="Report Logs" 
                />
              </div>
            </div>

            {/* 🔹 Time Filters */}
            <div className="group-6">
              <div className="overlap-10">
                <div className={`overlap-group-4 ${timeFilter === "daily" ? "active" : ""}`} onClick={() => setTimeFilter("daily")}>
                  <div className={`text-wrapper-26${timeFilter === "daily" ? "active" : ""}`}>Daily</div>
                </div>
                <div className={`overlap-group-4 ${timeFilter === "weekly" ? "active" : ""}`} onClick={() => setTimeFilter("weekly")}>
                  <div className={`text-wrapper-27${timeFilter === "weekly" ? "active" : ""}`}>Weekly</div>
                </div>
                <div className={`overlap-group-4 ${timeFilter === "monthly" ? "active" : ""}`} onClick={() => setTimeFilter("monthly")}>
                  <div className={`text-wrapper-28${timeFilter === "monthly" ? "active" : ""}`}>Monthly</div>
                </div>
                <div className={`overlap-group-4 ${timeFilter === "yearly" ? "active" : ""}`} onClick={() => setTimeFilter("yearly")}>
                  <div className={`text-wrapper-29${timeFilter === "yearly" ? "active" : ""}`}>Yearly</div>
              </div>
          </div>
            </div>

            {/* 🔹 Station & Elevator Filters */}
            <div className="group-7">
              <div className="UW-station-wrapper">
                <select className="station-dropdown" value={station} onChange={(e) => setStation(e.target.value)}>
                <option value="">All</option>
                  <option value="University Of Washington">University of Washington</option>
                  <option value="Union Station">Union Station</option>
                  <option value="Seattle Central">Seattle Central</option>
                  <option value="Bellevue Station">Bellevue Station</option>
                </select>
              </div>

              <div className="elevator-wrapper">
                <select className="elevator-dropdown" value={elevator} onChange={(e) => setElevator(e.target.value)}>
                  <option value="0">All</option>
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
            <div className="report-logs-container">
                  {/* 🔹 Report Summary Section */}
                  <div className="report-summary">
                    <div className="summary-title">{timeFilter.charAt(0).toUpperCase() + timeFilter.slice(1)} Report Logs ({startDate} - {endDate})</div>
                    <div className="summary-count">{logs.length} Alerts</div>
                    <div className="summary-change">{timeFilter} <span style={{ color: "#3cb371" }}>+15%</span></div>
                  </div>


                  {/* 🔹 Logs Table */}
                  <div className="logs-table">
                    <table>
                      <thead>
                        <tr>
                          <th>Location</th>
                          <th>Report Time</th>
                          <th>Resolved Time</th>
                          <th>Staff</th>
                          <th>Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {logs.map((log, index) => (
                          <tr key={index}>
                            <td>{log.station}, Elevator {log.elevatorNumber}</td>
                            <td>{log.timeStamp}</td>
                            <td>{log.duration ? `${log.duration} mins` : "N/A"}</td>
                            <td>
                              <div className="staff-info">
                                <img src="/img/image-2.png" alt="Staff" className="staff-avatar" />
                                {log.resolvedBy || "Pending"}
                              </div>
                            </td>
                            <td>
                              <span className={`status-badge ${log.resolved ? "resolved" : "in-progress"}`}>
                                {log.resolved ? "Resolved" : log.resolved ? "Resolved" : "In Progress"}
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

                <div className="text-wrapper-25">{alertNum}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
