import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Body
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Enable logging
logging.basicConfig(level=logging.INFO)

# Store active WebSocket connections
clients = []

class Alert(BaseModel):
    station: str
    elevator_num: int
    issue: str

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """ WebSocket connection handler """
    await websocket.accept()
    clients.append(websocket)
    logging.info(f"✅ WebSocket connected: {websocket.client}")

    try:
        while True:
            data = await websocket.receive_text()
            logging.info(f"📩 Received message: {data}")
            await websocket.send_text(f"Echo: {data}")  # ✅ Send back confirmation
    except WebSocketDisconnect:
        clients.remove(websocket)
        logging.warning("❌ WebSocket disconnected.")

@app.post("/send_alert")
async def send_alert(alert: Alert = Body(...)): 
    """ API endpoint for Azure Function to send an alert """
    message = f"🚨 New Cleanliness Alert at {alert.station} Station, Elevator {alert.elevator_num} - {alert.issue} Waste!"

    # Send message to all connected WebSocket clients
    # ✅ Send message to all connected WebSocket clients
    for client in clients:
        await client.send_text(message)
        logging.info(f"📤 Sent alert to WebSocket: {message}")  # ✅ Log message send

    return {"status": "Alert sent", "message": message}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
