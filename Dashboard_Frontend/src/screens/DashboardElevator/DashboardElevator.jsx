import React, { useState, useEffect } from "react";
import { Link , useParams} from "react-router-dom";
import { ActiveAlerts } from "../ActiveAlerts/ActiveAlerts";
import { Sidebar } from "../../components/Sidebar";
import "./style.css";

export const DashboardElevator = () => {

  const [showAlert, setShowAlert] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);

  const { stationName, elevatorId } = useParams(); // ✅ Extract URL parameters
  const decodedStationName = decodeURIComponent(stationName);

  // State to hold sensor data
  const [sensorData, setSensorData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  useEffect(() => {
      // Auto-hide the alert after 10 seconds
      const timer = setTimeout(() => setShowAlert(false), 100000);
      return () => clearTimeout(timer);
  }, []);


  useEffect(() => {
    // Fetch data from API using parameters
    const fetchElevatorData = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/elevator_status?station=${encodeURIComponent(stationName)}&elevator_num=${elevatorId}`
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

    fetchElevatorData();
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
                        <img
                        className="group-34"
                        alt="Group"
                        src="/img/group-21.png"
                      />
                    </div>
                <div className="sensor-info">
                  <p className="sensor-name">Infrared Sensor</p>
                  <p className="sensor-value">Value : {sensorData.infrared}</p>
                </div>   
                <div className={`sensor-status ${sensorData.infrared_status === "Good" ? "good" : "warning"}`}>
                  {sensorData.infrared_status === "Good" ? (
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

        <div className="overlap-42">
          <Link className="medium-chart-4" to="/dashboard-41">
            <div className="overlap-43">
              <div className="medium-chart-5">
                <div className="label-6">Report Logs</div>
              </div>

              <div className="name-7">UW Station, Elevator 2</div>

              <div className="date-7">12:00pm&nbsp;&nbsp;2024/12/07</div>

              <img
                className="vector-30"
                alt="Vector"
                src="/img/vector-2-3.png"
              />

              <div className="rectangle-31" />
            </div>
          </Link>

          <div className="name-8">UW Station, Elevator 7</div>

          <div className="group-35">
            <div className="overlap-44">
              <img
                className="group-36"
                alt="Group"
                src="/img/group-632523.png"
              />

              <img
                className="on-track-7"
                alt="On track"
                src="/img/on-track.png"
              />
            </div>
          </div>

          <div className="group-37">
            <img className="group-38" alt="Group" src="/img/group-632523.png" />
          </div>

          <div className="name-9">Warning</div>

          <div className="name-10">Warning</div>

          <div className="date-8">Resolution in progress</div>

          <div className="date-9">Resolution in progress</div>

          <div className="group-37">
            <div className="overlap-44">
              <img
                className="group-36"
                alt="Group"
                src="/img/group-632523.png"
              />

              <img
                className="on-track-7"
                alt="On track"
                src="/img/on-track.png"
              />
            </div>
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
