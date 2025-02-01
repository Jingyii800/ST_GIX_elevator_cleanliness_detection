import PropTypes from "prop-types";
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./style.css";

export const Sidebar = ({ activePage }) => {

  const [weatherData, setWeatherData] = useState({ temperature: "--", humidity: "--" });

  const fetchWeatherData = async () => {
    try {
      const response = await fetch(
        "https://api.open-meteo.com/v1/forecast?latitude=47.6062&longitude=-122.3321&current_weather=true&hourly=relative_humidity_2m"
      );
      if (!response.ok) throw new Error("Failed to fetch weather data");
  
      const data = await response.json();
  
      // ✅ Get latest temperature
      const temperature = data.current_weather.temperature; // Temperature in Celsius
  
      // ✅ Get latest humidity value from hourly data
      const humidity = data.hourly.relative_humidity_2m.pop(); // Latest humidity value
  
      setWeatherData({
        temperature: `${temperature}°C`,
        humidity: `${humidity}%`,
      });
  
    } catch (error) {
      console.error("Error fetching weather data:", error);
    }
  };
  
  // ✅ Call the function inside useEffect to fetch on component mount
  useEffect(() => {
    fetchWeatherData();
  }, []);


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
      {/* ✅ Weather Section */}
      <div className="sidebar-weather">
        <p className="weather-title">Current Conditions</p>
        <p className="weather-info">
          <strong>Temp:</strong> {weatherData.temperature}
        </p>
        <p className="weather-info">
          <strong>Humidity:</strong> {weatherData.humidity}
        </p>
      </div>
    </aside>
  );
};

Sidebar.propTypes = {
  activePage: PropTypes.string.isRequired, // Current active page for highlighting
};
