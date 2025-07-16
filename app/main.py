from fastapi import FastAPI, HTTPException, status
from app import service, access_control

app = FastAPI()

@app.on_event("startup")
def init():
    access_control.save_access_status(access_control.load_access_status())

@app.get("/status")
def get_service_status():
    return {"status": service.get_status()}

@app.post("/start")
def start_nginx():
    if not access_control.load_access_status():
        raise HTTPException(status_code=403, detail="Access denied")
    service.start_service()
    return {"message": "nginx started"}

@app.post("/stop")
def stop_nginx():
    if not access_control.load_access_status():
        raise HTTPException(status_code=403, detail="Access denied")
    service.stop_service()
    return {"message": "nginx stopped"}

@app.post("/restart")
def restart_nginx():
    if not access_control.load_access_status():
        raise HTTPException(status_code=403, detail="Access denied")
    service.restart_service()
    return {"message": "nginx restarted"}

@app.get("/access")
def check_access():
    return {"access_granted": access_control.load_access_status()}

@app.post("/access/enable")
def enable_access():
    access_control.save_access_status(True)
    return {"message": "Access enabled"}

@app.post("/access/disable")
def disable_access():
    access_control.save_access_status(False)
    return {"message": "Access disabled"}
