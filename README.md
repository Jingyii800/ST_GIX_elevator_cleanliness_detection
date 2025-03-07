# Sound Transit Elevator Cleanness Detection System 

## 📌 **Project Overview**  
### **🔹 Problem Statement**  
Public elevators frequently suffer from cleanliness issues, leading to poor user experiences and increased maintenance costs. Manual monitoring is inefficient, and automated solutions are needed to **detect and resolve issues in real time**.

### **💡 Solution**  
Our system integrates **hardware sensors (air quality, humidity, and passenger button)**, **real-time data processing**, and a **web dashboard** to:
- ✅ **Detect spills, odors, and cleanliness issues** in elevators  
- ✅ **Automatically alert staff** when an issue is detected  
- ✅ **Enable management to track and resolve alerts**  
- ✅ **Provide real-time sensor status for monitoring**  

---

## 🏗️ **Repository Structure**  

```plaintext
.github/                     # GitHub configurations & workflows
Dashboard_Backend/           # Flask-based backend for managing alerts and sensor data
Dashboard_Frontend/          # React.js-based web dashboard for monitoring and resolving alerts
fastapi-websocket/           # WebSocket service for real-time alert streaming
raspberryPi_Code/            # Code for Raspberry Pi to collect sensor data and send to the cloud
Realtime_Alerts_Pipeline/    # Cloud pipeline for processing real-time alerts (Azure Functions)
shared_utils/                # Shared utilities used across different modules
LICENSE                      # Project license
README.md                    # This documentation
```
---
## 🔧 **Tech Stack & Dependencies**
- Backend: Flask (Python), FastAPI (WebSockets), Azure Functions
- Frontend: React.js, JavaScript
- Database: Azure SQL
- Hardware: Raspberry Pi, MQ135 (air quality), DHT22 (humidity), Button sensor
- Messaging: RabbitMQ for asynchronous alert handling
### Install Dependencies
**Backend (Flask)** 
```plaintext
cd Dashboard_Backend
pip install -r requirements.txt
```
**Frontend (React.js)** 
```plaintext
cd Dashboard_Frontend
npm install
```
**Raspberry Pi Sensor Code** 
```plaintext
cd raspberryPi_Code
pip install -r requirements.txt
```
**WebSocket Service (FastAPI)** 
```plaintext
cd fastapi-websocket
pip install -r requirements.txt
```

---
## ⚙️  **Setup Instructions**
### 1️⃣ Clone the Repository
```
git clone https://github.com/your-repo/elevator-cleanliness.git
cd elevator-cleanliness
```
### 2️⃣ Setup Backend (Flask)
**Install Dependencies**
```plaintext
cd Dashboard_Backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

**Create .env File**
Copy .env.template and rename it to .env:
```
cp .env.template .env
```
Then, update the file with your actual database credentials:
```
SQL_CONNECTION_STRING=your_database_connection_string
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@example.com
SENDER_PASSWORD=your_password
```
Run the Backend Server
```
flask run
```
By default, the Flask backend runs on http://127.0.0.1:5000

### 3️⃣ Setup Frontend (React.js)
**Install Dependencies**
```
cd ../Dashboard_Frontend
npm install
```
**Configure API URL**
Edit src/config.js to point to your backend:
```
const API_BASE_URL = "http://127.0.0.1:5000";
export default API_BASE_URL;
```
**Run the Frontend**
```
npm run dev
```
### 4️⃣ Run Raspberry Pi Sensor Code
**Install Dependencies**
```
cd ../raspberryPi_Code
pip install -r requirements.txt
```
**Run Sensor Data Collection**
```
source venv/bin/activate
python iot.py
```
### 5️⃣ Start WebSocket Service
```
cd fastapi-websocket
uvicorn main:app --host 0.0.0.0 --port 8000
```
---
## 🛠**API Endpoints**
Endpoint	Method	Description

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/alerts` | `GET` | Retrieve all active alerts |
| `/alerts/<alert_id>` | `GET` | Get details of a specific alert |
| `/alerts/<alert_id>/update_issue` | `PUT` | Update issue type (solid/liquid) |
| `/alerts/<alert_id>/confirm_alert` | `PUT` | Confirm an alert and send an email |
| `/alerts/<alert_id>/confirm_cleaning?staff=Mark` | `GET` | Mark cleaning as completed |
| `/report_logs` | `GET` | Retrieve confirmed reports filtered by date, station, elevator |
| `/elevator_status` | `GET` | Get latest elevator sensor readings |

---
## 🔥 **Deployment Instructions (Azure)**
- Backend: Deploy Flask API to Azure Web App Service
- Frontend: Host React.js on Azure Static Web App
- Database: Use Azure SQL
- Real-Time Messaging: Deploy FastAPI WebSocket on Azure Web App Service
- Secrets Management: Use Azure Secrets Manager

## 🙌 **Contributors**
🔹 Jingyi Jia, Yuwei He, Chaney He
