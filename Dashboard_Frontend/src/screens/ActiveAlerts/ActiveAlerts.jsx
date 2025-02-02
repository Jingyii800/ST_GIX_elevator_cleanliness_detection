import React, { useState, useEffect } from "react";
import API_BASE_URL from "../../config";
import { Done } from "../../components/Done";
import { ConfirmPage } from "../ConfirmPage/ConfirmPage";
import "./style.css";

export const ActiveAlerts = ({ isOpen, onClose }) => {
  if (!isOpen) return null; // ✅ Don't render modal if it's not open

  const [alerts, setAlerts] = useState([]); // Store latest 4 alerts
  const [selectedAlert, setSelectedAlert] = useState(null); // Store details of the newest alert
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false); // ✅ Control Confirm Popup
  const [noAlerts, setNoAlerts] = useState(false); // ✅ Track if there are no alerts

  // 🔹 Handle Issue Type Change
  const handleChange = async (event) => {
    const newIssue = event.target.value;

    try {
      const response = await fetch(
        `${API_BASE_URL}/alerts/${selectedAlert.id}/update_issue`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ issue: newIssue }),
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to update issue. Status: ${response.status}`);
      }

      const result = await response.json();
      console.log(result.message);

      // ✅ Update local state
      setSelectedAlert((prev) => ({ ...prev, issue: newIssue }));
    } catch (error) {
      console.error("Error updating issue:", error);
    }
  };

  // 🔹 Fetch latest 4 alerts
  const fetchAlerts = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/alerts`);
      if (!response.ok) throw new Error("Failed to fetch alerts");
      
      const data = await response.json();
      setAlerts(data.slice(0, 4));

      if (data.length == 0) {
        setLoading(false);
        setNoAlerts(true); // ✅ Show "All Alerts Handled" popup
        return;
      }
      if (data.length > 0) {
        setLoading(false);
        fetchAlertDetails(data[0].logID);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

 // 🔹 Fetch alert details by ID
  const fetchAlertDetails = async (alertId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/alerts/${alertId}`);
      if (!response.ok) throw new Error("Failed to fetch alert details");

      const data = await response.json();

      // ✅ Format time from "Mon, 01 Jan 2024 08:30:00 GMT" to "HH:mm MM/DD"
      const formattedTime = new Date(data.time).toLocaleString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        month: "2-digit",
        day: "2-digit",
      });

      setSelectedAlert({ ...data, time: formattedTime });
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  // 🔹 Handle Marking as False Alarm and Move to Next Alert
  const handleFalseAlarm = async () => {
    if (!selectedAlert) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/alerts/${selectedAlert.id}/false_alarm`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to mark false alarm. Status: ${response.status}`);
      }

      const result = await response.json();
      console.log(result.message);

      // ✅ Move to the next alert in the list
      const currentIndex = alerts.findIndex((alert) => alert.logID === selectedAlert.id);
      if (currentIndex < alerts.length - 1) {
        fetchAlertDetails(alerts[currentIndex + 1].logID);
      } else {
        onClose(); // Close the modal if no more alerts
      }
    } catch (error) {
      console.error("Error marking as false alarm:", error);
    }
  };

  // ✅ Open Confirm Popup
  const handleNotifyStaff = () => {
    setShowConfirm(true);
  };

  // ✅ Handle Confirmation from Confirm Page
  const handleConfirm = async () => {
    if (!selectedAlert) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/alerts/${selectedAlert.id}/confirm_alert`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to confirm alert. Status: ${response.status}`);
      }

      const result = await response.json();
      console.log(result.message);

      setShowConfirm(false); // ✅ Close Confirm Page
      fetchAlerts(); // ✅ Refresh alerts
    } catch (error) {
      console.error("Error confirming alert:", error);
    }
  };
  

  // ✅ Show loading or error messages before rendering UI
  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p className="loading-text">Fetching Active Alerts...</p>
      </div>
    );
  }
  

  if (error) {
    return <p>Error fetching data: {error}</p>;
  }

  return (
    <div className="active-alerts">
      <div className="overlap-wrapper-3">
        <div className="overlap-50">
            <div className="overlap-51">
              <div className="group-48">
                <div className="group-49">
                <div className="alert-tabs-container">
                  <div className="overlap-group-17">
                    {alerts.map((alert, index) => (
                      <div
                        key={alert.logID}
                        className={`alert-tab ${selectedAlert?.id === alert.logID ? "active" : ""}`}
                        onClick={() => fetchAlertDetails(alert.logID)}
                      >
                        Alert {index + 1}
                      </div>
                    ))}
                  </div>
                </div>
                </div>
              </div>

              {/* 🔹 Main Alert Content (Dynamically Updates Based on Selected logID) */}
              {selectedAlert ? (
            <>
              <div className="group-50">
                  <div className="overlap-53">
                  <img
                  className="image-2"
                  alt="Image"
                  src="/img/image-1-6.png"
                />
                  <div className="text-wrapper-126">Active Alerts {alerts.findIndex(alert => alert.logID === selectedAlert?.id) + 1}</div>

                  <div className="overlap-55" onClick={handleFalseAlarm}>
                    <div className="text-wrapper-128">False Alarm</div>
                  </div>

                  <div className="overlap-54" onClick={handleNotifyStaff}>
                    <div className="text-wrapper-127">Notify Staff</div>
                  </div>



                  <div className="location">
                    <div className="text-4">
                      <div className="text-wrapper-129">
                      {selectedAlert.station} Station, Elevator {selectedAlert.elevatorNum}
                      </div>
                    </div>

                    <img
                      className="location-icon"
                      alt="Location icon"
                      src="/img/location-icon-2.png"
                    />
                  </div>

                  <div className="location-2">
                    <div className="text-5">
                      <div className="text-wrapper-129">Time：{selectedAlert.time}</div>
                    </div>
                  </div>

                  <div className="group-51">
                    <div className="img-wrapper">
                      <img
                        className="group-52"
                        alt="Group"
                        src="/img/group-25.png"
                      />
                    </div>

                    <div className="div-8">
                      <div className="on-track-9" />
                      <div
                        className="on-track-10"
                        alt="On track"
                      />
                      <img
                        className="group-58"
                        alt="Group"
                        src="/img/group-25.png"
                      />

                      <img
                        className="group-53"
                        alt="Group"
                        src="/img/group-25.png"
                      />

                      <div className="div-8">
                        <div className="overlap-56">
                          <div className="content-8">
                            <div className="div-9" />

                            <div className="name-date-5">
                              <div className="overlap-group-18">
                                <div className="name-11">Humidity Sensor</div>

                                <div className="date-10">
                                  Value：{selectedAlert.humidity}
                                </div>
                              </div>
                            </div>
                          </div>

                          <img
                            className="group-54"
                            alt="Group"
                            src="/img/group-632526-5.png"
                          />
                        </div>

                        <div className="overlap-57">
                          <div className="content-9">
                            <div className="div-9" />

                            <div className="name-date-6">
                              <div className="overlap-group-19">
                                <div className="name-11">
                                  Passenger Report
                                </div>

                                <p className="date-10">
                                Report：{selectedAlert.passenger_button ? "on" : "off"}
                                </p>
                              </div>
                            </div>
                          </div>

                          <img
                            className="vector-33"
                            alt="Vector"
                            src="/img/19-passanger-5.png"
                          />
                        </div>

                        <div className="overlap-58">
                          <div className="overlap-59">
                            <div className="content-10">
                              <div className="icon-4" />

                              <div className="name-date-7">
                                <div className="overlap-group-20">
                                  <div className="name-11">Infrared Sensor</div>

                                  <p className="date-10">
                                    Value : {selectedAlert.infrared}
                                  </p>
                                </div>

                                <div className="date-11">Value : {selectedAlert.airQuality}</div>
                              </div>
                            </div>

                            <img
                              className="group-55"
                              alt="Group"
                              src="/img/group-21.png"
                            />
                          </div>

                          <div className="content-11">
                            <div className="div-9">
                              <div className="noun-passenger-2">
                                <img
                                  className="element-passanger-2"
                                  alt="Element passanger"
                                  src="/img/vector-51.png"
                                />

                                <div className="overlap-group-21">
                                  <div className="text-wrapper-130">
                                    Created by Rian Akbar
                                  </div>

                                  <div className="text-wrapper-131">
                                    from the Noun Project
                                  </div>
                                </div>
                              </div>
                            </div>

                            <div className="name-date-8">
                              <div className="name-11">Air Quality Sensor</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="on-track-11">
                      <div className="frame-10">
                        <Done className="done-4" done="/img/done-22.png" />
                      </div>
                    </div>
                  </div>

                  <div className="group-56">
                    <div className="overlap-60">
                      <div className="rectangle-36" />

                      {/* 🟢 Dropdown Selector for Issue Type */}
                      <div className="location-3">
                      <select
                        className="issue-dropdown"
                        value={selectedAlert?.issue || "Liquid"} // Default to "solid"
                        onChange={handleChange}
                      >
                        <option value="liquid">Liquid Waste</option>
                        <option value="solid">Solid Waste</option>
                      </select>
                      </div>

                      <div className="location-4">
                        <div className="suspected-as-wrapper">
                          <div className="suspected-as">Suspected&nbsp;&nbsp;As :</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <p>Loadinging......</p>
          )}

          {/* 🚨 Confirm Page Popup */}
          {showConfirm && <ConfirmPage onConfirm={handleConfirm} onClose={() => setShowConfirm(false)} />}

            </div>
          {/* 🚨 CLose button */}
          <button className="close-button"onClick={onClose}>
            <img className="group-57" alt="Group" src="/img/group-18.png" />
          </button>
        </div>
      </div>
    </div>
  );
};
