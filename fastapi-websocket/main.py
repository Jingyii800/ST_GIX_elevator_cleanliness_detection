from fastapi import FastAPI, WebSocket, Body
import uvicorn
from pydantic import BaseModel

app = FastAPI()

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
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except:
        clients.remove(websocket)

@app.post("/send_alert")
async def send_alert(alert: Alert = Body(...)): 
    """ API endpoint for Azure Function to send an alert """
    message = f"🚨 New Cleanliness Alert at {alert.station} Station, Elevator {alert.elevator_num} - {alert.issue} Waste!"

    # Send message to all connected WebSocket clients
    for client in clients:
        await client.send_text(message)

    return {"status": "Alert sent", "message": message}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
